# -*- coding: utf-8 -*-
from scrapy import Spider, Request

class IndeedSpider(Spider):
    name = 'indeed'
    allowed_domains = ['indeed.com']

    def __init__(self, job='developer', *args, **kwargs):
        super(IndeedSpider, self).__init__(*args, **kwargs)

        job = clean_job_string(job)
        self.start_urls = [f'https://www.indeed.com/jobs?q={job}&l=&sort=date']

    def parse(self, response):
        
        links = response.xpath('//a[@class="turnstileLink"]/@href').extract()

        for link in links:
            if 'company' not in link:
                absolute_link = response.urljoin(link)
                yield Request(absolute_link, callback=self.parse_job_offer)

        if not 'start' in response.url:
            link = response.url + '&start=10'
        else:
            link_first, link_second = response.url.split('&start=')
            link_second = int(link_second) + 10
            link = f'{link_first}&start={link_second}'
             
        yield Request(link, callback=self.parse)
        

    def parse_job_offer(self, response):
        title = response.xpath('//h3[contains(@class, "JobInfoHeader-title")]/text()').extract_first()
        company = response.xpath('//*[contains(@class, "InlineCompanyRating")]/div/text()').extract()[0]
        company_rating = response.xpath('//meta[@itemprop="ratingValue"]/@content').extract_first()
        if not company_rating:
            company_rating = 'This company does not have a rating'
        else:
            company_rating = round(float(company_rating), 4)
            
        city = response.xpath('//*[contains(@class, "InlineCompanyRating")]/div/text()').extract()[2]
        job_url = response.url

        yield {
            'title': title,
            'company': company,
            'company_rating': company_rating,
            'city': city,
            'job_url': job_url,
        }

# Helper functions

# Cleans the job string passed as an argument
def clean_job_string(job_string):
    job_string = job_string.strip()
    job_string = job_string.replace(' ','+')
    return job_string