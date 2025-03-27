# Instagram Reel Scraper & Sender

This project is a two-in-one script that:
1. **Scrapes saved reels from a specified Instagram collection**
2. **Automatically sends them to a Telegram chat and deletes them after a short delay**

## Features
- **Automated Login**: Uses cookies to avoid logging in every time.
- **Scrape Instagram Reels**: Extracts all saved reels from a given collection.
- **Send to Telegram**: Automatically sends the scraped reels to a specified Telegram chat.
- **Auto-Delete Messages**: Deletes each sent reel after a short delay.

## Requirements
- Python 3.7+
- Selenium (undetected_chromedriver)
- Pyrogram (Telegram client)
- An Instagram account with saved reels
- A Telegram bot with access to the target chat

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/tars-06/reelstotg.git
   cd ReelsToTG
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Setup
1. **Instagram Credentials**:
   - Update `USERNAME` and `PASSWORD` in the script for the first-time login.
   - Cookies will be saved automatically to avoid re-login.

2. **Telegram API**:
   - Get your `API_ID` and `API_HASH` from [my.telegram.org](https://my.telegram.org/).
   - Set up a session file for Pyrogram.
   - Specify the `chat_id` where reels should be sent.

3. **Collection URL**:
   - Update `COLLECTION_URL` with the link to your saved reels collection.

## Usage
Run the script to scrape and send reels:
```sh
python main.py
```

## How It Works
1. The script logs into Instagram (or loads saved cookies).
2. It scrapes all reel links from the specified collection.
3. The links are saved to `reels.txt`.
4. The Telegram bot reads the links and sends them to the chat.
5. Each message is deleted after a short delay.

## Notes
- **Ensure your Instagram account is logged in and verified.**
- **Use a VPN if Instagram blocks automation attempts.**
- **Your Telegram bot must have permission to send and delete messages in the target chat.**

## Future Improvements
- **Error Handling:** Improve exception handling for network failures and login issues.
- **Auto Scrolling:** Automate scrolling to load all reels without manual input.
- **Parallel Sending:** Use `asyncio.gather()` to speed up the sending process.
- **Smart Deletion Timing:** Randomize deletion time to avoid detection patterns.
- **Headless Mode:** Fully enable headless scraping for efficiency.
- **Config File:** Store credentials & settings in a `.env` file instead of hardcoding.
- **Logging:** Save logs of sent and deleted messages for tracking.
- **Multi-Account Support:** Enable handling of multiple Instagram or Telegram accounts.

## License
This project is for educational purposes only. Use responsibly.

