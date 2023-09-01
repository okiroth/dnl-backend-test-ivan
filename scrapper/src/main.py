from database_handler import save_json_to_DB
import scrapy
import logging

# logging.getLogger('scrapy').propagate = False

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://www.urparts.com/index.cfm/page/catalogue",
        # "https://www.urparts.com/index.cfm/page/catalogue/Volvo/Loader%20Parts/L45"
    ]


    # took 384 seconds, 1 minute less than the old one
    def parse(self, response):
        org_url = response.url.replace('https://www.urparts.com/', '')
        # models page has 2 divs with class c_container
        for sel in (response.css('div.c_container')[-1]).css('ul').css('li').css('a'):
            url = sel.xpath('@href').get()
            # check that we are not querying the parts urls
            # check that we are not querying a previous (shorter) url
            if (url is None) or ("page/catalogue?part=" in url) or (len(url) < len(org_url)):
                yield {
                    "content": sel.css('*::text').extract(),
                    "url": url,
                }
            else:
                print(org_url, '---->', url)
                yield response.follow(url, self.parse)

    
    
