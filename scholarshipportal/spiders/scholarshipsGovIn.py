import scrapy
from urllib.parse import urljoin

class ScholarshipsGovInSpider(scrapy.Spider):
    name = 'scholarships.gov.in'
    allowed_domains = ['scholarships.gov.in']
    start_urls = ['http://scholarships.gov.in/']

    def parse(self, response):
        
        # tab where data to scrape is present
        main_tab_id = 'TabbedPanels1'

        # set of tab headers eg: central, state, ug.
        tab_header_class = 'TabbedPanelsTabGroup'

        # set of actual scholarship schemes information
        tab_content_class = 'TabbedPanelsContentGroup'

        # iterators for central and ug schemes
        itr_header = response.xpath(f'//div[@id="{main_tab_id}"]/ul[@class="{tab_header_class}"]')
        itr_content = response.xpath(f'//div[@id="{main_tab_id}"]/div[@class="{tab_content_class}"]')

        for _, content in zip(itr_header.xpath('li/text()'), itr_content.xpath('div[@class="TabbedPanelsContent"]')):
            
            # scraping only these schemes -> ['Central Schemes', 'State Schemes', 'UGC / AICTE Schemes']
            # iterate actual schemes
            for schema_grp_name, schemes in zip(content.xpath('button/text()'), content.xpath('div[@class="panel"]')):

                # iterate over scheme_grp, may contain two or three or more schemes
                for scheme_name, deadline, link  in zip(
                    schemes.xpath('div[@class="col-md-5"][position() > 1]/text()'),
                    schemes.xpath('div[@class="col-md-2"][position() mod 3 = 0]/text()'),
                    schemes.xpath('//a[contains(@href, "schemeGuidelines")]/@href'),
                ):
                    yield {
                        'name': schema_grp_name.get().strip(),
                        'for': scheme_name.get().strip(),
                        'deadline': deadline.get().replace('Closed on ', '').strip(),
                        'link': urljoin(self.start_urls[0], link.get())
                    }