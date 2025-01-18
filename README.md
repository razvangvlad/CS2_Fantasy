# 🔥 Fantasy Data Scraper

**Fantasy Data Scraper** is an automated Python script that **scrapes HLTV Fantasy team data** and updates it in a **Google Spreadsheet**. It runs periodically, handling cookies, refreshing data on demand, and maintaining logs for debugging.

## 📜 Features
- **Scrapes Fantasy team stats** from HLTV Fantasy.
- **Handles cookie popups** automatically.
- **Stores results in Google Sheets**.
- **Auto-refreshes every 15 minutes** (900 seconds).
- **Supports on-demand refresh** by checking a spreadsheet flag.
- **Logs all actions** to `fantasy_scraper.log`.

---

## 🚀 Installation

### 1️⃣ **Clone the Repository**
```sh
git clone https://github.com/yourusername/fantasy-data-scraper.git
cd fantasy-data-scraper
```

### 2️⃣ **Set Up a Virtual Environment**
```sh
python -m venv venv
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows
```

### 3️⃣ **Install Dependencies**
```sh
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

> **If `requirements.txt` is missing, install manually:**
```sh
python -m pip install pandas
python -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
python -m pip install beautifulsoup4
python -m pip install selenium
brew install chromedriver  # macOS users only
```

---

## ⚙️ **Configuration**
1. **Set up Google Sheets API** and update credentials in `tools.py`.
2. Ensure `SPREADSHEET_ID` is set correctly in `main.py`.

---

## 🏃 **Running the Script**
```sh
python main.py
```

- The script **fetches fantasy team data** every 15 minutes (`REFRESH_INTERVAL = 900`).
- It **checks Google Sheets every minute** for a **manual refresh request**.
- Logs are stored in `fantasy_scraper.log`.

---

## 📊 **Logging & Debugging**
- **All actions are logged** to `fantasy_scraper.log`.
- To view logs in real-time:
  ```sh
  tail -f fantasy_scraper.log
  ```

---

## 🎯 **Project Structure**
```
📂 fantasy-data-scraper/
│── 📜 main.py             # Main script that runs the scraper
│── 📜 tools.py            # Utility functions (Google Sheets API)
│── 📜 fantasy_scraper.log # Log file storing execution details
│── 📜 venv/               # Virtual environment (ignored in .gitignore)
│── 📜 README.md           # Project documentation
│── 📜 requirements.txt    # Python dependencies
```

---

