import scrapy


class ToScrapeSpiderXPath(scrapy.Spider):
    name = 'toscrape-xpath'
    start_urls = [
        'https://www.brainyquote.com/topics/life-quotes',
    ]

    def parse(self, response):
        for quote in response.xpath('//div[starts-with(@id,"qpos")]'):
            yield {
                'text': quote.xpath('.//a[@title="view quote"]/text()').extract_first(),
                'author': quote.xpath('.//a[@title="view author"]/text()').extract_first(),
                'tags': quote.xpath('.//div[@class="kw-box"]/a/text()').extract()
            }