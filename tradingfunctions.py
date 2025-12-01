import requests
import re
from collections import defaultdict
from mistralai import Mistral
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
import random
from dotenv import load_dotenv
import os

sp500_tickers = [
    'MMM', 'AOS', 'ABT', 'ABBV', 'ACN', 'ATVI', 'ADM', 'ADBE', 'ADP', 'AAP', 'AES', 'AFL',
    'A', 'APD', 'AKAM', 'ALK', 'ALB', 'ARE', 'ALGN', 'ALLE', 'LNT', 'ALL', 'GOOGL', 'GOOG',
    'MO', 'AMZN', 'AMCR', 'AMD', 'AEE', 'AAL', 'AEP', 'AXP', 'AIG', 'AMT', 'AWK', 'AMP',
    'ABC', 'AME', 'AMGN', 'APH', 'ADI', 'ANSS', 'AON', 'APA', 'AAPL', 'AMAT', 'APTV', 'ANET',
    'AJG', 'AIZ', 'T', 'ATO', 'ADSK', 'AZO', 'AVB', 'AVY', 'AXON', 'BKR', 'BALL', 'BAC',
    'BBWI', 'BAX', 'BDX', 'WRB', 'BRK.B', 'BBY', 'BIO', 'TECH', 'BIIB', 'BLK', 'BK', 'BA',
    'BKNG', 'BWA', 'BXP', 'BSX', 'BMY', 'AVGO', 'BR', 'BRO', 'BF.B', 'BG', 'CHRW', 'CDNS',
    'CZR', 'CPT', 'CPB', 'COF', 'CAH', 'KMX', 'CCL', 'CARR', 'CTLT', 'CAT', 'CBOE', 'CBRE',
    'CDW', 'CE', 'CNC', 'CNP', 'CDAY', 'CF', 'CRL', 'SCHW', 'CHTR', 'CVX', 'CMG', 'CB',
    'CHD', 'CI', 'CINF', 'CTAS', 'CSCO', 'C', 'CFG', 'CLX', 'CME', 'CMS', 'KO', 'CTSH',
    'CL', 'CMCSA', 'CMA', 'CAG', 'COP', 'ED', 'STZ', 'CEG', 'COO', 'CPRT', 'GLW', 'CTVA',
    'CSGP', 'COST', 'CTRA', 'CCI', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DE',
    'DAL', 'XRAY', 'DVN', 'DXCM', 'FANG', 'DLR', 'DFS', 'DIS', 'DG', 'DLTR', 'D', 'DPZ',
    'DOV', 'DOW', 'DTE', 'DUK', 'DD', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EW', 'EA',
    'ELV', 'LLY', 'EMR', 'ENPH', 'ETR', 'EOG', 'EPAM', 'EQT', 'EFX', 'EQIX', 'EQR', 'ESS',
    'EL', 'ETSY', 'RE', 'EVRG', 'ES', 'EXC', 'EXPE', 'EXPD', 'EXR', 'XOM', 'FFIV', 'FDS',
    'FICO', 'FAST', 'FRT', 'FDX', 'FITB', 'FRC', 'FE', 'FIS', 'FISV', 'FLT', 'FMC', 'F',
    'FTNT', 'FTV', 'FOXA', 'FOX', 'BEN', 'FCX', 'GRMN', 'IT', 'GEHC', 'GEN', 'GNRC', 'GD',
    'GE', 'GIS', 'GM', 'GPC', 'GILD', 'GL', 'GPN', 'GS', 'HAL', 'HBI', 'HAS', 'HCA', 'PEAK',
    'HSIC', 'HSY', 'HES', 'HPE', 'HLT', 'HOLX', 'HD', 'HON', 'HRL', 'HST', 'HWM', 'HPQ',
    'HUM', 'HBAN', 'HII', 'IBM', 'IEX', 'IDXX', 'ITW', 'ILMN', 'INCY', 'IR', 'PODD', 'INTC',
    'ICE', 'IFF', 'IP', 'IPG', 'INTU', 'ISRG', 'IVZ', 'INVH', 'IQV', 'IRM', 'JBHT', 'JKHY',
    'J', 'JNJ', 'JCI', 'JPM', 'JNPR', 'K', 'KDP', 'KEY', 'KEYS', 'KMB', 'KIM', 'KMI', 'KLAC',
    'KHC', 'KR', 'LHX', 'LH', 'LRCX', 'LW', 'LVS', 'LDOS', 'LEN', 'LNC', 'LIN', 'LYV', 'LKQ',
    'LMT', 'L', 'LOW', 'LUMN', 'LYB', 'MTB', 'MRO', 'MPC', 'MKTX', 'MAR', 'MMC', 'MLM', 'MAS',
    'MA', 'MTCH', 'MKC', 'MCD', 'MCK', 'MDT', 'MRK', 'META', 'MET', 'MTD', 'MGM', 'MCHP', 'MU',
    'MSFT', 'MAA', 'MRNA', 'MHK', 'MOH', 'TAP', 'MDLZ', 'MPWR', 'MNST', 'MCO', 'MS', 'MOS',
    'MSI', 'MSCI', 'NDAQ', 'NTAP', 'NFLX', 'NWL', 'NEM', 'NWSA', 'NWS', 'NEE', 'NKE', 'NI',
    'NDSN', 'NSC', 'NTRS', 'NOC', 'NCLH', 'NRG', 'NUE', 'NVDA', 'NVR', 'NXPI', 'ORLY', 'OXY',
    'ODFL', 'OMC', 'ON', 'OKE', 'ORCL', 'OGN', 'OTIS', 'PCAR', 'PKG', 'PARA', 'PH', 'PAYX',
    'PAYC', 'PYPL', 'PNR', 'PEP', 'PKI', 'PFE', 'PCG', 'PM', 'PSX', 'PNW', 'PXD', 'PNC',
    'POOL', 'PPG', 'PPL', 'PFG', 'PG', 'PGR', 'PLD', 'PRU', 'PEG', 'PTC', 'PSA', 'PHM',
    'QRVO', 'PWR', 'QCOM', 'DGX', 'RL', 'RJF', 'RTX', 'O', 'REG', 'REGN', 'RF', 'RSG',
    'RMD', 'RHI', 'ROK', 'ROL', 'ROP', 'ROST', 'RCL', 'SPGI', 'CRM', 'SBAC', 'SLB', 'STX',
    'SEE', 'SRE', 'NOW', 'SHW', 'SPG', 'SWKS', 'SJM', 'SNA', 'SEDG', 'SO', 'LUV', 'SWK',
    'SBUX', 'STT', 'STE', 'SYK', 'SYF', 'SNPS', 'SYY', 'TMUS', 'TROW', 'TTWO', 'TPR',
    'TRGP', 'TGT', 'TEL', 'TDY', 'TFX', 'TER', 'TSLA', 'TXN', 'TXT', 'TMO', 'TJX', 'TSCO',
    'TT', 'TDG', 'TRV', 'TRMB', 'TFC', 'TYL', 'TSN', 'USB', 'UDR', 'ULTA', 'UNP', 'UAL',
    'UPS', 'URI', 'UNH', 'UHS', 'VLO', 'VTR', 'VRSN', 'VRSK', 'VZ', 'VRTX', 'VFC', 'VTRS',
    'VICI', 'V', 'VMC', 'WAB', 'WBA', 'WMT', 'WBD', 'WM', 'WAT', 'WEC', 'WFC', 'WELL',
    'WST', 'WDC', 'WRK', 'WY', 'WHR', 'WMB', 'WTW', 'GWW', 'WYNN', 'XEL', 'XYL', 'YUM',
    'ZBRA', 'ZBH', 'ZION', 'ZTS', "MBLY", "DELL"
]

# Expanded lists of German stocks from various indices

dax40_tickers = [
    "ADS", "AIR", "ALV", "BAS", "BAYN", "BEI", "BMW", "BNR", "CON", "DHER",
    "DTG", "DTE", "EOAN", "FME", "FRE", "HEN3", "HEI", "HFG", "IFX", "LEG",
    "LIN", "MRK", "MTX", "MUV2", "PAH3", "PBB", "PUM", "QIA", "RHM", "RWE",
    "SAP", "SART", "SIE", "SY1", "TKA", "VNA", "VOW3", "VOW", "ZAL", "TUI1",
    "P911"
]

sdax_tickers = [
    "AIXA", "ASIZ", "BNHL", "CELA", "COS", "DELG", "DIC", "ESEG", "FREN", "GESA",
    "HNR", "IGL", "KRON", "LEIW", "MANU", "NEUB", "ODXA", "PRIA", "QANT", "RABA", "AFX"
]

