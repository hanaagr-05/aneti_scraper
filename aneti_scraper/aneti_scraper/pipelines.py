# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import mysql.connector
from scrapy.exceptions import DropItem
import logging

class MySQLPipeline:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def open_spider(self, spider):
        try:
            self.conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',  
                database='aneti_data'
            )
            self.cursor = self.conn.cursor()
            self.cursor.execute("""
                    CREATE TABLE IF NOT EXISTS offres (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        reference VARCHAR(100) UNIQUE,
                        profession VARCHAR(255),
                        activité VARCHAR(255),
                        service VARCHAR(255),
                        nb_poste INT,
                        date_post VARCHAR(50),
                        niveau VARCHAR(100),
                        status VARCHAR(255),
                        link VARCHAR(255),
                        description TEXT
                    )
                """)
        except mysql.connector.Error as e:
            logging.error(f"Database connection error: {e}")
            raise


    def close_spider(self, spider):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        try:
            self.cursor.execute(
                "SELECT reference FROM offres WHERE reference = %s",
                (item.get('reference', ''),)
            )
            if self.cursor.fetchone():
                raise DropItem(f"Duplicate item found: {item['reference']}")
            
            

            self.cursor.execute("""
                INSERT INTO offres (reference, profession, activité, service, nb_poste, date_post, niveau, status, link, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                item.get('reference', ''),
                item.get('profession', ''),
                item.get('activite', ''),
                item.get('service', ''),
                item.get('nb_poste', None),
                item.get('date_post', ''),
                item.get('niveau', ''),
                item.get('status', ''),
                item.get('link', ''),
                item.get('description', '')
            ))
            self.conn.commit()
        except DropItem as e:
            logging.warning(str(e))
            return item
        except Exception as e:
            logging.error(f"Error inserting item: {e}")
            self.conn.rollback()
        return item
    