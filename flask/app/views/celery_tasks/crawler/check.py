# Import 爬蟲相關
import requests
from bs4 import BeautifulSoup

# Import 資料處理相關
from datetime import datetime


class Craw:
    def __init__(self):
        self.dict_crawl = {"name": [], "description": [], "link": []}

        self.headers = {
            "Referer": "https://qdm.zendesk.com/hc/zh-tw/sections/203750947-%E5%8A%9F%E8%83%BD%E7%95%B0%E5%8B%95",
            "User-Agent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko; googleweblight) Chrome/38.0.1025.166 Mobile Safari/535.19",
            "X-Requested-With": "XMLHttpRequest",
        }

        self.NOW = datetime.now()

    def fetch_data(self, website_url):
        url = website_url
        r = requests.get(url=url, headers=self.headers).text

        soup = BeautifulSoup(r, features="html.parser")
        # print(soup)
        try:
            for i in range(2):
                print(i)
                self.dict_crawl["name"].append(
                    soup.find_all("h4")[i + 2].text.replace("\n", "")
                )
                self.dict_crawl["description"].append(
                    soup.find_all(class_="itemcontent")[i + 2].text[:500]
                )
                self.dict_crawl["link"].append(soup.find_all("a")[i].get("href"))

            # print(self.dict_crawl)

        except Exception as e:
            print(e)

        return self.dict_crawl


if __name__ == "__main__":

    url_op = "https://googlewebmastercentral.blogspot.com/atom.xml"

    crawler = Craw()
    task = crawler.fetch_data(url_op)
    print(task)
