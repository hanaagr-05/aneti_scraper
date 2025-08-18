# ANETI Scraper

This Scrapy project scrapes job listings from the ANETI website[](http://emploi.nat.tn) and stores them in a MySQL database. It is designed for developers or recruiters who want to collect and analyze job data from ANETI programmatically.

## Features
- Scrapes job titles, descriptions, and labels from ANETI job listings.
- Stores data in a MySQL database with columns: `id`, `reference`, `profession`, `activité`, `service`, `nb_poste`, `date_post`, `niveau`, `status`, `link`, `description`.
- Supports configuration via environment variables for secure handling of database credentials and ANETI cookies (if required).
- Optional: Schedule scraping tasks with APScheduler for automated updates.

## Prerequisites
- Python 3.8+
- Git
- MySQL server (e.g., MySQL 8.0+) with a configured database
- ANETI cookies or login credentials (if required for protected pages)

## Setup
1. **Clone the repository**:
   
```bash
   git clone https://github.com/hanaagr-05/aneti_scraper.git
   cd aneti_scraper
```

2.Install dependencies:
```bash
   pip install -r requirements.txterror: externally-managed-environment
```

3.Set up MySQL database:

. Create a MySQL database (e.g., aneti_jobs):
```sql 
CREATE DATABASE aneti_jobs;
```
. Create the jobs table:
```sql
USE aneti_db;
CREATE TABLE jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    labels VARCHAR(255),
    posted BOOLEAN DEFAULT FALSE
);
```



4.Set up environment variables:
Create a .env file in the project root:
envMYSQL_HOST="localhost"
MYSQL_USER="your_mysql_user"
MYSQL_PASSWORD="your_mysql_password"
MYSQL_DATABASE="aneti_jobs"
ANETI_COOKIES="your_aneti_cookies_here"  # Optional, if ANETI requires cookies


Usage

Run the Scrapy spider manually:
```bash
scrapy crawl aneti
```
This scrapes jobs from emploi.nat.tn and saves them to the MySQL database.
Run scheduled scraping:
Start the scheduler to run the spider daily:
bashpython scheduler.py


Database Schema
Data is stored in the jobs table in the aneti_jobs MySQL database:
```sql
CREATE TABLE jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    labels VARCHAR(255),
    posted BOOLEAN DEFAULT FALSE
);
```
Project Structure
textaneti_scraper/
├── aneti_job_scraper/
│   ├── spiders/
        ├── _init_.py
│   │   └── aneti_spider.py
    ├── _init_.py
│   ├── items.py
│   ├── pipelines.py
│   ├── settings.py
|   ├── middlewares.py
|   ├── aneti_spider_scheduler.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env  # Not committed

Ethical Considerations

Compliance: Respect ANETI’s terms of service and robots.txt. Set DOWNLOAD_DELAY = 2 in settings.py to avoid overloading the server.
Data Privacy: Ensure scraped data complies with Tunisian data protection laws. Do not store or share personal information (e.g., names, emails).
Rate Limiting: Configure Scrapy settings (e.g., DOWNLOAD_DELAY, CONCURRENT_REQUESTS) to mimic human behavior and avoid IP bans.

Dependencies

Scrapy: Web scraping framework.
mysql-connector-python: For MySQL database connectivity.
python-dotenv: For environment variables.
APScheduler: For scheduled scraping.

See requirements.txt for the full list.
Contributing
Contributions are welcome! Please:

Fork the repository.
Create a feature branch (git checkout -b feature/YourFeature).
Commit changes (git commit -m "Add YourFeature").
Push to the branch (git push origin feature/YourFeature).
Open a pull request.

License
MIT License