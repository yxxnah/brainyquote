import scrapy
import time
from selenium import webdriver as wd

class ToScrapeCSSSpider(scrapy.Spider):
    name = "toscrape-css"
    start_urls = [
        'https://www.brainyquote.com/topics/life-quotes',
    ]

    def __init__(self):
        # init browser with Selenium chrome driver here
        scrapy.Spider.__init__(self)
        self.browser = wd.Chrome(executable_path='/Users/seoyoonah/brainyquote/brainyquote/brainyquote/spiders/chromedriver')

    def parse(self, response):
        # load page on Selenium
        self.browser.get(response.url)
        self.browser.implicitly_wait(5)

        # Setting infinite scrolling
        seen = set()
        LIMIT_OF_RESULTS = 100

        # Get scroll height
        last_height = self.browser.execute_script("return document.body.scrollHeight")
        print('last height:', last_height)

        while len(seen) < LIMIT_OF_RESULTS:
            html = self.browser.find_element_by_xpath("//*").get_attribute('outerHTML')
            selector = scrapy.Selector(text=html)

            for quote in selector.css("div[id^='qpos']"):
                text = quote.css("a[title='view quote']::text").extract_first(),
                author = quote.css("a[title='view author']::text").extract_first(),
                tags = quote.css("div.kw-box > a::text").extract()

                if text not in seen:
                    seen.add(text)
                    yield {
                        'text' : text,
                        'author' : author,
                        'tags' : tags
                    }

            # scroll down to bottom
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            # Wait to load page
            time.sleep(3)
            # Calculate new scroll height and compare with last scroll height
            new_height = self.browser.execute_script("return document.body.scrollHeight")
            print('new height:', new_height, 'last height:', last_height)
            if new_height == last_height:
                print("the end of document")
                break
            last_height = new_height
            print("seen : ", len(seen))