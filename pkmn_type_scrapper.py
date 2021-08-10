import scrapy
from scrapy.crawler import CrawlerProcess

def pkm_spider():
    class PkmSpider(scrapy.Spider):
        name = 'pkms'

        def start_requests(self):
            yield scrapy.Request('https://bulbapedia.bulbagarden.net/wiki/Bulbasaur_(Pok%C3%A9mon)')

        def parse(self, response):
            items = {}
            # name = response.css('span.CurrentConditions--tempValue--1RYJJ::text').extract()
            name = str(response.css('h1.firstHeading::text').get(default='Not Applicable').strip())[:-10]
            next_pkm = str(response.xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr[2]/td[3]/table/tbody/tr/td[1]/a/span/text()').get(default='Not Applicable').strip())[6:]
            if next_pkm == 'plicable':
                next_pkm = str(response.xpath('//*[@id="mw-content-text"]/div/table[1]/tbody/tr[1]/td[3]/table/tbody/tr/td[1]/a/span/text()').get(default='Not Applicable').strip())[6:]
            else:
                pass
            type1 = response.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td[1]/a/span/b/text()').get(default='Not Applicable').strip()
            type2 = response.xpath('//*[@id="mw-content-text"]/div/table[2]/tbody/tr[2]/td/table/tbody/tr/td[1]/table/tbody/tr/td[2]/a/span/b/text()').get(default='Not Applicable').strip()

            items['name'] = name
            items['type1'] = type1
            items['type2'] = type2

            yield items
            yield scrapy.Request(f'https://bulbapedia.bulbagarden.net/wiki/{next_pkm}_(Pok%C3%A9mon)', callback=self.parse)


    process = CrawlerProcess(settings={
        'FEED_URI': 'pkmns_name_type.csv',
        'FEED_FORMAT': 'csv'
    })

    process.crawl(PkmSpider)
    process.start()


if __name__ == "__main__":
    pkm_spider()
