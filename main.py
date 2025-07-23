from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep, time
from datetime import datetime
import tools
from logging import basicConfig, getLogger, INFO, ERROR, StreamHandler, Formatter
from sys import exc_info, stdout
from traceback import format_exception
import config_file
from sys import argv
from zoneinfo import ZoneInfo


SPREADSHEET_ID = config_file.spreadsheet_id
REFRESH_INTERVAL = 1800
AWAKENING_INTERVAL = 60

def parse_key_numbers(key_number_rows, fantasy_team_name, run_mode):
    data_dict = {
            "total_points": "0",
            "league_placement": "-",
            "total_players": "-",
            "percentage": "-",
            "role": "-",
            "boosters": "-",
            "league_placement_money": "-",
            "total_players_money": "-",
            "percentage_money": "-"
        }
    for row in key_number_rows:
        description = row.find_element(By.CLASS_NAME, "key-number-description").text
        data = row.find_element(By.CLASS_NAME, "key-number-data").text

        if description == 'League placement':
            try:
                data_dict["league_placement"] = data.split(" / ")[0]
                data_dict["total_players"] = data.split(" / ")[1]
                data_dict["percentage"] = f"{(int(data_dict['league_placement']) / int(data_dict['total_players'])) * 100:.2f}%"
            except:
                pass
        elif description == 'Total points':
            try:
                data_dict["total_points"] = str(int(data))
            except:
                pass
        elif description == 'Role / boosters':
            try:
                data_dict["role"] = data.split(" / ")[0]
                data_dict["boosters"] = data.split(" / ")[1]
            except:
                pass
        elif description == 'Money drafted teams':
            try:
                data_dict["league_placement_money"] = data.split(" / ")[0]
                data_dict["total_players_money"] = data.split(" / ")[1]
                data_dict["percentage_money"] = f"{(int(data_dict['league_placement_money']) / int(data_dict['total_players_money'])) * 100:.2f}%"
            except:
                pass

    if run_mode == 'leaderboard':
        return [fantasy_team_name] + list(data_dict.values())
    elif run_mode == 'tournament':
        return [data_dict["total_points"]]

def fetch_fantasy_data(url_list, run_mode, logger):
    # # Enable headless mode (optional)
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Use new headless mode for better rendering
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-web-security")  # Allow all resources
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-features=BlockInsecurePrivateNetworkRequests")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")  # Spoof real browser

    # Set up ChromeDriver
    service = Service(config_file.chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    result_tournament = []
    result_leaderboard = []
    is_first = 1
    spiderman_dies = False

    for url in url_list:
        if url == '' and run_mode == 'tournament':
            result_tournament.append(['0'])
            continue

        try:
            driver.get(url)
            wait = WebDriverWait(driver, 20)
            
            if is_first == 1:
                button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='CybotCookiebotDialogBodyButtonDecline']")))
                button.click()
                logger.info("Garbage cookies button clicked!")

            key_numbers_section = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "key-numbers-rows")))
            key_number_rows = key_numbers_section.find_elements(By.CLASS_NAME, "key-number-row")

            fantasy_team_name = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//div[@class='fantasy-team-teamname-container']//div[@class='text-ellipsis']")
                )).text
            
            result_leaderboard.append(parse_key_numbers(key_number_rows, fantasy_team_name, 'leaderboard'))
            result_tournament.append(parse_key_numbers(key_number_rows, fantasy_team_name, 'tournament'))
            logger.info(f'Successfully fetched data for {url}')

        except Exception as e:
            spiderman_dies = True

            exception_message = str(e)

            exc_type, exc_value, exc_traceback = exc_info()
            traceback_info = format_exception(exc_type, exc_value, exc_traceback)
            
            full_exception_info = f"{exception_message}\n{''.join(traceback_info)}"
            logger.critical(full_exception_info)
            print(full_exception_info)

        finally:
            is_first = 0

    # Close browser
    try:
        driver.quit()
    except:
        pass
    # Optional: Take screenshot for debugging
    # driver.save_screenshot("debug_screenshot.png")
    # print("Screenshot saved as debug_screenshot.png")
    
    result_leaderboard = sorted(result_leaderboard, key=lambda x: int(x[1]), reverse=True)
    if run_mode == 'leaderboard':
        return result_leaderboard, spiderman_dies

    elif run_mode == 'tournament':
        return result_tournament, result_leaderboard, spiderman_dies

def read_config(logger):
    config_data = tools.readDataFromSpreadsheet(spreadsheetId=SPREADSHEET_ID, range_name='Config!A2:A')
    logger.info('Successfully read config_data.')

    try:
        _ = config_data[0][0]
        timely_refresh = 1
    except:
        timely_refresh = 0

    url_list = []
    if len(config_data) > 3:
        for url in config_data[3:]:
            try:
                url_list.append(url[0])
            except:
                pass
    
    return timely_refresh, set(url_list)

