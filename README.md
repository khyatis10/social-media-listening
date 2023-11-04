# social-media-listening

# Scrapy Project: Autoportal Spider

## Description
This Scrapy project is designed to scrape review data from the Autoportal website for specific car models. The spider visits the section of the website and collects review data for the car models.

## Files Used
- .scrapy/ (Scrapy cache and metadata files)
    - httpcache/ (HTTP request/response cache)
        - Autoportal/ (Autoportal-specific cache)
            - meta (metadata file)
            - pickled_meta (pickled metadata)
            - request_body (HTTP request body)
            - request_headers (HTTP request headers)
            - response_body (HTTP response body)
            - response_headers (HTTP response headers)
    - spiders/ (Scrapy spider files)
        - __init__.py (Initialization script)
        - items.py (Item definitions)
        - middlewares.py (Scrapy middlewares)
        - pipelines.py (Item pipelines)
        - settings.py (Scrapy settings)

## Scrapy Structure
- AutoportalSpider is the main Scrapy spider responsible for crawling the website and extracting review data.
- scrape_reviews method collects review data for a specific car model and page number.
- parse_reviews method is the callback function for processing review data from a page.
- clean_data method cleans and processes the collected review data.
- save_data method saves the cleaned data to a file (customize as needed).
- clean_html function removes HTML tags from the text data.
- clean_reviews_text function cleans the review text data.
- The spider is configured to start with the URL 'https://autoportal.com/newcars/' and crawl specific car models.

## Usage
1. Ensure you have Scrapy installed. If not, install it using pip install scrapy.
2. Place this project in your preferred directory.
3. Customize the data saving mechanism in the save_data method.
4. Run the spider by executing `scrapy crawl Autoportal` in the project directory.

## Note:
You might have to add some keys or make changes in settings.py if there is problem crawling website. You might need ethical permissions to crawl through website. 
