import scrapy
from aneti_scraper.items import AnetiScraperItem
import logging

class AnetiSpider(scrapy.Spider):
    name = "aneti_spider"
    allowed_domains = ["emploi.nat.tn"]
    start_urls = ["https://www.emploi.nat.tn/fo/Fr/global.php?page=993&menu1=1"]

    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'LOG_LEVEL': 'INFO',
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS': 8,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',  # Mimic a browser
    }

    def start_requests(self):
        logging.info(f"Starting AnetiSpider... Allowed domains: {self.allowed_domains}")
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse, meta={'page_number': 993})

    def parse(self, response):
        try:
            logging.debug(f"Response status: {response.status}, URL: {response.url}, Body length: {len(response.body)}")
            if response.status != 200:
                logging.warning(f"Non-200 status on page: {response.url}. Skipping.")
                return

            list_emp = response.xpath('//tr[contains(@class, "emp")]')
            logging.debug(f"Found {len(list_emp)} elements with class 'emp'")

            if not list_emp:
                logging.warning(f"No job listings found on page: {response.url}")
                with open(f"page_{response.meta['page_number']}.html", "w", encoding="utf-8") as f:
                    f.write(response.text)
                logging.debug(f"Saved page source to page_{response.meta['page_number']}.html")
            else:
                for emp in list_emp:
                    item = AnetiScraperItem()
                    item['reference'] = emp.css('td.poste a.ref::text').get(default='').strip()
                    item['profession'] = emp.css('td.profession a::text').get(default='').strip()
                    item['activite'] = emp.css('td.nom::text').get(default='').strip()
                    item['region'] = emp.css('td.service::text').get(default='').strip()
                    item['nb_poste'] = emp.css('td.poste[align="center"]::text').get(default='').strip()
                    item['date_post'] = emp.css('td.status:not([style*="display:none"])::text').get(default='').strip()
                    item['niveau'] = emp.css('td.poste[style*="display:none"]::text').get(default='').strip()
                    item['status'] = emp.css('td.status[style*="display:none"]::text').get(default='').strip()
                    relative_link = emp.css('td.poste a.ref::attr(href)').get()
                    item['link'] = response.urljoin(relative_link) if relative_link else ''

                    if item['link']:
                        yield scrapy.Request(
                            url=item['link'],
                            callback=self.parse_job,
                            meta={'item': item.copy()},  # Pass item to parse_job for description
                            dont_filter=True  # Avoid duplicate filtering for detail pages
                        )
                    else:
                        item['description'] = ''  # Default empty description for items without links
                        yield item

        except Exception as e:
            logging.error(f"Error in parse: {e}")

    def parse_job(self, response):
        try:
            if response.status != 200:
                logging.warning(f"Non-200 status on job page: {response.url}. Skipping.")
                return

            item = response.meta['item']  # Retrieve the original item passed via meta
            trs = response.xpath('.//table[@class="table"]//tr')
            description_parts = []
            for tr in trs:
                texts = tr.css('td ::text').getall()
                clean_texts = [t.strip() for t in texts if t.strip()]
                if clean_texts:
                    description_parts.append(' '.join(clean_texts))

            item['description'] = ' '.join(description_parts)
            yield item  # Yield the item with the description

        except Exception as e:
            logging.error(f"Error in parse_job: {e}")
