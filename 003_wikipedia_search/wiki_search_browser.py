"""
Prompts:
1. Instead of using Wikipedia API, can you use the browser automation to implement the same functionalit?
2. How about using `selenium` and `webdriver`, and using the Chrome browser which is already installed in the system.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

def search_wikipedia_selenium(query):
    """
    Searches Wikipedia using Selenium by driving the Chrome browser.
    """
    print(f"Starting Chrome to search for: {query}...")
    
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Commented out so the user can see the browser
    
    # Initialize the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Navigate to Wikipedia
        driver.get("https://www.wikipedia.org")
        
        # Find the search input field
        # On the main page, it's usually an input with id 'searchInput'
        search_input = driver.find_element(By.ID, "searchInput")
        
        # Type the query and press Enter
        search_input.send_keys(query)
        search_input.send_keys(Keys.RETURN)
        
        # Wait a moment for the page to load
        time.sleep(2)
        
        print(f"Currently viewing: {driver.title}")
        print(f"URL: {driver.current_url}")
        
        # Keep the browser open so the user can see it
        input("\nPress Enter in this terminal to close the browser and exit...")
        
    except Exception as e:
        print(f"An error occurred during browser automation: {e}")
    finally:
        driver.quit()

def main():
    print("=== Wikipedia Search (Browser Automation) ===")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Search for an article: ").strip()

        if query.lower() == 'exit':
            break

        if not query:
            continue

        search_wikipedia_selenium(query)
        print("-" * 25)

if __name__ == "__main__":
    main()