mdax_tickers = [
    "ALDI", "BAIN", "CUNA", "DIFO", "ELOX", "FIRE", "GOMA", "HUMA", "IVIA", "JUMO",
    "KUKA", "LUBA", "MIRA", "NEUM", "OPTB", "PUMA", "QUEN", "ROTI", "SONN", "TROX"
]

tecdax_tickers = [
    "ANDI", "BRAU", "CONX", "DANU", "EPEX", "FONI", "GRAV", "HOF", "INTU", "JAZZ",
    "KIWI", "LEON", "MANTA", "NEXO", "ORIX", "PEGA", "QUAD", "RADI", "SIMO", "TECH"
]

german_tickers = dax40_tickers + sdax_tickers + mdax_tickers + tecdax_tickers


load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
MARKETAUX_API_KEY = os.getenv("MARKETAUX_API_KEY")



US_EXCHANGES = ['NYQ', 'NMS', 'ASE', 'AMEX', 'OTC', 'TSX', 'NASDAQ', 'NYSE', 'BATS', 'ARCA', 'NEO', 'NCM', 'PCX', 'PNK', 'CBOE', 'CSE', 'OTCBB', 'OTCQB', 'OTCQX', 'BVC', 'CNSX', 'NEO', 'TSXV', 'TSX', 'NGM', 'SMART']
EUROPEAN_EXCHANGES = ['LSE', 'FRA', 'AMS', 'MC', 'SWX', 'GER', 'XETRA', 'BME', 'STO', 'ICE', 'ASX', 'HKEX', 'NSE', 'TSE', 'SSE', 'JSE', 'BSE', 'KRX', 'TWSE', 'SGX', 'IDX', 'SET', 'MYX', 'PSE', 'HOSE', 'HNX', 'KASE', 'TASE', 'BCBA', 'BVMF', 'BMV', 'BVC', 'BVLP', 'BVL', 'IBIS']


mistral_client = Mistral(api_key=MISTRAL_API_KEY)

mistral_model = "mistral-small-latest"

"""
Functions to retrieve articles via API/webscraping
"""

# from alpha vantage
def get_articles():
    
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "apikey": ALPHA_VANTAGE_API_KEY
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        print("Successfully got news")
    except requests.RequestException as e:
        print(f"Failed to fetch news from Alpha Vantage: {e}")
        return []
    
    if "feed" in data:
        return data["feed"]
    else:
        print("API response limit reached")
        return []



def get_articles_finanznachrichten(url) -> list:
    driver = None
    try:
        # Set up Selenium with Chrome
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")  
        chrome_options.add_argument("--headless=new")  # doesnt open a window when scraping

        # Install matching chromedriver
        chromedriver_autoinstaller.install()

        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(20)  # Add timeout for page loads
    except Exception as e:
        print("Driver failed:", e)
        if driver:
            driver.quit()
        return []

    try:
        # Fetch the main page
        try:
            driver.get(url)
            driver.implicitly_wait(10)  # Wait for page to load
        except Exception as e:
            print(f"Error loading main page {url}: {e}")
            driver.quit()
            return []

        # Find article links
        article_links_aufFn = driver.find_elements(By.CLASS_NAME, 'nT.aufFn')
        article_links_extern = driver.find_elements(By.CSS_SELECTOR, '.nT.extern.href.cursor_pointer')
        # testing without external links, seem to not be able to be accessed anyway
        article_links = article_links_aufFn 

        # Extract headline text and URLs
        articles_data = []
        for link in article_links:
            try:
                headline_text = link.text.strip()
                article_url = link.get_attribute('href')
                if headline_text and article_url:
                    articles_data.append({'headline': headline_text, 'url': article_url})
            except Exception as e:
                print(f"Error processing link: {e}")
                continue

        if not articles_data:
            print(f"No articles found at {url}")
            return []

        # Scrape article content
        full_articles = []
        for item in articles_data[:15]:  # Limit to 15 articles
            try:
                # Set a timeout for loading each article
                driver.set_page_load_timeout(10)
                driver.get(item['url'])
                driver.implicitly_wait(5)
                
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                content_div = soup.find('div', id='artikelTextPuffer')

                if content_div:
                    paragraphs = content_div.find_all('p')
                    article_text = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                    
                    if article_text:  # Only add if we got actual content
                        full_articles.append({
                            'headline': item['headline'],
                            'url': item['url'],
                            'content': article_text
                        })
                        print(f"Successfully scraped: {item['headline']}")
                    else:
                        print(f"No content found for article: {item['headline']}, using headline for scoring")
                        full_articles.append({
                            'headline': item['headline'],
                            'url': item['url'],
                            'content': ""
                        })
                        
                time.sleep(1)  # Reduced sleep time
                
            except Exception as e:
                print(f"Error scraping article {item['url']}: {e}")
                continue  # Skip to next article on error

        # Process successful articles
        articles = []
        for article in full_articles:
            if article.get('content'):  # Only include articles with content
                articles.append(article['headline'] + ' ' + article['content'])

        return articles

    except Exception as e:
        print(f"General error in get_articles_finanznachrichten: {e}")
        return []
        
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass  


def get_articles_cnbc_latest(url) -> list:

    try:
        # Set up Selenium with Chrome
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument("--headless=new")  # doesnt open a window when scraping

        # Install matching chromedriver
        chromedriver_autoinstaller.install()

        # Initialize the driver
        driver = webdriver.Chrome(options=chrome_options)
    except Exception as e:
        print("Driver failed:", e)
        return []

    try:
        # Fetch the main page
        try:
            driver.set_page_load_timeout(15)
            driver.get(url)
            driver.implicitly_wait(10)  # Wait for page to load
        except Exception as e:
            print(f"Error loading page {url}: {e}")
            driver.quit()
            return []

        # Find article link elements with class truncate
        article_links_headline = driver.find_elements(By.CLASS_NAME, "LatestNews-headline")
        article_links_dates = driver.find_elements(By.CLASS_NAME, "LatestNews-timestamp")

        article_links = []

        for i in range(len(article_links_headline)):
            # Extract the number from the "Xm" format and convert to int
            if "HOUR" in article_links_dates[i].text:
                break
            minutes = int(article_links_dates[i].text.strip(" MIN AGO"))
            if minutes <= 30:
                article_links.append(article_links_headline[i]) 

        # Extract headline text and URLs
        articles_data = []

        for link in article_links:
            try:
                headline_text = link.text.strip()
                article_url = link.get_attribute('href')
                if headline_text and article_url:
                    articles_data.append({'headline': headline_text, 'url': article_url})
            except Exception as e:
                print(f"Error processing link at {url}: {e}")
                continue

        # Check if we found any articles
        if not articles_data:
            print(f"No articles found with the specified classes at {url}.")
            driver.quit()
            return []

        # Scrape article content from each URL
        full_articles = []
        for item in articles_data[:15]:  # Limit to 15 articles per page
            try:
                driver.set_page_load_timeout(10)
                driver.get(item['url'])
                driver.implicitly_wait(5)
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                
                # Directly find the div with id="artikelTextPuffer"
                content_div = soup.find('div', id='RegularArticle-ArticleBody-5')

                if content_div:
                    # Extract all <p> tags within the content div
                    paragraphs = content_div.find_all('p')
                    article_text = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
                else:
                    article_text = "Content not found."

                full_articles.append({
                    'headline': item['headline'],
                    'url': item['url'],
                    'content': article_text
                })
                print(f"Scraped: {item['headline']}")
                time.sleep(2)  # Be polite to the server
            except Exception as e:
                print(f"Error scraping {item['url']}: {e}")
                full_articles.append({
                    'headline': item['headline'],
                    'content': f"Error: {e}"
                })

        # For each article in full_articles, concatenate the headline and content
        articles = []
        for article in full_articles:
            articles.append(article['headline'] + ' ' + article['content'])

        return articles

    except Exception as e:
        print(f"General error cnbc articles from {url}: {e}")
        return []
    finally:
        driver.quit()



