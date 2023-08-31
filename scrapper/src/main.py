import asyncio
import json
from database_handler import save_json_to_DB
import time
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://www.urparts.com/index.cfm/page/catalogue",
    ]

    def parse(self, response):
        for sel in response.css('div#content').css('ul').css('li').css('a'):
            url = sel.xpath('@href').get()
            if url is not None:
                yield response.follow(url, self.parse)
            yield {
                "url": url,
                "brand": sel.css('::text').get(),
            }

        # next_page = response.css('li.next a::attr("href")').get()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)
    