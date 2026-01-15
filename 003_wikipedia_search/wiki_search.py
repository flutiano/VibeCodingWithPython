"""
Prompts:
1. Create a Python program that can go to Wikipedia and search an article entered by the user. 
   First, create a new subdirectory to put the program in.
2. Instead of a plain-text summary of the article, I want to see the article in a browser.
"""

import requests
import webbrowser

def search_wikipedia(query):
    """
    Searches Wikipedia for the given query and returns the URL of the most relevant article.
    Uses the Wikipedia OpenSearch API.
    """
    api_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "opensearch",
        "search": query,
        "limit": 1,
        "namespace": 0,
        "format": "json"
    }
    headers = {
        "User-Agent": "WikiSearchBot/1.0 (Contact: your-email@example.com)"
    }

    try:
        response = requests.get(api_url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        # OpenSearch result format: [query, [titles], [descriptions], [urls]]
        if len(data) >= 4 and len(data[3]) > 0:
            return data[1][0], data[3][0]
        else:
            return None, None
    except Exception as e:
        print(f"Error connecting to Wikipedia: {e}")
        return None, None

def main():
    print("=== Wikipedia Search ===")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Search for an article: ").strip()

        if query.lower() == 'exit':
            break

        if not query:
            continue

        print(f"Searching for '{query}'...")
        title, url = search_wikipedia(query)

        if url:
            print(f"Found: {title}")
            print(f"Opening {url} in your browser...")
            webbrowser.open(url)
        else:
            print(f"No results found for '{query}'.")
        print("-" * 25)

if __name__ == "__main__":
    main()