def get_articles_finanzen_latest(url) -> list:
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
        # Load the page with timeout
        driver.set_page_load_timeout(15)
        driver.get(url)
        driver.implicitly_wait(10)

        # Extract page source and parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Find all articles
        articles_data = []
        article_elements = soup.find_all('div', class_='article-layout')


        for article in article_elements:
            try:
                # Find the article link
                link_tag = article.find('a', class_='article-teaser')
                
                if link_tag:
                    article_url = "https://www.finanzen.net" + link_tag['href']
                    headline_text = link_tag.text.strip()

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
        for item in articles_data:  # Limit to 15 articles
            try:
                driver.set_page_load_timeout(10)
                driver.get(item['url'])
                driver.implicitly_wait(5)
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # Find the main content div (update if needed)
                content_div = soup.find('div', class_='news-container__text')
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
                

        return full_articles

    except Exception as e:
        print("General error scraping finanzen:", e)
        return []
    finally:
        driver.quit()


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
        # Load the page with timeout
        driver.set_page_load_timeout(15)
        driver.get(url)
        driver.implicitly_wait(10)

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
        for item in articles_data[:5]:
            try:
                driver.set_page_load_timeout(10)
                driver.get(item['url'])
                driver.implicitly_wait(10)
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
                
        return full_articles

    except Exception as e:
        print("General error scraping finanzen:", e)
        return []
    finally:
        driver.quit()


"""
Functions to generate scores from articles and parse them 
"""

# used as fallback if ticker extraction from json is unsuccessful, used only for alpha vantage news
def extract_stock_symbols(text) -> list:
    pattern = r'\b(?:\$?([A-Z]{1,5}(?:\.[A-Z]{1,2})?))\b'
    matches = re.findall(pattern, text)
    return list(set(matches))


# gets score from 0 to 100 for stocks based on article content, mentioned stocks must be given
def get_scores_from_llm(article_text, stocks) -> str:

    prompt = (
        f"""
        Analyze the following article and provide a score from 0 to 100 for each of the mentioned stocks: {', '.join(stocks)}.

        The score should indicate the likely impact on the stock's trend based solely on the article's content, where 0 means a strong downtrend and 100 means a strong uptrend. 
        A score below or equal to 50 should signify that selling is preferable over buying, while a score above 50 should indicate a preference for buying over selling.

        When assigning scores, consider factors such as:
        - Mentions of new products, services, or innovations
        - Financial performance indicators (e.g., revenue, profit, growth)
        - Market trends and competitive landscape
        - Regulatory changes or legal issues 
        - Management changes or corporate governance
        - Any other events or news that could affect the stock's value

        Evaluate each stock individually based on how it is portrayed in the article. For example:
        - If the article discusses a company's strong earnings report, the score should be high (e.g., 80-100).
        - If the article highlights a new partnership or product launch, the score should be moderate (e.g., 40-60).
        - If the article mentions a decline in sales, a negative market sentiment or a weak earnings report, the score should be low (e.g., 0-20).
        - If the article mentions a lawsuit against a company, the score should be low (e.g., 0-20).
        - If the article is neutral or doesn't provide clear information about a stock's prospects, the score should be around 50.

        Do not base the scores on general knowledge about the stocks or their historical performance. Focus only on the information provided in the article.

        Provide the scores in the format: STOCK1: score1, STOCK2: score2, ..., with the assigned scores as integers. Do not provide any further explaination or text.

        Article:
        {article_text}
        """
    )
    try:
        response = mistral_client.chat.complete(
            model=mistral_model,
            messages=[{"role": "user", "content": prompt}]
        )
        time.sleep(5)
        response_text = response.choices[0].message.content
        print("Got response for article:", response_text)
        return response_text
    except Exception as e:
        print(f"Mistral API error: {e}")
        time.sleep(5)
        return ""


# gets score from 0 to 100 for stocks based on article content, also extracts mentioned stocks from article, without them being given
def get_scores_from_llm_global(article_text) -> str:

    prompt = (
    f"""
    Read the article below and assign a score (0-100) for each mentioned stock based solely on its content. 

    The score should indicate the likely impact on the stock's trend based solely on the article's content, where 0 means a strong downtrend and 100 means a strong uptrend. 
    A score below or equal to 50 should signify that selling is preferable over buying, while a score above 50 should indicate a preference for buying over selling.

    When assigning scores, consider factors such as:
    - Mentions of new products, services, or innovations
    - Financial performance indicators (e.g., revenue, profit, growth)
    - Market trends and competitive landscape
    - Regulatory changes or legal issues
    - Management changes or corporate governance
    - Any other events or news that could affect the stock's value

    Evaluate each stock individually based on how it is portrayed in the article. For example:
    - If the article discusses a company's strong earnings report, the score should be high (e.g., 80-100).
    - If the article highlights a new partnership or product launch, the score should be moderate (e.g., 40-60).
    - If the article mentions a decline in sales, a negative market sentiment or a weak earnings report, the score should be low (e.g., 0-20).
    - If the article mentions a lawsuit against a company, the score should be low (e.g., 0-20).
    - If the article is neutral or doesn't provide clear information about a stock's prospects, the score should be around 50.

    Do not base the scores on general knowledge about the stocks or their historical performance. Focus only on the information provided in the article.

    Provide the scores in the format: company name 1: score1, company name 2: score2, ..., with the assigned scores as integers. Do not provide additonal text or any additional explaination.

    Article:
    {article_text}
    """
    )

    try:
        response = mistral_client.chat.complete(
            model=mistral_model,
            messages=[{"role": "user", "content": prompt}]
        )
        time.sleep(5)
        response_text = response.choices[0].message.content
        print(f"Got response for article: {response_text}")
        return response_text
    except Exception as e:
        print(f"Mistral API error: {e}")
        time.sleep(5)
        return ""


# gets scores based on if short term or long term investment is better
def get_trade_term_scores_from_llm(article_text) -> str:
    prompt = (
        f"""
        Analyze the following article and provide a trade term score from 0 to 100 for each of the mentioned stocks.
        The score should indicate the recommended holding period: 0 means a very short-term trade (sell quickly) and 100 means a very long-term trade (hold for a long time).
        A score of between 90 and 100 should be given if there is no information available about the short term or long term development of the stock price, as a long term investment
        strategy is safer when less information is available. This is important in order to insure that the model does not recommend short term trades when there is no information available about the stock price development.
        A score below or equal to 50 should signify that a short-term trade is preferable over a long-term investment, while a score above about 70 should indicate a preference for a long-term investment over a short-term trade.
        When assigning scores, consider factors such as:
        - The article's discussion of the stock's future prospects
        - The expected duration of the stock's price movement
        - The article's analysis of the stock's long-term potential
        - The article's mention of short-term catalysts or events
        - Any other information that could affect the stock's price in the short or long term
        Note that not all of this information may be present in the article, and you should base your scores on the content provided.
        Provide the scores in the following format, without any explaination or additional text: companyname1: score, companyname2: score, ...
        Here are some examples for company names, when providing the scores, this is what the company name should be like: "Apple", "Nvidia", "Rheinmetall", "DHL", "Rewe"
        
        Article:
        {article_text}
        """
    )
    try:
        response = mistral_client.chat.complete(
            model=mistral_model,
            messages=[{"role": "user", "content": prompt}]
        )
        time.sleep(5)  # rate-limit safeguard
        response_text = response.choices[0].message.content
        print(f"Got response for article (trade term): {response_text}")
        return response_text
    except Exception as e:
        print(f"Mistral API error (trade term): {e}")
        time.sleep(5)
        return ""


# converts dict with comp name and score to dict with ticker and score
def get_ticker_trade_term_scores(company_name_scores) -> dict:
    
    ticker_scores = load_scores_from_json(filename="saved_term_scores.json")  # Load existing scores from the file
    
    for comp_name, score in company_name_scores.items():
        ticker = stock_ticker_from_company_name(comp_name)

        # Add German extension if applicable
        if not ticker.endswith(".DE") and ticker in german_tickers:
            ticker += ".DE"

        if ticker and ticker != "None":
            if ticker in ticker_scores:
                ticker_scores[ticker] = (ticker_scores[ticker] + score) / 2  # Averaging old and new scores
            else:
                ticker_scores[ticker] = score

    save_scores_to_json(stock_scores=ticker_scores, filename="saved_term_scores.json")  # Save updated scores back to the file
    return ticker_scores


# parses the score for each stock from the llm response 
def parse_ticker_scores(response) -> dict:
    try:
        scores = {}
        if not response:
            return scores
        # Try splitting on either comma or newline.
        items = re.split(r'[,\n]+', response)
        # Revised regex: match tickers that are 1-5 alphanumerics optionally followed by a dot and 1-2 alphanumerics
        pattern = r"([A-Z0-9]{1,5}(?:\.[A-Z0-9]{1,2})?)\s*:\s*(\d{1,3})"
        for item in items:
            match = re.search(pattern, item)
            if match:
                ticker = match.group(1)
                score = int(match.group(2))
                if 0 <= score <= 100:
                    scores[ticker] = score
        if not scores:
            print("Warning: No scores parsed from response.")
            return scores
        print("Parsed scores:", scores)
        return scores
    except Exception as e:
        print(f"Error while parsing scores {e}")
        return scores


