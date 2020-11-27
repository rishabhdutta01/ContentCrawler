import scrapy
from re import search
from scrapy.loader import ItemLoader
from pandas import datetime
from ..items import NewscrawlerItem
from datetime import date

# start variable to store the starting date of archive page, later used for storing startime-number.cms
start_date_day_index = 36892
start_date = datetime(2001, 1, 1).date()
current_date = date.today()
no_of_days_elapsed = int((current_date-start_date).days) + start_date_day_index

current_date_str = date.today().strftime("%Y/%m/%d")
year=int(current_date_str.split("/")[0])
month=int(current_date_str.split("/")[1])
day=int(current_date_str.split("/")[2])

class TimesOfIndia(scrapy.Spider):
    name = "timesofindia"
    allowed_domains = ['timesofindia.indiatimes.com']
    start_urls = ['https://timesofindia.indiatimes.com/{}/{}/{}/archivelist/year-{},month-{},starttime-{}.cms'.format(year, month, day, year, month, no_of_days_elapsed)]

    def parse(self, response):
        self.logger.info('Parse function called on {}'.format(response.url))
        all_articles = response.xpath('//span/a/@href').extract()
        yield from response.follow_all(all_articles, callback = self.parse_news_content)

    def parse_news_content(self, response):
        article_item = ItemLoader(item = NewscrawlerItem(), response = response)
        article_item.add_xpath('title', '//h1[@class="heading1"]/arttitle/text() | //h1[@class="_23498"]/text()')
        article_item.add_value('url', response.url)
        article_item.add_value('id', 'TOI{0}'.format(search('articleshow/(\d*).cms', response.url).group(1)))
        article_item.add_xpath('author', '//a[@class = "auth_detail"]/text()')

        content = response.xpath('//arttextxml//text() | //div[@class= "_1_Akb clearfix  "]//text() | //div[@class="Normal"]//text() | //div[@class="Normal"]//text()').getall()
        if ':' in content[0]:
            article_item.add_value('content', (search('([^:]*)(.*)', content[0]).group(2)).split() + content[1:])
            article_item.add_value('location', search('([^:]*)(.*)', content[0]).group(1))
        else:
            self.logger.info('YYYYYYYYYYY')
            article_item.add_value('content', content)

        article_item.add_xpath('date', '//section/span/span/text()')
        yield article_item.load_item()
