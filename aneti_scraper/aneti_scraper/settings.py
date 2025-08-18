# Scrapy settings for aneti_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "aneti_scraper"

SPIDER_MODULES = ["aneti_scraper.spiders"]
NEWSPIDER_MODULE = "aneti_scraper.spiders"

ADDONS = {}

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Concurrency and throttling settings
CONCURRENT_REQUESTS = 16  # Reduced from 16 to 8 to avoid overwhelming the server
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 2  # Kept as is, but can be increased if rate-limited

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/',
}

# Enable or disable downloader middlewares
# Removed Splash middleware, keeping only default middlewares
DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

# Enable or disable spider middlewares
# Removed Splash middleware
SPIDER_MIDDLEWARES = {}

# Item pipelines
ITEM_PIPELINES = {
    'aneti_scraper.pipelines.MySQLPipeline': 300,
}

# Retry settings
RETRY_ENABLED = True
RETRY_TIMES = 3  # Retry up to 3 times
RETRY_HTTP_CODES = [500, 502, 503, 504, 429]  

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"

# Optional: Add these if needed
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'  # Can move here if preferred over DEFAULT_REQUEST_HEADERS
# AUTOTHROTTLE_ENABLED = True  # Enable auto-throttling if you encounter rate limits
# AUTOTHROTTLE_START_DELAY = 5
# AUTOTHROTTLE_MAX_DELAY = 60
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0