# parses comp names from llm response
def parse_company_names_scores(response) -> dict:
    try:
        company_scores = {}
        if not response:
            return company_scores
        items = re.split(r'[,\n]+', response)
        # Regex pattern: capture company names (letters, numbers, spaces, common punctuation) then a colon and a score.
        pattern = r"([\w\s&\.\-]+)\s*:\s*(\d{1,3})"
        for item in items:
            match = re.search(pattern, item)
            if match:
                company = match.group(1).strip()
                score = int(match.group(2))
                if 0 <= score <= 100:
                    company_scores[company] = score
        if not company_scores:
            print("Warning: No company names parsed from response.")
        return company_scores
    except Exception as e:
        print(f"Error while parsing company names: {e}")
        return {}
    

# retrieves stock ticker from company name (with extension)
def stock_ticker_from_company_name(company_name: str) -> str:

    try:
        # Clean the company name
        company_name = company_name.strip()
        
        # Yahoo Finance search URL
        search_url = f"https://query1.finance.yahoo.com/v1/finance/search?q={company_name}&quotesCount=1&newsCount=0"
        
        # Set a user agent to avoid being blocked
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Make the request
        response = requests.get(search_url, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            
            # Extract the first ticker symbol from the search results
            if data.get('quotes') and len(data['quotes']) > 0:
                ticker = data['quotes'][0]['symbol']
                return ticker
            else:
                return "None"
        else:
            return f"Error: HTTP status code {response.status_code}"
            
    except Exception as e:
        return f"Error: {str(e)}"





"""
Final score and buy/sell amount getting functions
"""


# gets articles, generates scores with llm, gives average score for each stock
def get_final_scores_alpha():
    stock_scores = defaultdict(list)
    final_scores = {}

    # Get articles from the Alphavantage API
    articles = get_articles() 

    if not articles:
        print("No articles retrieved from Alphavantage.")
        return final_scores

    # Process Alpha Vantage articles
    for article in articles:
        print("Processing Alpha Vantage Article:")
        stocks = []

        title = article.get("title", "")
        summary = article.get("summary", "")
        article_text = f"{title}. {summary}"
        time_published_iso = article.get("time_published", "")
        
        # Skip old articles
        if time_published_iso:
            from datetime import timezone
            time_published = datetime.fromisoformat(time_published_iso.replace(' ', 'T')).replace(tzinfo=timezone.utc)
            time_diff_seconds = (datetime.now(timezone.utc) - time_published).total_seconds()
            if time_diff_seconds > 10800:  # Skip articles older than 3 hours
                print("Skipping old article")
                continue
        
        # Extract tickers from the API response
        tickers_sentiment = article.get("ticker_sentiment", [])
        if tickers_sentiment:
            for t in tickers_sentiment:
                if "ticker" in t:
                    stocks.append(t["ticker"])
                else:
                    temp_stocks = extract_stock_symbols(article_text)
                    stocks.extend(temp_stocks)
                    print("Using regex fallback for ticker extraction")
        else:
            # No ticker_sentiment provided, use fallback extraction
            stocks = extract_stock_symbols(article_text)
            print("No ticker_sentiment found; using fallback extraction:", stocks)
        
        # Generate scores for Alpha Vantage articles
        if stocks:
            response = get_scores_from_llm(article_text, stocks)
            scores = parse_ticker_scores(response)
            if scores:
                for stock, score in scores.items():
                    stock_scores[stock].append(score)
            else:
                print("No valid scores parsed for this article, assigning default score of 50 to each extracted stock.")
                for stock in stocks:
                    stock_scores[stock].append(50)
        else:
            print("No stocks extracted for this article.")
    
    # Calculate final average scores
    if not stock_scores:
        print("No scores were generated from any articles.")
        return final_scores

    # Average the lists of scores for each stock
    for stock, scores_list in stock_scores.items():
        if scores_list:
            final_scores[stock] = sum(scores_list) / len(scores_list)

    print("\nFinal averaged scores:")
    for stock, avg_score in final_scores.items():
        print(f"{stock}: {avg_score:.2f}")
    return final_scores



def get_final_scores_web_german() -> dict:

    stock_scores = defaultdict(list)
    final_scores = {}

     # Process global (euro) articles
    print("\nProcessing euro articles...")
    try:
        euro_articles = get_articles_finanznachrichten("https://www.finanznachrichten.de/nachrichten-index/dax-40.htm") + \
                        get_articles_finanznachrichten("https://www.finanznachrichten.de/nachrichten-index/sdax.htm") + \
                        get_articles_finanznachrichten("https://www.finanznachrichten.de/nachrichten-index/mdax-50.htm") + \
                        get_articles_finanznachrichten("https://www.finanznachrichten.de/nachrichten-index/tecdax.htm") + \
                        get_articles_finanzen_latest("https://www.finanzen.net/nachrichten/ressort/aktien")

    except Exception as e:
        print("Error retrieving euro articles:", e)
        
    print("Got all euro articles")
        
    print("Processing euro articles...")
    if not euro_articles:
        print("No euro articles found.")
        return final_scores
    
    for euro_article in euro_articles:
        try:
            # Get str LLM response for the article
            euro_comp_names_response = get_scores_from_llm_global(euro_article)
            # gets dict with company names and scores
            euro_comp_names_dict = parse_company_names_scores(euro_comp_names_response)

            print("LLM response (euro article):", euro_comp_names_response)
            
            # Convert company names to tickers and add scores to stock_scores
            for comp_name, score in euro_comp_names_dict.items():
                ticker = stock_ticker_from_company_name(comp_name)
                if ticker != "None":  # Only add valid tickers
                    stock_scores[ticker].append(score)
                    print(f"From euro articles -- Stock: {ticker} -- Score: {score}")
                else:
                    print(f"Ticker conversion failed for {comp_name}")
                    
        except Exception as e:
            print(f"Error processing a euro article: {e}")

    # Calculate final average scores
    if not stock_scores:
        print("No scores were generated from any articles.")
        return final_scores

    # Average the lists of scores for each stock
    for stock, scores_list in stock_scores.items():
        if scores_list:
            # Add .DE extension if not present
            if not stock.endswith('.DE') and stock in german_tickers:
                stock = stock + '.DE'
                
            final_scores[stock] = sum(scores_list) / len(scores_list)

    print("\nFinal averaged scores:")
    for stock, avg_score in final_scores.items():
        print(f"{stock}: {avg_score:.2f}")
    return final_scores



def get_final_scores_web_english() -> dict:

    stock_scores = defaultdict(list)
    final_scores = {}

     # Process global (euro) articles
    try:
        articles = get_articles_cnbc_latest("https://www.cnbc.com/") + \
                   get_articles_stocktitan_latest("https://www.stocktitan.net/news/live.html") 

    except Exception as e:
        print("Error retrieving english articles:", e)
        
        
    print("Processing english articles...")
    if not articles:
        print("No english articles found.")
        return final_scores
    
    for article in articles:
        try:
            # Get str LLM response for the article
            english_comp_names_response = get_scores_from_llm_global(article)
            # gets dict with company names and scores
            english_comp_names_dict = parse_company_names_scores(english_comp_names_response)

            print("LLM response (english article):", english_comp_names_response)
            
            # Convert company names to tickers and add scores to stock_scores
            for comp_name, score in english_comp_names_dict.items():
                ticker = stock_ticker_from_company_name(comp_name)
                if ticker != "None":  # Only add valid tickers
                    stock_scores[ticker].append(score)
                    print(f"From euro articles -- Stock: {ticker} -- Score: {score}")
                else:
                    print(f"Ticker conversion failed for {comp_name}")
                    
        except Exception as e:
            print(f"Error processing a euro article: {e}")

    # Calculate final average scores
    if not stock_scores:
        print("No scores were generated from any articles.")
        return final_scores

    # Average the lists of scores for each stock
    for stock, scores_list in stock_scores.items():
        if scores_list:
            final_scores[stock] = sum(scores_list) / len(scores_list)
    
    print("\nFinal averaged scores:")
    for stock, avg_score in final_scores.items():
        print(f"{stock}: {avg_score:.2f}")
    return final_scores



def get_all_trade_term_scores() -> dict:
    # Process trade term scores
    trade_term_scores_accum = {}
    term_articles = []

    # Fetch articles with individual error handling to prevent one failure from blocking everything
    print("Fetching Alpha Vantage articles...")
    try:
        alpha_articles = get_articles()
        print(f"Got {len(alpha_articles)} Alpha Vantage articles")
        term_articles.extend(alpha_articles)
    except Exception as e:
        print(f"Error fetching Alpha Vantage articles: {e}")

    print("Fetching DAX-40 articles...")
    try:
        dax_articles = get_articles_finanznachrichten("https://www.finanznachrichten.de/nachrichten-index/dax-40.htm")
        print(f"Got {len(dax_articles)} DAX-40 articles")
        term_articles.extend(dax_articles)
    except Exception as e:
        print(f"Error fetching DAX-40 articles: {e}")

    print("Fetching SDAX articles...")
    try:
        sdax_articles = get_articles_finanznachrichten("https://www.finanznachrichten.de/nachrichten-index/sdax.htm")
        print(f"Got {len(sdax_articles)} SDAX articles")
        term_articles.extend(sdax_articles)
    except Exception as e:
        print(f"Error fetching SDAX articles: {e}")

    print("Fetching MDAX articles...")
    try:
        mdax_articles = get_articles_finanznachrichten("https://www.finanznachrichten.de/nachrichten-index/mdax-50.htm")
        print(f"Got {len(mdax_articles)} MDAX articles")
        term_articles.extend(mdax_articles)
    except Exception as e:
        print(f"Error fetching MDAX articles: {e}")

    print("Fetching TecDAX articles...")
    try:
        tecdax_articles = get_articles_finanznachrichten("https://www.finanznachrichten.de/nachrichten-index/tecdax.htm")
        print(f"Got {len(tecdax_articles)} TecDAX articles")
        term_articles.extend(tecdax_articles)
    except Exception as e:
        print(f"Error fetching TecDAX articles: {e}")

    print("Fetching CNBC articles...")
    try:
        cnbc_articles = get_articles_cnbc_latest("https://www.cnbc.com/")
        print(f"Got {len(cnbc_articles)} CNBC articles")
        term_articles.extend(cnbc_articles)
    except Exception as e:
        print(f"Error fetching CNBC articles: {e}")

    print("Fetching Finanzen.net articles...")
    try:
        finanzen_articles = get_articles_finanzen_latest("https://www.finanzen.net/nachrichten/ressort/aktien")
        print(f"Got {len(finanzen_articles)} Finanzen.net articles")
        term_articles.extend(finanzen_articles)
    except Exception as e:
        print(f"Error fetching Finanzen.net articles: {e}")

    print(f"Total articles fetched: {len(term_articles)}")

    if term_articles:
        for term_article in term_articles:
            try:
                comp_name_term_score_response = get_trade_term_scores_from_llm(term_article)
                parsed_comp_names_scores_dict = parse_company_names_scores(comp_name_term_score_response)
                term_scores = get_ticker_trade_term_scores(parsed_comp_names_scores_dict)
                for stock, term in term_scores.items():
                    trade_term_scores_accum.setdefault(stock, []).append(term)
            except Exception as e:
                print(f"Error getting trade term scores: {e}")
                continue

        final_trade_term_scores = {
            stock: sum(terms) / len(terms) for stock, terms in trade_term_scores_accum.items()
        }

        print("Got final trade term scores")
        return final_trade_term_scores
    else:
        print("No articles, couldn't get trade term scores")
        return {}
        


# takes in a dict of stocks, reads latest articles for each stock and generates scores, used to offset lack of information on stocks present in portfolio
def get_final_scores_for_portfolio_stocks(portfolio: dict) -> dict:

    if not portfolio:
        return {}

    stock_scores = {}

    print("Getting scores for portfolio stocks...")

    for stock in portfolio.keys():
        try:
            if not isinstance(stock, str) or not stock:
                print(f"Invalid stock ticker: {stock}")
                continue

            if stock in german_tickers and not stock.endswith(".DE"):
                stock += ".DE"

            # Fetch news articles using Yahoo Finance
            ticker = yf.Ticker(stock)
            news_articles = getattr(ticker, "news", None)

            if not news_articles:
                print(f"No news articles found for {stock} on Yahoo Finance")
                continue

            # Process article titles and summaries
            article_texts = []
            for article in news_articles[:10]:  # Limit to 10 articles
                content = article.get("content", {})

                title = content.get("title", "").strip()
                summary = content.get("summary", "").strip()

                if title:
                    text = title + (f" {summary}" if summary else "")
                    article_texts.append(text)
                else:
                    print(f"Skipping article with empty title for {stock}")

            if not article_texts:
                print(f"No valid articles found for {stock}")
                continue

            combined_text = "\n".join(article_texts)

            # Get sentiment score from LLM
            scores_response = get_scores_from_llm(combined_text, [stock])
            scores = parse_ticker_scores(scores_response)

            if stock in scores:
                stock_scores[stock] = scores[stock]
            else:
                print(f"No valid score parsed for {stock}, defaulting to 50")
                stock_scores[stock] = 50.0


            # Avoid API rate limits
            time.sleep(1)

        except Exception as e:
            print(f"Error processing {stock}: {e}")
            stock_scores[stock] = 0.0  # Assign default score on error

    return stock_scores



def get_amount_to_buy(total_networth, stock_scores: dict) -> dict:
    """Calculate buy amounts for stocks based on scores and available balance."""
    from collections import defaultdict
    buy_amounts = defaultdict(float)
    
    
    # Filter stocks with scores above 50
    investable = {stock: score for stock, score in stock_scores.items() if score > 50}
    if not investable:
        print("No stocks with scores above 50")
        return {}
    
    total_score_points = sum(score for score in investable.values())
    if total_score_points <= 0:
        print("Total score points is 0")
        return {}
        
    # Calculate allocation based on relative scores
    for stock, score in investable.items():
        # adjust for volatility 
        adjusted_score = score + adjust_score_master(stock)

        if adjusted_score < 0:
            adjusted_score = 0
        if adjusted_score > 100:
            adjusted_score = 100

        # Calculate weight based on score relative to total scores
        weight = adjusted_score / total_score_points
        # maximum allocation is 15 percent of the cash balance per stock 
        max_allocation = 0.9 * total_networth
        # Allocate portion of port based on weight
        allocation = total_networth * weight
        
        buy_amounts[stock] = min(max_allocation, allocation)
    
    return dict(buy_amounts)



def get_amount_to_sell(positions: dict, stock_scores: dict, final_trade_term_scores: dict) -> dict:

    sell_amounts = defaultdict(float)
    
    scores_for_positions = get_final_scores_for_portfolio_stocks(positions)

    for stock, score in stock_scores.items():
        if stock.split(".")[0] in sp500_tickers or stock in german_tickers:
            adjusted_score = score + adjust_score_master(stock)

            if adjusted_score < 0:
                adjusted_score = 0
            if adjusted_score > 100:
                adjusted_score = 100

            stock_scores[stock] = adjusted_score
        else:
            continue

    for stock, info in positions.items():
        shares = info['shares']
        if shares <= 0:
            continue
        avg_bought_at = info['avg_cost']  # Directly from IB API
        current_price = get_stock_closing_price(stock) # type: ignore
        if current_price <= 0:
            continue
        total_current_value = shares * current_price
        # average of original score (if existent) and the new score based off articles
        score = (stock_scores.get(stock, 50) + scores_for_positions.get(stock, 50)) / 2

        # Calculate sell fraction
        baseline_sell_fraction = ((50 - score) / 50) if score < 50 else 0
        if stock in final_trade_term_scores:
            term_score = final_trade_term_scores[stock]
            adjusted_sell_fraction = baseline_sell_fraction * (1 - term_score / 100)
        else:
            adjusted_sell_fraction = baseline_sell_fraction

        sell_value = total_current_value * adjusted_sell_fraction
        change_percent = (current_price - avg_bought_at) / avg_bought_at if avg_bought_at > 0 else 0

        # reduce force selling when stock is down by checking term score
        if change_percent < 0:
            term_score = final_trade_term_scores.get(stock, 50)
            
            if term_score > 80:
                print(f"Not forcing a sale for {stock} due to high long-term trade term score ({term_score}).")
                sell_value = 0

        if sell_value > 0 and (change_percent < -0.10 or change_percent > 0.10):
            forced_sell_fraction = 0.60
            sell_value = max(sell_value, total_current_value * forced_sell_fraction) 
            sell_value = min(sell_value, total_current_value)
            sell_amounts[stock] = sell_value


    return dict(sell_amounts)



# retrieves most recent closing price for a given stock
def get_stock_closing_price(stock: str, max_retries: int = 3) -> float:
    """
    Gets the most recent closing price for a given stock using Yahoo Finance.
    """
    # Fix for German tickers
    if stock.split('.')[0] in german_tickers and not stock.endswith('.DE'):
        stock = f"{stock}.DE"

    for attempt in range(max_retries):
        try:
            ticker = yf.Ticker(stock)

            # Try to get the current price from info first (faster)
            info = ticker.info

            # Try multiple price fields in order of preference
            price = None
            if 'currentPrice' in info and info['currentPrice']:
                price = float(info['currentPrice'])
            elif 'regularMarketPrice' in info and info['regularMarketPrice']:
                price = float(info['regularMarketPrice'])
            elif 'previousClose' in info and info['previousClose']:
                price = float(info['previousClose'])

            # If info doesn't work, try historical data
            if not price or price <= 0:
                history = ticker.history(period="1d")
                if not history.empty:
                    price = float(history['Close'].iloc[-1])

            # Validate and return price
            if price and price > 0:
                return price
            else:
                print(f"[Attempt {attempt+1}] No valid price found for {stock}")

        except Exception as e:
            print(f"[Attempt {attempt+1}] Error fetching price for {stock}: {e}")

        # Short delay before retry
        if attempt < max_retries - 1:
            time.sleep(1)

    print(f"Failed to fetch reliable price for {stock} after {max_retries} attempts.")
    return 0.0



def get_exchange_rate_euro_to_dollar(pair="EURUSD=X") -> float:
    try:
        ticker = yf.Ticker(pair)
        data = ticker.history(period="1d")
        if not data.empty:
            return data["Close"].iloc[-1]
        return 1.0  # Default if fetch fails
    except Exception as e:
        print(f"Error getting exchange rate for {pair}: {e}")
        return 1.0

    """Schedules both functions to run concurrently."""


def get_stock_exchange(stock_symbol) -> str:
    """Get the correct exchange for a stock symbol."""
    # First check if it's a German stock by symbol or .DE extension
    base_symbol = stock_symbol.split('.')[0]
    if base_symbol in german_tickers or stock_symbol.endswith('.DE'):
        print(f"Identified {stock_symbol} as German stock")
        return 'IBIS'
        
    # Then check if it's a US stock
    if base_symbol in sp500_tickers:
        print(f"Identified {stock_symbol} as US stock")
        return 'SMART'
        
    # Default case with logging
    try:
        ticker = yf.Ticker(stock_symbol) # type: ignore
        info = ticker.info
        if 'exchange' in info:
            result = info['exchange']
            return result
    except Exception as e:
        print(f"Error getting exchange for {stock_symbol}: {e}")
    return 'Unknown'




"""
Reading and writing term scores from and to file
"""

def save_scores_to_json(stock_scores: dict, filename: str):

    try:
        with open(filename, "w") as file:
            json.dump(stock_scores, file, indent=4)
    except Exception as e:
        print(f"Error saving scores to file: {e}")



def load_scores_from_json(filename: str):

    try:
        with open(filename, "r") as file:
            stock_scores = json.load(file)
        return stock_scores
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {filename}.")
        return {}





"""
Additional weighting of scores  
"""


def volatility_additional_score(stock) -> int:
    try:
        ticker = yf.Ticker(stock)
        beta = ticker.info.get("beta", 1.0)
        if beta > 1.5:
            # High volatility detected; reduce score by 5 points
            return -5
        return 0
    except Exception as e:
        print(f"Error fetching volatility info for {stock}: {e}")
        return 0
    finally:
        time.sleep(2)
    


def recommendations_additional_score(stock: str) -> int:
    try:
        # Validate input
        if not stock or not isinstance(stock, str):
            raise ValueError("Stock symbol must be a non-empty string")

        ticker = yf.Ticker(stock)
        
        # Fetch recommendations summary (this is the correct attribute for the DataFrame format you provided)
        # Note: yfinance's `recommendations_summary` is the attribute that provides this data, not `recommendations`
        recommendations = ticker.recommendations_summary
        if recommendations is None or recommendations.empty:
            print(f"No recommendations summary data available for {stock}")
            return 0
        
        
        # Ensure required columns are present
        required_columns = ["period", "strongBuy", "buy", "hold", "sell", "strongSell"]
        if not all(col in recommendations.columns for col in required_columns):
            print(f"Missing required columns in recommendations for {stock}. Found: {list(recommendations.columns)}")
            return 0
        
        # Get the most recent period (should be "0m")
        latest_period = recommendations[recommendations["period"] == "0m"]
        if latest_period.empty:
            print(f"No data for the current period (0m) for {stock}")
            return 0
        
        # Extract the latest ratings
        strong_buy = int(latest_period["strongBuy"].iloc[0])
        buy = int(latest_period["buy"].iloc[0])
        hold = int(latest_period["hold"].iloc[0])
        sell = int(latest_period["sell"].iloc[0])
        strong_sell = int(latest_period["strongSell"].iloc[0])
        
        # Calculate the weighted score
        weighted_score = (2 * strong_buy) + (1 * buy) + (0 * hold) + (-1 * sell) + (-2 * strong_sell)
        
        # Calculate the total number of ratings
        total_ratings = strong_buy + buy + hold + sell + strong_sell
        if total_ratings == 0:
            print(f"No ratings available for {stock} in the current period")
            return 0
        
        # Normalize the score to a range of [-2, 2]
        normalized_score = (weighted_score / total_ratings) * 2
        
        # Scale to the range [-10, 10] and round to an integer
        final_score = round(normalized_score * 5)
        
        # Cap the score within [-10, 10]
        final_score = max(min(final_score, 10), -10)
        
        return final_score
    
    except Exception as e:
        print(f"Failed to get recommendation info for {stock}: {e}")
        return 0
    finally:
        time.sleep(2)


def earnings_reports_additional_score(stock: str) -> int:

    try:
        # Validate input
        if not stock or not isinstance(stock, str):
            raise ValueError("Stock symbol must be a non-empty string")

        ticker = yf.Ticker(stock)
        
        # Fetch earnings dates
        earnings_dates = ticker.calendar
        if earnings_dates is None:
            print(f"No earnings calendar data available for {stock}")
            return 0
        
        # Handle different possible formats of earnings_dates
        next_earnings = None
        if isinstance(earnings_dates, pd.DataFrame):
            # If it's a DataFrame, look for "Earnings Date" in the index or columns
            if "Earnings Date" in earnings_dates.index:
                next_earnings = earnings_dates.loc["Earnings Date"].iloc[0]
            elif "Earnings Date" in earnings_dates.columns:
                next_earnings = earnings_dates["Earnings Date"].iloc[0]
            else:
                print(f"No 'Earnings Date' found in DataFrame for {stock}. Index: {earnings_dates.index}, Columns: {earnings_dates.columns}")
                return 0
        elif isinstance(earnings_dates, dict):
            # If it's a dictionary, use .get()
            next_earnings = earnings_dates.get("Earnings Date", None)
        elif isinstance(earnings_dates, list) and len(earnings_dates) > 0:
            # If it's a list, assume the first item is the next earnings date
            next_earnings = earnings_dates[0]
        
        if next_earnings is None:
            print(f"No upcoming earnings date found for {stock}")
            return 0
        
        # Handle the case where next_earnings is a list of dates
        if isinstance(next_earnings, list):
            if not next_earnings:
                print(f"Earnings date list is empty for {stock}")
                return 0
            # Select the earliest date in the list
            next_earnings = min(next_earnings)
        
        # Convert next_earnings to a timezone-aware Timestamp
        try:
            # Handle different possible types
            if isinstance(next_earnings, (str, date, pd.Timestamp)):
                next_earnings = pd.to_datetime(next_earnings)
            else:
                raise ValueError(f"Unexpected earnings date format: {type(next_earnings)}")
            
            # Ensure timezone awareness (convert to UTC)
            if next_earnings.tzinfo is None:
                # Assume the date is in UTC if no timezone is specified
                next_earnings = next_earnings.tz_localize("UTC")
            else:
                next_earnings = next_earnings.tz_convert("UTC")
        except Exception as e:
            print(f"Failed to convert earnings date for {stock}: {e}")
            return 0
        
        # Get the current time in UTC
        now = datetime.now(timezone.utc)
        
        # Calculate the difference in days
        days_until_earnings = (next_earnings - now).days
        
        # Adjust score if earnings are within 7 days
        if 0 <= days_until_earnings < 7:
            print(f"Earnings report for {stock} within {days_until_earnings} days, applying penalty")
            return -10
        
        return 0
    
    except Exception as e:
        print(f"Failed to get earnings report info for {stock}: {e}")
        return 0
    finally:
        time.sleep(2)



def put_call_ratio_additional_scores(stock: str) -> int:

    try:
        # Validate input
        if not stock or not isinstance(stock, str):
            raise ValueError("Stock symbol must be a non-empty string")

        ticker = yf.Ticker(stock)
        
        # Fetch options data (use the first available expiration date)
        option_dates = ticker.options
        if not option_dates:
            print(f"No options data available for {stock}")
            return 0
        
        # Use the first expiration date (closest to today)
        earliest_date = option_dates[0]
        options = ticker.option_chain(earliest_date)
        
        # Calculate put and call volumes, handling NaN/None values
        put_volume = 0
        if not options.puts.empty and "volume" in options.puts.columns:
            put_volumes = options.puts["volume"].fillna(0)  # Replace NaN with 0
            put_volume = int(put_volumes.sum())  # Ensure integer
        else:
            print(f"No put options volume data for {stock}")
        
        call_volume = 0
        if not options.calls.empty and "volume" in options.calls.columns:
            call_volumes = options.calls["volume"].fillna(0)  # Replace NaN with 0
            call_volume = int(call_volumes.sum())  # Ensure integer
        else:
            print(f"No call options volume data for {stock}")
        
        # Debug: Print the calculated volumes
        print(f"Put volume for {stock}: {put_volume}")
        print(f"Call volume for {stock}: {call_volume}")
        
        # Check if we have enough data to calculate the ratio
        if call_volume == 0 or (put_volume == 0 and call_volume == 0):
            print(f"Insufficient options volume data for {stock} to calculate put/call ratio")
            return 0
        
        # Calculate the put/call ratio
        put_call_ratio = put_volume / call_volume
        print(f"Put/Call ratio for {stock}: {put_call_ratio:.2f}")
        
        # Adjust score based on the put/call ratio
        if put_call_ratio > 1.5:  # Bearish sentiment
            print(f"Bearish sentiment detected for {stock} (put/call ratio = {put_call_ratio:.2f})")
            return -10
        elif put_call_ratio < 0.5:  # Bullish sentiment
            print(f"Bullish sentiment detected for {stock} (put/call ratio = {put_call_ratio:.2f})")
            return 10
        else:  # Neutral sentiment
            print(f"Neutral sentiment for {stock} (put/call ratio = {put_call_ratio:.2f})")
            return 0
    
    except Exception as e:
        print(f"Failed to get put/call ratio info for {stock}: {e}")
        return 0
    finally:
        time.sleep(2)



def momentum_additional_score(stock: str):

    try:
        # Validate input
        if not stock or not isinstance(stock, str):
            raise ValueError("Stock symbol must be a non-empty string")

        ticker = yf.Ticker(stock)
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=35)  # 1 month with buffer for weekends / holidays
        
        # Fetch historical data (daily interval)
        data = ticker.history(start=start_date, end=end_date, interval="1d")
        
        if data.empty or len(data) < 2:
            raise ValueError(f"Not enough price data for {stock} over the last {30} days")
        
        # Get the closing prices at the start and end of the period
        start_price = data["Close"].iloc[0]  # First available price in the period
        end_price = data["Close"].iloc[-1]  # Most recent price
        
        if not isinstance(start_price, (int, float)) or not isinstance(end_price, (int, float)):
            raise ValueError(f"Invalid price data for {stock}: start={start_price}, end={end_price}")
        
        # Calculate momentum as percentage change
        momentum = (end_price - start_price) / start_price * 100

        if momentum >= 20: # potentially overbought
            return -10
        elif momentum <= -20: # potentially oversold
            return 5
        else:
            return 0
    
    except Exception as e:
        print(f"Error calculating momentum for {stock}: {e}")
        return 0  
    finally:
        time.sleep(2)



