"""
Bitcoin Price Fetcher using CoinGecko API

Example output:
    Fetching latest Bitcoin price...
    
    ==================================================
               BITCOIN PRICE
    ==================================================
    Current Price:    $96,502.00 USD
    24h Change:       ▲ +4.53%
    Last Updated:     2026-01-14 23:58:52
    ==================================================
"""

import requests
import sys
from datetime import datetime

def get_bitcoin_price():
    """
    Fetches the latest Bitcoin price in USD using CoinGecko's free API.
    No authentication required.
    """
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        'ids': 'bitcoin',
        'vs_currencies': 'usd',
        'include_24hr_change': 'true',
        'include_last_updated_at': 'true'
    }
    
    try:
        print("Fetching latest Bitcoin price...")
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if 'bitcoin' in data:
            btc_data = data['bitcoin']
            price = btc_data['usd']
            change_24h = btc_data.get('usd_24h_change', 0)
            last_updated = btc_data.get('last_updated_at', 0)
            
            # Format the timestamp
            update_time = datetime.fromtimestamp(last_updated).strftime('%Y-%m-%d %H:%M:%S')
            
            # Display the results
            print("\n" + "="*50)
            print("           BITCOIN PRICE")
            print("="*50)
            print(f"Current Price:    ${price:,.2f} USD")
            
            # Show change with color indicator
            change_symbol = "▲" if change_24h > 0 else "▼" if change_24h < 0 else "="
            print(f"24h Change:       {change_symbol} {change_24h:+.2f}%")
            print(f"Last Updated:     {update_time}")
            print("="*50 + "\n")
            
            return price
        else:
            print("Error: Unable to fetch Bitcoin data from API response.")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Bitcoin price: {e}")
        return None

if __name__ == "__main__":
    price = get_bitcoin_price()
    if price is None:
        sys.exit(1)
