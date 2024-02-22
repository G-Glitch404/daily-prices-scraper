from requests import Session
from parsel import Selector
import json
import datetime


class Tracker(Session):
    def __init__(self):
        super().__init__()
        self.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
        self.is_digit = lambda digit: digit.replace(' ', '').replace('.', ' ').split(' ')[0].strip()

    def __oboormarket_get_prices(self) -> dict:
        select = Selector(text=self.get('http://www.oboormarket.org.eg/Prices_ar.aspx').text, type="html")
        market_date = str(datetime.datetime.strptime(select.css('div[data-aos="fade-up"] > header > h4 ::text').get().split(' : ', 1)[1], '%m/%d/%Y').date())
        items = [
            {
                "name": item.css('div.card-header > h5::text').get(),
                "price": sorted([float(item_price)
                                 for item_price in item.css('h6.card-title ::text').extract()
                                 if self.is_digit(item_price).isdigit()])  # min, max
            } for item in select.css('#pricing > div:nth-child(2) > div > div')
        ]
        return {market_date: items}

    def __bashaier_get_prices(self) -> list:
        select = Selector(text=self.get('https://www.bashaier.net/pricing/market').text, type="html")
        return [
            {
                "name": item.css('td.text-center > img ::attr(alt)').get().capitalize(),
                "price": [float(item_price)
                          for item_price in item.css('td.text-center ::text').extract()
                          if self.is_digit(item_price).isdigit()]  # min, max, avg
            } for item in select.css('div.main-post-content > table > tbody > tr')
        ]

    def markets(self) -> str:
        return json.dumps({
            "oboormarket.org.eg": self.__oboormarket_get_prices(),
            "bashaier.net": self.__bashaier_get_prices()
        }, ensure_ascii=False)