def institutional_activity_additional_score(stock: str) -> int:

    try:
        # Validate input
        if not stock or not isinstance(stock, str):
            raise ValueError("Stock symbol must be a non-empty string")

        ticker = yf.Ticker(stock)
        
        # Step 1: Fetch institutional holders data
        institutional_holders = ticker.institutional_holders
        if institutional_holders is None or institutional_holders.empty:
            print(f"No institutional holders data available for {stock}")
            return 0
        
        # Get the total shares held by institutions (as a proxy for ownership)
        total_institutional_shares = institutional_holders["Shares"].sum()
        
        # Step 2: Fetch historical price and volume data to infer activity
        end_date = datetime.now()
        start_date = end_date - timedelta(days=35)  # Buffer for weekends/holidays
        data = ticker.history(start=start_date, end=end_date, interval="1d")
        
        if data.empty or len(data) < 2:
            raise ValueError(f"Not enough historical data for {stock} over the last {35} days")
        
        # Calculate average volume and price change over the period
        avg_volume = data["Volume"].mean()
        price_change = (data["Close"].iloc[-1] - data["Close"].iloc[0]) / data["Close"].iloc[0] * 100
        
        # Step 3: Fetch outstanding shares to estimate institutional ownership percentage
        info = ticker.info
        total_shares_outstanding = info.get("sharesOutstanding", None)
        if total_shares_outstanding:
            institutional_ownership_percent = (total_institutional_shares / total_shares_outstanding) * 100
        else:
            institutional_ownership_percent = 0
        
        # Step 4: Infer institutional activity based on volume and price trends
        # High volume + price increase = likely buying
        # High volume + price decrease = likely selling
        # Use volume relative to average as a proxy for institutional activity
        recent_volume = data["Volume"].iloc[-5:].mean()  # Last 5 days
        volume_spike = recent_volume / avg_volume if avg_volume > 0 else 1.0
        
        score_adjustment = 0.0
        if volume_spike > 1.5 and price_change > 5:  # High volume and price increase
            print(f"Detected potential institutional buying for {stock}: volume spike {volume_spike:.2f}x, price change {price_change:.2f}%")
            score_adjustment = 10  # Boost score for buying activity
        elif volume_spike > 1.5 and price_change < -5:  # High volume and price decrease
            print(f"Detected potential institutional selling for {stock}: volume spike {volume_spike:.2f}x, price change {price_change:.2f}%")
            score_adjustment = -10  # Reduce score for selling activity
        else:
            print(f"No significant institutional activity detected for {stock}: volume spike {volume_spike:.2f}x, price change {price_change:.2f}%")
        
        # Step 5: Adjust score based on institutional ownership percentage
        # Higher institutional ownership means their activity has a larger impact
        if institutional_ownership_percent > 50:  # Significant institutional ownership
            score_adjustment *= 1.5  # Amplify the adjustment
            print(f"Amplified adjustment for {stock} due to high institutional ownership ({institutional_ownership_percent:.2f}%)")
        
        return score_adjustment
    
    except Exception as e:
        print(f"Error analyzing institutional activity for {stock}: {e}")
        return 0  # Neutral adjustment if data fetch fails
    finally:
        time.sleep(2)


