import scrapy


class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'https://www.brainyquote.com/topics/life-quotes',
    ]

    def parse(self, response):
        for quote in response.css("div[id^='qpos']"):
            yield {
                'text': quote.css("a[title='view quote']::text").extract_first(),
                'author': quote.css("a[title='view author']::text").extract_first(),
                'tags': quote.css("div.kw-box > a::text").extract()
            }