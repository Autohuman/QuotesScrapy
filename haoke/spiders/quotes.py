# -*- coding: utf-8 -*-
import scrapy
from haoke.items import haokeItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')
        for quote in quotes:
            item = haokeItem()
            text = quote.css('.text::text').extract_first()
            author = quote.css('.author::text').extract_first()
            tags = ''
            for x in quote.css('.tags .tag::text').extract():
                tags += x + ','
            item['text'] = text
            item['author'] = author
            item['tags'] = tags
            yield item

        next = response.css('body > div > div:nth-child(2) > div.col-md-8 > nav > ul > li.next > a::attr(href)').extract_first()
        url = response.urljoin(next)
        yield scrapy.Request(url=url, callback=self.parse)