def price_earnings_ratio_additonal_score(stock: str) -> int:
    try:
        ticker = yf.Ticker(stock)
        pe_ratio = ticker.info.get("trailingPE", None)
        if pe_ratio is not None:
            pe_ratio = float(pe_ratio)
            if pe_ratio > 30:
                return -2
            elif pe_ratio < 10:
                return 2
            else:
                return 0
        
        return 0
    except Exception as e:
        print(f"Error adjusting score for {stock} based on P/E ratio: {e}")
        return 0
    finally:
        time.sleep(2)



def moving_averages_additional_score(stock: str) -> int:

    try:
        # Validate input
        if not stock or not isinstance(stock, str):
            raise ValueError("Stock symbol must be a non-empty string")

        ticker = yf.Ticker(stock)
        
        # Fetch historical price data (need at least 200 days for the 200-day SMA)
        hist = ticker.history(period="1y")
        
        if hist.empty or len(hist) < 200:
            print(f"Insufficient historical data for {stock} to calculate moving averages")
            return 0
        
        # Calculate 50-day and 200-day SMAs
        hist["SMA_50"] = hist["Close"].rolling(window=50).mean()
        hist["SMA_200"] = hist["Close"].rolling(window=200).mean()
        
        # Get the latest and previous values to detect a crossover
        latest_sma_50 = hist["SMA_50"].iloc[-1]
        latest_sma_200 = hist["SMA_200"].iloc[-1]
        prev_sma_50 = hist["SMA_50"].iloc[-2]
        prev_sma_200 = hist["SMA_200"].iloc[-2]
        
        
        # Detect golden cross (50-day SMA crosses above 200-day SMA)
        if prev_sma_50 <= prev_sma_200 and latest_sma_50 > latest_sma_200:
            print(f"Golden cross detected for {stock}, applying bonus")
            return 5
        
        # Detect death cross (50-day SMA crosses below 200-day SMA)
        if prev_sma_50 >= prev_sma_200 and latest_sma_50 < latest_sma_200:
            print(f"Death cross detected for {stock}, applying penalty")
            return -5
        
        return 0
    
    except Exception as e:
        print(f"Failed to calculate moving averages for {stock}: {e}")
        return 0
    finally:
        time.sleep(2)


