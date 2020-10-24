# Import Model
import pandas as pd
from ..crawler import database, spider


class Crawler:
    '''
    參考框架 - https://www.itread01.com/content/1548981552.html
    '''
    def __init__(self):
        # url DB 管理
        self.database = database.Database()
        # url 爬取
        self.spider = spider.Craw()

    def crawl(self, db, crawler_link):
        website_soup = self.database.get_data(db, crawler_link)
        dict_crawl = self.spider.fetch_data(db, website_soup)
        df = pd.DataFrame(dict_crawl)
        print(df)
        df.to_sql(name='crawlerData',
                  con=db.engine,
                  if_exists='append',
                  index=False)
        print('done')
        return 'cralwer down'
