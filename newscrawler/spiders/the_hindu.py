import scrapy
from re import search
from scrapy.loader import ItemLoader

from ..items import NewscrawlerItem
from datetime import date

current_date = date.today().strftime("%Y/%m/%d")

class TheHindu(scrapy.Spider):
    name = "thehindu"
    allowed_domains = ["thehindu.com"]
    start_urls = ['https://www.thehindu.com/archive/web/',
                  'https://www.thehindu.com/archive/print/']

    def parse(self, response):
        self.logger.info('Parse function called on {}'.format(response.url))
        yield response.follow(current_date, callback = self.parse_date)

    def parse_date(self, response):
        all_articles = response.xpath('//ul[@class = "archive-list"]/li/a/@href').extract()
        yield from response.follow_all(all_articles, callback = self.parse_news_content)
        # for link in sel_article:
        #    yield response.follow(link, callback=self.parse_news_content)

    def parse_news_content(self, response):
        article_item = ItemLoader(item = NewscrawlerItem(), response = response)
        article_item.add_xpath('title', '//h1[@class = "title"]/text() | //h2[@special-article-heading]/text()')
        article_item.add_value('url', response.url)
        article_item.add_value('id', 'TH{0}'.format(search('article(\d*).ece', response.url).group(1)))
        article_item.add_xpath('author', '//a[@class = "auth-nm lnk"]/text() | //a[@class = "auth-nm no-lnk"]/text()')
        article_item.add_xpath('content', '//div[@class = "paywall"]/p/text()')
        article_item.add_xpath('location', '//span[@class = "blue-color ksl-time-stamp"]/text()')
        article_item.add_value('date', date.today())
        yield article_item.load_item()