# fetch the interest rate in the respective country for the stock
def interest_rates_additional_scores(stock) -> int:
    today = datetime.now().date()
    start_date_fred = today - timedelta(days=30) # Look back 30 days for FRED data availability

    # us rate
    if get_stock_exchange(stock) in US_EXCHANGES:
        try:
            fred_series = 'DFEDTARU'

            # Fetch data for the last 30 days and get the most recent entry
            fed_rate_series = pdr.get_data_fred(fred_series, start=start_date_fred, end=today)

            if not fed_rate_series.empty:
                # Get the last available rate and its date index
                last_rate = fed_rate_series.iloc[-1][fred_series]
                rate_value_us = float(last_rate)

                print(f"Successfully fetched US Fed Rate): {rate_value_us}%")

                if rate_value_us <= 2.5:
                    return 3
                elif rate_value_us >= 5:
                    return -3
                else:
                    return 0

            else:
                print(f"Could not find recent US Fed Rate data on FRED for series {fred_series}.")

        except Exception as e:
            print(f"Error fetching US Fed Rate from FRED: {e}")
        finally:
            time.sleep(2)


    elif get_stock_exchange(stock) in EUROPEAN_EXCHANGES:
        # german rate
        try:
            url = "https://tradingeconomics.com/euro-area/interest-rate"
            # Using a more common/recent user agent string
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
            }
            rate_value_germany = None # Initialize

            
            response = requests.get(url, headers=headers, timeout=15) # Increased timeout slightly
            response.raise_for_status() # Check for HTTP errors (like 403 Forbidden, 404 Not Found)
            print(f"Request to {url} successful (Status Code: {response.status_code})")

            soup = BeautifulSoup(response.content, 'lxml')

            target_link_part = '/euro-area/interest-rate'
            found_row = None
            rows = soup.find_all('tr')

            for row in rows:
                link = row.find('a', href=lambda href: href and target_link_part in href)
                if link:
                    # Check if the text nearby confirms it's the main interest rate row
                    row_text = row.get_text(strip=True, separator="|").lower() # Get all text in row, lowercase
                    if "interest rate" in row_text:
                        found_row = row
                        break # Assume the first matching row is the correct one

            if found_row:
                actual_value_element = found_row.find('span', id=re.compile(r'actual', re.IGNORECASE))
                if not actual_value_element:
                    # Option 1b: Fallback - look for the first cell after the link cell that looks like a number
                    cells = found_row.find_all(['td', 'th']) # Get all cells
                    link_cell_index = -1
                    for i, cell in enumerate(cells):
                        if cell.find('a', href=lambda href: href and target_link_part in href):
                            link_cell_index = i
                            break

                    if link_cell_index != -1 and link_cell_index + 1 < len(cells):
                        # Check the cell immediately after the link cell
                        potential_value_cell = cells[link_cell_index + 1]
                        # Check if it contains text that looks like a rate (number maybe with %)
                        if re.search(r'[\d\.]+', potential_value_cell.get_text(strip=True)):
                            actual_value_element = potential_value_cell

                if actual_value_element:
                    rate_text = actual_value_element.get_text(strip=True)
                    try:
                        # Clean the text (remove %, any potential extra chars) and convert
                        cleaned_rate_text = re.sub(r'[^\d\.-]', '', rate_text) # Keep digits, dot, minus
                        rate_value_germany = float(cleaned_rate_text)

                        print(f"Successfully parsed ECB Rate: {rate_value_germany}%")

                        if rate_value_germany <= 2.5:
                            return 3
                        elif rate_value_germany >= 5:
                            return -3
                        else:
                            return 0

                    except ValueError:
                        print(f"Could not convert cleaned ECB rate text '{cleaned_rate_text}' to float.")
                    except TypeError:
                        print(f"Rate text element content was invalid: {rate_text}")
                else:
                    print("Could not find the specific 'actual' value element or subsequent cell within the identified row.")

            else:
                main_value_div = soup.find("div", id="ctl00_ContentPlaceHolder1_ctl00_ctl01_Panel1")
                if main_value_div:
                    rate_text = main_value_div.get_text(strip=True)
                    print(f"Direct search found potential rate text: '{rate_text}'")


        except Exception as e:
            print(f"An error occurred during parsing: {e}")

    return 0    



