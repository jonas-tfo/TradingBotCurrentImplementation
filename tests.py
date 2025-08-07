import requests
import os
from typing import List, Dict, Optional
import requests
import re
from collections import defaultdict
from google import genai
import time
import yfinance as yf
from ib_insync import *
from datetime import datetime, timedelta, timezone, date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
import json
import pandas_datareader.data as pdr


# Renamed function slightly for clarity
def get_latest_marketaux_news_with_snippet(
    api_token: str,
    limit: int = 10,
    symbols: Optional[List[str]] = None,
    language: Optional[str] = 'en'
) -> Optional[List[Dict]]:
    """
    Retrieves the latest news articles, including snippets provided by Marketaux.

    Note: This function retrieves the content snippet/summary provided directly
    by the Marketaux API. It does *not* scrape the full article text from
    the source websites due to technical and legal complexities.

    Args:
        api_token: Your Marketaux API token.
        limit: The maximum number of news articles to return (default: 10).
        symbols: Optional list of stock symbols to filter news by.
        language: Optional language filter (default: 'en').

    Returns:
        A list of news article dictionaries (including title, url, snippet, etc.),
        or None if an error occurs.
    """
    base_url = "https://api.marketaux.com/v1/news/all"
    params = {
        'api_token': api_token,
        'sort': 'published_on', # Ensure latest first
        'limit': limit,
        # Consider adding 'filter_entities=true' if you only want articles
        # where Marketaux identified stock symbols within the text.
        # 'filter_entities': 'true'
    }

    if symbols:
        params['symbols'] = ','.join(symbols)
    if language:
        params['language'] = language

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status() # Check for HTTP errors

        data = response.json()
        # Return the list of article objects from the 'data' key
        return data.get('data', [])

    except requests.exceptions.RequestException as e:
        print(f"Error fetching news from Marketaux API: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
    


def get_articles_stocktitan_latest(url) -> list:
    try:
        # Set up Selenium with Chrome
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless=new")  # Run headless
        chrome_options.add_argument("--remote-debugging-port=9222")

        # Install matching chromedriver
        chromedriver_autoinstaller.install()

        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print("Driver initialization failed:", e)
        return []

    try:
        # Load the page
        driver.get(url)
        driver.implicitly_wait(40)

        # Extract page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all articles
        articles_data = []
        article_headlines_with_href = soup.find_all('a', class_='text-gray-dark feed-link', href=True)
        if not article_headlines_with_href:
            print("No articles found on the page.")
            return []

        for article_headline in article_headlines_with_href:
            try:
                # Find the article link
                link_tag = article_headline['href']
                if link_tag:
                    article_url = "https://www.stocktitan.net" + link_tag
                    headline_text = article_headline.text.strip()

                    if headline_text and article_url:
                        articles_data.append({'headline': headline_text, 'url': article_url})
     

            except Exception as e:
                print("Error processing an article element:", e)
                continue

        if not articles_data:
            print("No articles found.")
            return []

        # Scrape article content
        full_articles = []
        for item in articles_data[:3]:  # Limit to 15 articles
            try:
                driver.get(item['url'])
                driver.implicitly_wait(20)
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Find the main content div (update if needed)
                content_div = soup.find('article', class_='article')
                if content_div:
                    paragraphs = content_div.find_all('p')
                    article_text = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                else:
                    article_text = "Content not found."

                full_articles.append({
                    'headline': item['headline'],
                    'url': item['url'],
                    'content': article_text
                })
                 
                time.sleep(2) # be nice to server
                

            except Exception as e:
                print(f"Error scraping {item['url']}: {e}")
                
        print(full_articles)
        return full_articles

    except Exception as e:
        print("General error scraping finanzen:", e)
        return []
    finally:
        driver.quit()



# --- Example Usage ---
if __name__ == "__main__":

    articles = get_articles_stocktitan_latest("https://www.stocktitan.net/news/live.html")