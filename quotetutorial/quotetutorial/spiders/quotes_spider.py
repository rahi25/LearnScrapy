import scrapy


class QuoteSpider(scrapy.Spider):
    # define variable and it is important to write them exactly
    name = 'quotes'
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    def parse(self, response):
        title = response.css('title::text').extract()
        yield {'titletext': title}