def read_tournament_config(logger):
    config_data = tools.readDataFromSpreadsheet(spreadsheetId=SPREADSHEET_ID, range_name='Config!C3:J')
    logger.info('Successfully read tournament_config_data.')

    url_list = []
    players_count = int(config_data[0][0])

    if len(config_data) != players_count+3:
        raise RuntimeError('I bet there is an x missing.')

    for i in range(1,len(config_data[1])):
        if config_data[-1][i].lower() == 'x':
            index = i
            break

    for i in range(players_count):
        try:
            url_list.append(config_data[i+2][index])
        except:
            url_list.append('')

    output_range = f"Tournament!{config_data[0][index]}4:{config_data[0][index]}"
    
    return url_list, output_range

def push_results(results, spiderman_dies, logger):
    now = datetime.now(ZoneInfo("Europe/Berlin"))
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    push_data = []
    push_data.append({'range':'Leaderboard!L2','values':[[formatted_time]]})

    if spiderman_dies:
        push_data.append({'range':'Leaderboard!L3','values':[["Mr. Stark, I don't feel so good..."]]})

    if results:
        push_data.append({'range':'Leaderboard!A2','values':results})

        tools.clearDataSpreadsheetRange(spreadsheetId=SPREADSHEET_ID,range_name='Leaderboard!A2:J')
        logger.info('Cleared Leaderboard!A2:J')

    tools.writeMultipleRangesToSpreadsheet(spreadsheetId=SPREADSHEET_ID,data=push_data)
    logger.info('Refreshed the spreadsheet.')

def push_tournament_results(results_tournament, output_range, results_leaderboard, spiderman_dies, logger):
    now = datetime.now(ZoneInfo("Europe/Berlin"))
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    push_data = []
    push_data.append({'range':'Tournament!A1','values':[[formatted_time]]})

    if spiderman_dies:
        push_data.append({'range':'Tournament!A2','values':[[" "]]})

    else:
        if results_tournament:
            push_data.append({'range':output_range,'values':results_tournament})
        if results_leaderboard:
            push_data.append({'range':'Leaderboard!A2','values':results_leaderboard})
        tools.clearDataSpreadsheetRange(spreadsheetId=SPREADSHEET_ID,range_name='Leaderboard!A2:J')
        logger.info('Cleared Leaderboard!A2:J')
        push_data.append({'range':'Leaderboard!L2','values':[[formatted_time]]})

    tools.writeMultipleRangesToSpreadsheet(spreadsheetId=SPREADSHEET_ID,data=push_data)
    logger.info('Refreshed the spreadsheet.')

def main():
    if len(argv) != 2:
        raise ValueError("Exactly one argument is required: 'tournament' or 'leaderboard'.")

    arg = argv[1].lower()

    if arg not in {"tournament", "leaderboard"}:
        raise ValueError(f"Invalid argument: '{arg}'. Expected 'tournament' or 'leaderboard'.")

    basicConfig(
        filename=f"fantasy_scraper_{arg}.log",
        level=INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger = getLogger(f"fantasy_scraper_{arg}")
    getLogger("googleapiclient.discovery_cache").setLevel(ERROR)

    console_handler = StreamHandler(stdout)
    console_handler.setLevel(INFO)
    console_handler.setFormatter(Formatter("%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"))
    logger.addHandler(console_handler)

    last_refresh_time = 0

    while True:
        try:
            logger.info("I'm up bitches!")
            current_time = time()

            am_i_impatient, url_list = read_config(logger)

            if am_i_impatient == 1 or\
                current_time - last_refresh_time >= REFRESH_INTERVAL:

                if am_i_impatient == 1:
                    tools.clearDataSpreadsheetRange(spreadsheetId=SPREADSHEET_ID, range_name='Config!A2')

                if arg == 'tournament':
                    url_list, output_range = read_tournament_config(logger)
                    results_tournament, results_leaderboard, spiderman_dies = fetch_fantasy_data(url_list, arg, logger)
                    push_tournament_results(results_tournament, output_range, results_leaderboard, spiderman_dies, logger)

                elif arg == 'leaderboard' and url_list:
                    results, spiderman_dies = fetch_fantasy_data(url_list, arg, logger)         
                    push_results(results, spiderman_dies, logger)

                spiderman_dies = False
                last_refresh_time = current_time
                logger.info('It was hard work, going to sleep.')

            else:
                logger.info('Boring, going to sleep.')
                            
        except Exception as e:
            spiderman_dies = True
            exception_message = str(e)

            exc_type, exc_value, exc_traceback = exc_info()
            traceback_info = format_exception(exc_type, exc_value, exc_traceback)
            
            full_exception_info = f"{exception_message}\n{''.join(traceback_info)}"

            try:
                if arg == 'leaderboard':
                    push_results([], spiderman_dies, logger)
                elif arg == 'tournament':
                    push_tournament_results([], '', spiderman_dies, logger)

            except Exception as f:
                logger.critical('We are living a really sad reality if the error handling fails...')
                exception_message = str(f)

                exc_type, exc_value, exc_traceback = exc_info()
                traceback_info = format_exception(exc_type, exc_value, exc_traceback)
                
                full_exception_info = f"{exception_message}\n{''.join(traceback_info)}"
                logger.critical(full_exception_info)
            else:
                spiderman_dies = False

        finally:
            sleep(AWAKENING_INTERVAL)

if __name__ == "__main__":
    main()
