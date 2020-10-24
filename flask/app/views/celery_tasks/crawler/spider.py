# Import 爬蟲相關
import requests, cloudscraper
from bs4 import BeautifulSoup
import feedparser

# Import 資料處理相關
import pandas as pd
from datetime import datetime
import re


class Craw:
    def __init__(self):

        self.dict_crawl = {
            'wid': [],
            'crawler_name': [],
            'crawler_description': [],
            'crawler_link': [],
            'insert_time': []
        }

        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Macintosh Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }

        self.NOW = datetime.now()

    def fetch_data(self, db, website_db):
        for row in range(website_db.shape[0]):
            check_crawler_type = website_db['type'][row]
            url = website_db['website_url'][row]
            try:
                if check_crawler_type == 'cloudscraper':
                    new_body = cloudscraper.create_scraper().get(url).text
                    soup = BeautifulSoup(new_body, features="html.parser")

                elif check_crawler_type == 'feed':
                    feed = feedparser.parse(url).entries

                else:
                    r = requests.get(url=url, headers=self.headers).text
                    soup = BeautifulSoup(r, features="html.parser")

                for i in range(2):
                    css_name = eval(website_db['css_name'][row])
                    css_description = eval(website_db['css_description'][row])
                    css_link = eval(website_db['css_link'][row])

                    self.dict_crawl['wid'].append(website_db['wid'][row])
                    self.dict_crawl['crawler_name'].append(css_name)
                    self.dict_crawl['crawler_description'].append(
                        css_description)
                    self.dict_crawl['crawler_link'].append(css_link)
                    self.dict_crawl['insert_time'].append(self.NOW)

                df = pd.DataFrame({
                    'wid': [website_db['wid'][row]],
                    'crawler_status': ['ok'],
                    'insert_time': [self.NOW],
                })

                df.to_sql(name='statusLog',
                          con=db.engine,
                          if_exists='append',
                          index=False)

            except Exception as e:
                print('[This is Exception ---666---]', e)
                dff = pd.DataFrame({
                    'wid': [website_db['wid'][row]],
                    'crawler_status': ['error'],
                    'insert_time': [self.NOW],
                })
                dff.to_sql(name='statusLog',
                           con=db.engine,
                           if_exists='append',
                           index=False)
                df_error = pd.DataFrame({
                    'url': [url],
                    'wid': [website_db['wid'][row]],
                    'error': [str(e)],
                    'insert_time': [self.NOW],
                })
                df_error.to_sql(name='error',
                                con=db.engine,
                                if_exists='append',
                                index=False)

        return self.dict_crawl
