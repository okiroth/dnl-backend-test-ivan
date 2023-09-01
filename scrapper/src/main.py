from database_handler import save_json_to_DB
import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://www.urparts.com/index.cfm/page/catalogue",
    ]


    # took 384 seconds, 1 minute less than the old one
    def parse(self, response):
        for sel in (response.css('div.c_container')[-1]).css('ul').css('li').css('a'):
            url = sel.xpath('@href').get()
            # check that we are not querying the parts urls
            if url is not None and "page/catalogue?part=" not in url:
                yield response.follow(url, self.parse)
            yield {
                "url": url,
                "brand": sel.css('::text').get(),
            }

    
    
