import scrapy
import pandas as pd
import re
from time import sleep
from random import randint

class AutoportalSpider(scrapy.Spider):
    name = "Autoportal"
    start_urls = ['https://autoportal.com/newcars/mahindra/']
    
    def parse(self, response):
        urls = ['xuv-300', 'thar']
        for url in urls:
            reviews_list = scrape_reviews(self, url)
            cleaned_reviews, cleaned_ratings = clean_data(reviews_list)
            save_data(url, cleaned_reviews, cleaned_ratings)

    def scrape_reviews(self, url):
        reviews_list = []
        base_url = 'https://autoportal.com/newcars/mahindra/'

        #iterating over all pages in website
        for page in range(1, 12):
            page_url = f"{base_url}{url}/reviews/page/{page}/" if page > 1 else f"{base_url}{url}/reviews/"
            yield scrapy.Request(url=page_url, callback=self.parse_reviews, meta={'reviews_list': reviews_list})

    def parse_reviews(self, response):
        # below extracting data using CSS elements 
        reviews_list = response.meta['reviews_list']
        reviews = response.css('div.model-reviews__item-desc::text').extract()
        reviews_list.extend(reviews)
        print(f"Reviews on Page {response.url}: {len(reviews)}")
        sleep(randint(2, 10))
        yield {'reviews_list': reviews_list}

    def clean_data(self, reviews_list):
        # cleaning data to remove any expression which hinders text quality.
        cleaned_reviews = ' '.join(map(str, reviews_list))
        cleaned_reviews = clean_html(cleaned_reviews)
        cleaned_reviews = clean_reviews_text(cleaned_reviews)

        return cleaned_reviews

    def save_data(self, url, cleaned_reviews, cleaned_ratings):
        # Can Customize this part to save data as prefered (e.g., to CSV files)
        
        with open(f'/Social Media Listening/tutorial/autoportal_reviews_{url}.txt', "w", encoding="utf-8") as text_file:
            text_file.write(cleaned_reviews)

def clean_html(text):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    return re.sub(cleanr, '', text)

def clean_reviews_text(text):
    text = text.replace('] [\n', ', \n')
    text = text.replace('... Read\xa0More »', '')
    text = text.replace('\n\n', '  ')
    text = text.replace('[\n', '  ')
    return text

if __name__ == "__main__":
    from scrapy.crawler import CrawlerProcess

    process = CrawlerProcess()
    process.crawl(AutoportalSpider)
    process.start()


