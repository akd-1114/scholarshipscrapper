import scrapy


class ScholarshipSpider(scrapy.Spider):
    name = 'scholarship'
    allowed_domains = ['www.scholarshipportal.com']
    start_urls = ['https://www.scholarshipportal.com/scholarships/india']

    def parse(self, response):
        for list in response.xpath('//a[@class="scholarship scholarship__type--list"]'):
            link = response.urljoin(list.xpath('.//@href').get())

            yield scrapy.Request(url=link, callback=self.parse_link)

        next_page_shortlink = response.xpath(
            '//a[@rel="next"]/@href').get()
        next_page = response.urljoin(next_page_shortlink)

        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_link(self, response):
        yield {
            'Name': response.xpath('.//h1/text()').get(),
            'for': response.xpath('.//ul/li[1]/span/text()').get(),
            'deadline': response.xpath('.//ul/li[3]/span/text()').get(),
            'link': response.xpath('//a[@rel="nofollow noopener"]/@href').get()
        }
