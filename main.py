import asyncio
import os
import pickle
import random
import time
from pyrogram import Client
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Instagram Credentials (ONLY needed for first-time login)
USERNAME = os.getenv("INSTAGRAM_USERNAME")
PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

# Collection Link (Saved Reels)
COLLECTION_URL = os.getenv("COLLECTION_URL")

# Telegram API Credentials
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME")
CHAT_ID = int(os.getenv("CHAT_ID"))

# File Paths
COOKIES_FILE = "instagram_cookies.pkl"
REELS_FILE = "reels.txt"
MESSAGE_LOG = "sent_messages.txt"

# Initialize Chrome Driver
options = uc.ChromeOptions()
options.headless = False
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"
)
driver = uc.Chrome(options=options)


def load_cookies():
    """Loads saved cookies to avoid logging in every time."""
    if os.path.exists(COOKIES_FILE):
        driver.get("https://www.instagram.com")
        time.sleep(3)
        with open(COOKIES_FILE, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
        print("Cookies loaded successfully!")
    else:
        login_instagram()


def save_cookies():
    """Saves cookies after login for future use."""
    with open(COOKIES_FILE, "wb") as file:
        pickle.dump(driver.get_cookies(), file)
    print("Cookies saved!")


def login_instagram():
    """Logs into Instagram and saves cookies."""
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(5)

    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)

    time.sleep(8)  # Wait for login
    save_cookies()


def scrape_saved_links():
    """Continuously scrapes links while the user scrolls manually."""
    driver.get(COLLECTION_URL)
    time.sleep(5)  # Allow page to load

    post_links = set()
    print("Manually scroll to load more reels. Close the tab when done.")

    try:
        while True:
            post_elements = driver.find_elements(
                By.XPATH, "//a[contains(@href, '/p/') or contains(@href, '/reel/')]"
            )
            new_links = {post.get_attribute("href") for post in post_elements}
            post_links.update(new_links)

            print(f"Collected {len(post_links)} links so far...", end="\r")
            time.sleep(2)  # Wait before checking again
    except:
        print("\nTab closed. Stopping link collection.")

    return list(post_links)


def save_links_to_file(links):
    """Saves reel links to a file."""
    with open(REELS_FILE, "w", encoding="utf-8") as file:
        for link in links:
            file.write(link + "\n")
    print(f"{len(links)} reel links saved to {REELS_FILE}")


async def send_reels():
    """Sends reels from the saved file to Telegram and deletes them after a delay."""
    async with Client(SESSION_NAME, API_ID, API_HASH) as app:

        if not os.path.exists(REELS_FILE):
            print("No reels.txt file found.")
            return

        with open(REELS_FILE, "r", encoding="utf-8") as file, open(
            MESSAGE_LOG, "w"
        ) as log_file:
            for line in file:
                reel_link = line.strip()
                if reel_link:
                    message = await app.send_message(CHAT_ID, reel_link)
                    log_file.write(f"{message.id}\n")  # Save message ID

                    await asyncio.sleep(5)  # Wait before deleting
                    await app.delete_messages(CHAT_ID, message.id)

                    print(f"Sent and deleted: {reel_link}")


def main():
    """Runs both Instagram scraping and Telegram sending."""
    load_cookies()
    reel_links = scrape_saved_links()
    save_links_to_file(reel_links)
    asyncio.run(send_reels())


if __name__ == "__main__":
    main()
