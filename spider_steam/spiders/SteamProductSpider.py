import scrapy
from urllib.parse import urlencode
from urllib.parse import urlparse
from urllib.parse import urljoin
import re
import json
from spider_steam.items import SpiderSteamItem


queries = ['strategy', 'minecraft', 'indie']

class SteamproductspiderSpider(scrapy.Spider):
    name = 'SteamProductSpider'
    allowed_domains = ['store.steampowered.com']
    start_urls = ['https://store.steampowered.com/search/']
    page = 1
    def start_requests(self):
        for query in queries:
            cur_url = 'https://store.steampowered.com/search/?' + urlencode({'term': query, 'page': str(1)})
            yield scrapy.Request(url=cur_url, callback=self.parse_keyword_response)
            cur_url = 'https://store.steampowered.com/search/?' + urlencode({'term': query, 'page': str(2)})
            yield scrapy.Request(url=cur_url, callback=self.parse_keyword_response)



    def parse_keyword_response(self, response):
        games = set()

        for res in response.xpath('//a[contains(@href, "app")]/@href').extract():
            if 'app' in res:
                games.add(res)

        for game in games:
            cur_url = game
            yield scrapy.Request(url=cur_url, callback=self.parse_game_page)

    def parse_game_page(self, response):
        if "agecheck" in response.url:
            return
        item = SpiderSteamItem()
        category = [response.xpath('//div[@class="blockbg"]/a/text()').extract()[1]]
        reviews_cnt = []
        try:
            reviews_cnt = [response.xpath('//span[@class="responsive_hidden"]/text()').extract()[-2]]
        except:
            pass
        grade = response.xpath('//span[starts-with(@class, "game_review_summary") and contains(@itemprop, "description")]/text()').extract()
        release_date = response.xpath('//div[contains(@class, "release_date")]/div[contains(@class, "date")]/text()').extract()
        developers = response.xpath('//div[contains(@id, "developers_list")]/a/text()').extract()
        tags = [re.sub(r'[\n\t\r]', "", elem) for elem in response.xpath('//div[contains(@class, "glance_tags popular_tags")]/a[contains(@class, "app_tag")]/text()').extract()]
        price = response.xpath('//div[@class="game_purchase_price price"]/text()').extract()
        price += response.xpath('//div[@class="discount_prices"]/div[@class="discount_original_price"]/text()').extract()
        platforms = response.xpath('//div[@class="sysreq_tabs"]//@data-os').extract()
        recommendations = response.xpath('//div[@id="recommended_block"]//a/@href').extract()
        details = response.xpath('//div[@class="game_area_features_list_ctn"]//div[@class="label"]/text()').extract()
        details = [re.sub(r'[\n\t\r]', "", elem) for elem in details]
        languages = response.xpath('//table[@class="game_language_options"]//td[@class="ellipsis"]/text()').extract()
        languages = [re.sub(r'[\n\t\r]', "", elem) for elem in languages]
        title = response.xpath('//div[starts-with(@class, "page_title_area")]//div[@id="appHubAppName"]/text()').extract()

        try:
            year = int(release_date.split()[-1])
            if year < 2000:
                raise Exception
        except:
            pass

        item["title"] = "".join(title).strip()
        item["category"] = "".join(category).strip()
        if platforms == []:
            platforms = ["win"]
        item["price"] = "No price"
        try:
            item["price"] = "".join(price[0]).strip().rstrip()
        except:
            pass
        item["all_reviews_count"] = "".join(reviews_cnt).strip()
        item["grade"] = "".join(grade).strip()
        item["release_date"] = "".join(release_date).strip()
        item["developers"] = developers
        item["tags"] = tags
        item["platforms"] = platforms
        item["recommendations"] = "".join(recommendations)
        item["details"] = details
        item["languages"] = languages
        yield item
