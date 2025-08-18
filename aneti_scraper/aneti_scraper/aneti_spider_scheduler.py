import schedule
import subprocess
import time
import logging
from pathlib import Path

# Create a logs folder
Path("logs").mkdir(exist_ok=True)

# Logging configuration (to file and console)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/scheduler.log"),
        logging.StreamHandler()
    ]
)

def run_spider():
    try:
        logging.info("Starting spider...")
        subprocess.run(["scrapy", "crawl", "aneti_spider"], check=True)
        logging.info("Spider executed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Spider execution failed: {e}")

def schedule_spider():
    schedule.every().day.at("19:00").do(run_spider)
    logging.info("Spider scheduled to run daily at 19:00.")

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    schedule_spider()
