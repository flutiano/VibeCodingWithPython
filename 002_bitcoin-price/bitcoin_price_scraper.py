"""
Bitcoin Price Scraper using Web Scraping (No API)

This demonstrates an alternative approach to getting Bitcoin prices
by scraping HTML from CoinDesk's website instead of using an API.

Example output:
    Fetching Bitcoin price via web scraping...
    
    ==================================================
           BITCOIN PRICE (Web Scraping)
    ==================================================
    Current Price:    $96,502.00 USD
    Source:           CoinDesk
    Method:           Web Scraping (BeautifulSoup)
    ==================================================

Note: Web scraping is more fragile than APIs and may break if the
      website's HTML structure changes. This is for educational purposes.
"""

import requests
import sys
from bs4 import BeautifulSoup
import re

def get_bitcoin_price_scraping():
    """
    Fetches Bitcoin price by scraping blockchain.info's ticker page.
    No API required - parses HTML directly.
    
    Note: We're using blockchain.info/ticker which is actually a JSON endpoint,
    but we treat it as a web page to demonstrate web scraping concepts.
    For a true HTML scraping example, we scrape the main page too.
    """
    
    # Method 1: Scrape from blockchain.info ticker (JSON-ish response)
    url_ticker = "https://blockchain.info/ticker"
    
    # Method 2: Fallback - scrape from a simple price display
    url_main = "https://www.blockchain.com/explorer"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
    
    try:
        print("Fetching Bitcoin price via web scraping...")
        
        # Try Method 1: blockchain.info/ticker (simplest for demonstration)
        try:
            response = requests.get(url_ticker, headers=headers, timeout=10)
            response.raise_for_status()
            
            # This returns JSON-like data, which we can parse with BeautifulSoup or just regex
            content = response.text
            
            # Extract USD price using regex from the JSON response
            # Example: "USD" : {"15m" : 96502.45, "last" : 96502.45, ... }
            match = re.search(r'"USD"\s*:\s*{[^}]*"last"\s*:\s*([\d.]+)', content)
            if match:
                price = float(match.group(1))
                
                # Try to get the 15-minute average too
                match_15m = re.search(r'"USD"\s*:\s*{[^}]*"15m"\s*:\s*([\d.]+)', content)
                price_15m = float(match_15m.group(1)) if match_15m else None
                
                # Display the results
                print("\n" + "="*50)
                print("    BITCOIN PRICE (Web Scraping)")
                print("="*50)
                print(f"Current Price:    ${price:,.2f} USD")
                if price_15m:
                    print(f"15m Average:      ${price_15m:,.2f} USD")
                print(f"Source:           Blockchain.info")
                print(f"Method:           Web Scraping (Regex)")
                print("="*50 + "\n")
                
                print("⚠️  Note: This method scrapes web content directly.")
                print("          Web scraping can break when sites update!")
                print("          The API method (bitcoin_price.py) is more reliable.\n")
                
                return price
        except Exception as e:
            print(f"Method 1 failed: {e}")
            print("Trying alternative method...")
        
        # Method 2: Try scraping from HTML page
        response = requests.get(url_main, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'lxml')
        
        # Look for price in the page
        # blockchain.com typically has price info in specific divs
        price_text = None
        
        # Try common selectors
        for selector in [
            {'class': 'sc-price'},
            {'data-test': 'btc-price'},
            {'class': 'price'},
        ]:
            elem = soup.find('span', selector) or soup.find('div', selector)
            if elem:
                price_text = elem.get_text(strip=True)
                break
        
        # Extract price from text
        if price_text:
            match = re.search(r'([\d,]+\.?\d*)', price_text)
            if match:
                price = float(match.group(1).replace(',', ''))
                
                print("\n" + "="*50)
                print("    BITCOIN PRICE (Web Scraping)")
                print("="*50)
                print(f"Current Price:    ${price:,.2f} USD")
                print(f"Source:           Blockchain.com")
                print(f"Method:           HTML Scraping (BeautifulSoup)")
                print("="*50 + "\n")
                
                print("⚠️  Note: Web scraping is fragile!")
                print("          Use the API version for production.\n")
                
                return price
        
        # If we got here, nothing worked
        print("\n❌ Error: Could not find Bitcoin price.")
        print("   The website structure may have changed.\n")
        print("💡 This demonstrates why web scraping is fragile!")
        print("   The API version (bitcoin_price.py) is much more reliable.\n")
        print("   Try running: ./venv/bin/python 002_bitcoin-price/bitcoin_price.py\n")
        return None
            
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error fetching page: {e}\n")
        print("💡 This is a common issue with web scraping!")
        print("   Sites may block scrapers or change their structure.")
        print("   Use the API version instead: bitcoin_price.py\n")
        return None
    except Exception as e:
        print(f"\n❌ Error parsing page: {e}\n")
        return None

if __name__ == "__main__":
    price = get_bitcoin_price_scraping()
    if price is None:
        sys.exit(1)
