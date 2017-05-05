# Only crawl event news from this page

import scrapy

from scrapy import Spider
from scrapy.selector import Selector
from MySpider.items import NewsItem

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class DantriSpider(Spider):
    name = "dantri"
    allowed_domains = ["dantri.com.vn"]
    start_urls = [
        "http://dantri.com.vn",
    ]

    def parse(self, response):
        articles = Selector(response).css('.noibattrangchu h2 a')

        for article in articles:
            item = NewsItem()
            item['title'] = article.css('::text').extract_first()
            item['url'] = article.xpath('::attr(href)').extract_first()

            article_page = item['url']
            if article_page is not None:
                article_page = response.urljoin(article_page)
                request = scrapy.Request(article_page, callback=self.__parse_content, errback=self.errback_tinhte)
                request.meta['item'] = item
            yield request

    def __parse_content(self, response):
        item = response.meta['item']
        content = Selector(response).css('#divNewsContent').extract_first()
        item['content'] = content

    def errback_tinhte(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)