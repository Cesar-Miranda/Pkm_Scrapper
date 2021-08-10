import scrapy
from scrapy.crawler import CrawlerProcess

all_pkm_names = []
special_names = '''DeoxysWormadamGiratinaShayminBasculinDarmanitanTornadusThundurusLandorus
KeldeoMeloettaMeowsticAegislashPumpkabooGourgeistZygardeHoopaOricorioLycanrocWishiwashiMinior
ToxtricityEiscueIndeedeeMorpekoZacianZamazentaUrshifu'''


# checking variations of the pokemon like Mega, alolan etc...
def name_equal(pkm_name, all_names):
    for name in all_names:
        if pkm_name in all_names and len(pkm_name) == len(name):
            return True


def pkm_spider():
    class PkmSpider(scrapy.Spider):
        name = 'pkmns'

        def start_requests(self):
            yield scrapy.Request('https://pokemondb.net/pokedex/all')

        def parse(self, response):
            items = {}
            n_counter = 0
            subtext_number = 0
            stat_multiplier = 0

            # Name
            for pkmn in response.css('a.ent-name'):
                name = pkmn.css('::text').get()


                try:
                    if name_equal(name, all_pkm_names) or name in special_names:
                        name = f"{name} ({response.css('small.text-muted::text').getall()[subtext_number]})"
                        subtext_number += 1
                except:
                    pass

                items['name'] = name

                # Number
                number = response.css('span.infocard-cell-data::text').getall()[n_counter]
                items['number'] = number

                items['hp'] = response.css('td.cell-num::text').getall()[stat_multiplier]
                items['atk'] = response.css('td.cell-num::text').getall()[stat_multiplier+1]
                items['defense'] = response.css('td.cell-num::text').getall()[stat_multiplier+2]
                items['sp_atk'] = response.css('td.cell-num::text').getall()[stat_multiplier+3]
                items['sp_defense'] = response.css('td.cell-num::text').getall()[stat_multiplier+4]
                items['speed'] = response.css('td.cell-num::text').getall()[stat_multiplier+5]

                n_counter += 1
                stat_multiplier += 6
                if n_counter == len(response.css('a.ent-name')):
                    break
                yield items
                all_pkm_names.append(items['name'])

            yield items
            all_pkm_names.append(items['name'])

    process = CrawlerProcess(settings={
        'FEED_URI': 'pkmns_stat.csv',
        'FEED_FORMAT': 'csv'
    })

    process.crawl(PkmSpider)
    process.start()


if __name__ == "__main__":
    pkm_spider()
