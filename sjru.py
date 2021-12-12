import scrapy
from scrapy.http import HtmlResponse
from laraparser.items import LaraparserItem


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bt%5D%5B0%5D=4',
                  'https://spb.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@class="icMQ_ bs_sM _3ze9n _1M2AW f-test-button-dalshe f-test-link-Dalshe"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//div[@class="jNMYr GPKTZ _1tH7S"]/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.xpath('//h1//text()').get()
        salary = response.xpath('//span[@class="_1OuF_ ZON4b"]//text()').getall()
        url = response.url
        yield LaraparserItem(name=name, salary=salary, url=url)
