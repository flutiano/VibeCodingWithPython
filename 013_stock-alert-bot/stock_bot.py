"""
Task Prompt: Create a Python program that fetches stock/currency prices and sends alerts to Discord and Telegram.
Features:
- Reads tickers from external `tickers.json`
- Fetches data using `yfinance`
- Decoupled logic: Sends to Discord and/or Telegram independently based on available config.
"""
import os
import discord
import yfinance as yf
from dotenv import load_dotenv
import json
import aiohttp
import asyncio

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_CHANNEL_ID = os.getenv('DISCORD_CHANNEL_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Load tickers from external JSON file
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'tickers.json')
    with open(file_path, 'r') as f:
        TICKERS = json.load(f)
except FileNotFoundError:
    print(f"Error: tickers.json not found at {file_path}")
    TICKERS = {}
except json.JSONDecodeError:
    print("Error: Failed to decode tickers.json")
    TICKERS = {}

def get_market_data(symbol):
    print(f"Fetching data for {symbol}...")
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")
    
    if data.empty:
        print(f"Warning: No data found for {symbol}")
        return None, None
    
    # Get the most recent close 
    current_price = data['Close'].iloc[-1]
    open_price = data['Open'].iloc[-1]
    
    # Calculate daily change percentage
    change_percent = ((current_price - open_price) / open_price) * 100
    
    return current_price, change_percent

def fetch_all_market_data():
    """Fetches data for all tickers and returns a clean dictionary."""
    results = {}
    print("\n--- Starting Data Fetch ---")
    for name, symbol in TICKERS.items():
        price, change = get_market_data(symbol)
        if price is not None:
            results[name] = {"price": price, "change": change}
    print("--- Data Fetch Complete ---\n")
    return results

def format_ticker_data(name, price, change):
    """Helper to format price and change strings consistently."""
    emoji = "📈" if change >= 0 else "📉"
    sign = "+" if change >= 0 else ""
    
    value_str = f"${price:,.2f}"
    if "/" in name:
         value_str = f"{price:,.2f}"
    
    change_str = f"{sign}{change:.2f}%"
    return {
        "name": name,
        "emoji": emoji,
        "value": value_str,
        "change": change_str
    }

class MarketReport(dict):
    """Common report schema for cross-platform messaging."""
    def __init__(self, title="📊 Market Update", description="Latest prices", footer="Stock Alert Bot"):
        super().__init__()
        self["title"] = title
        self["description"] = description
        self["items"] = []
        self["footer"] = footer
        
    def add_ticker(self, name, price, change):
        self["items"].append(format_ticker_data(name, price, change))
        

def prepare_market_report(market_data):
    """Creates/Factory for the MarketReport object."""
    report = MarketReport()
    for name, data in market_data.items():
        report.add_ticker(name, data['price'], data['change'])
    return report

# --- Discord Logic ---

class DiscordOneShotBot(discord.Client):
    def __init__(self, report, channel_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.report = report
        self.channel_id = int(channel_id)

    async def on_ready(self):
        print(f'[Discord] Logged in as {self.user}')
        try:
            channel = self.get_channel(self.channel_id)
            if not channel:
                try:
                    channel = await self.fetch_channel(self.channel_id)
                except Exception as e:
                    print(f"[Discord] Error fetching channel: {e}")
                    await self.close()
                    return

            # Construct Embed from MarketReport schema
            embed = discord.Embed(
                title=self.report["title"],
                description=self.report["description"],
                color=0x3498db
            )
            
            for item in self.report["items"]:
                # Discord formatting: "$123.45 (📈 +1.23%)"
                embed.add_field(
                    name=item["name"], 
                    value=f"{item['value']} ({item['emoji']} {item['change']})", 
                    inline=True
                )
            
            embed.set_footer(text=self.report["footer"])
            
            print(f"[Discord] Sending embed to #{channel.name}...")
            await channel.send(embed=embed)
            print("[Discord] Message sent!")
            
        except Exception as e:
            print(f"[Discord] Error: {e}")
        finally:
            print("[Discord] Closing connection...")
            await self.close()

async def run_discord_task(report):
    if not DISCORD_TOKEN or not DISCORD_CHANNEL_ID:
        print("[Discord] configuration missing, skipping.")
        return

    intents = discord.Intents.default()
    bot = DiscordOneShotBot(report, DISCORD_CHANNEL_ID, intents=intents)
    try:
        await bot.start(DISCORD_TOKEN)
    except Exception as e:
        print(f"[Discord] Failed to start bot: {e}")

# --- Telegram Logic ---

async def run_telegram_task(report):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("[Telegram] configuration missing, skipping.")
        return

    print("[Telegram] Preparing message...")
    
    # Construct message from MarketReport schema
    
    # 1. Title
    lines = [f"*{report['title']}*"]
    
    # 2. Description
    if report.get("description"):
        lines.append(f"_{report['description']}_")
    
    lines.append("") # Spacer
    
    # 3. Items
    for item in report["items"]:
        # Telegram formatting: "📈 *Name*: $123.45 (+1.23%)"
        lines.append(f"{item['emoji']} *{item['name']}*: {item['value']} ({item['change']})")
    
    lines.append("") # Spacer

    # 4. Footer
    if report.get("footer"):
        lines.append(f"`{report['footer']}`")
    
    message = "\n".join(lines)
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=payload) as response:
                if response.status == 200:
                    print("[Telegram] Message sent successfully!")
                else:
                    text = await response.text()
                    print(f"[Telegram] Failed to send: {text}")
        except Exception as e:
            print(f"[Telegram] Connection error: {e}")

# --- Main Orchestrator ---

async def main():
    # 1. Fetch Data Once
    market_data = fetch_all_market_data()
    
    if not market_data:
        print("No market data fetched. Exiting.")
        return

    # 2. Prepare Common Market Report
    report = prepare_market_report(market_data)

    # 3. Run Sending Tasks Concurrently
    tasks = []
    
    if DISCORD_TOKEN:
        tasks.append(run_discord_task(report))
    else:
        print("Discord token not set.")
        
    if TELEGRAM_TOKEN:
        tasks.append(run_telegram_task(report))
    else:
        print("Telegram token not set.")
        
    if not tasks:
        print("No tasks configured (missing tokens for both Discord and Telegram).")
        return

    await asyncio.gather(*tasks)
    
    # Allow underlying aiohttp/SSL connections to close gracefully
    await asyncio.sleep(0.250)

if __name__ == "__main__":
    asyncio.run(main())