def rsi_additonal_score(stock, period=14):
    """Calculate RSI and return trading signal"""
    try:
        # Validate input
        if not stock or not isinstance(stock, str):
            raise ValueError("Stock symbol must be a non-empty string")

        stockyf = yf.Ticker(stock)
        history = stockyf.history(period="1y")
        
        # Check if we have enough data
        if history.empty or len(history['Close']) < period:
            print(f"Insufficient data for {stock} to calculate RSI (need at least {period} days)")
            return 0

        prices = history['Close'].values
        prices_series = pd.Series(prices)
        delta = prices_series.diff()
        
        gain = (delta.where(delta > 0, 0)).rolling(window=period, min_periods=1).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period, min_periods=1).mean()
        
        # Avoid division by zero or invalid RS
        if loss.eq(0).all():  # If all losses are zero, RSI is undefined or 100
            print(f"All losses are zero for {stock}, RSI undefined")
            return 0
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # Ensure rsi has valid data
        if rsi.empty or rsi.isna().all():
            print(f"RSI calculation resulted in empty or all-NaN series for {stock}")
            return 0
        
        latest_rsi = rsi.iloc[-1]
        
        # Return signal based on RSI levels
        if pd.isna(latest_rsi):
            return 0
        elif latest_rsi < 30:
            return 2  # Buy signal (oversold)
        elif latest_rsi > 70:
            return -2  # Sell signal (overbought)
        return 0  # Neutral
    
    except Exception as e:
        print(f"Error calculating RSI for {stock}: {e}")
        import traceback
        traceback.print_exc()  # Optional: for detailed debugging
        return 0
    finally:
        time.sleep(2)



def detect_trend_additional_score(stock, window=20):
    try:
        """Detect trend and return trading signal"""
        stockyf = yf.Ticker(stock)
        history = stockyf.history(period="1y")
        prices = history['Close'].values
        prices_series = pd.Series(prices)
        ma = prices_series.rolling(window=window, min_periods=1).mean()
        
        valid_ma = ma.dropna()
        if len(valid_ma) < 2:
            return 0  # Neutral if insufficient data
        
        slope = valid_ma.iloc[-1] - valid_ma.iloc[-2]
        
        if slope > 0:
            return 2  # Buy signal (uptrend)
        elif slope < 0:
            return -2  # Sell signal (downtrend)
        return 0  # Neutral (sideways)
    except:
        print("Error getting trend score")
        return 0
    finally:
        time.sleep(2)








# returns the amount to adjust score by for a given stock
def adjust_score_master(stock) -> float:
    try:
        if stock.split(".")[0] in sp500_tickers or stock.split(".")[0] in german_tickers:
            adjusted_score = volatility_additional_score(stock) + \
                            recommendations_additional_score(stock) + \
                            earnings_reports_additional_score(stock) + \
                            put_call_ratio_additional_scores(stock) + \
                            momentum_additional_score(stock) + \
                            institutional_activity_additional_score(stock) + \
                            price_earnings_ratio_additonal_score(stock) + \
                            moving_averages_additional_score(stock) + \
                            interest_rates_additional_scores(stock) + \
                            rsi_additonal_score(stock, 14) + \
                            detect_trend_additional_score(stock, 20)
                            

            return adjusted_score
        else:
            return 0.0
    except Exception as e:
        print("Warning, adjusted score set to zero due to Error")
        return 0.0
