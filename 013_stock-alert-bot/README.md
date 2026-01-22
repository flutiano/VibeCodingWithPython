# Stock Alert Bot

A flexible, decoupled Python bot that fetches market data and sends formatted alerts to **Discord** and **Telegram**.

## Features
- **Centralized Data**: Fetches data once and shares it across notification platforms.
- **Structured Reports**: Uses a common `MarketReport` schema to ensure message consistency.
- **External Configuration**: Tickers are managed in a simple `tickers.json` file.
- **Asynchronous**: Sends notifications concurrently using `asyncio.gather`.
- **Fault-Tolerant**: Continues to work if optional platform credentials (like Telegram) are missing.

## Setup

1. **Install Dependencies**:
   ```bash
   ./venv/bin/python3 -m pip install -r 013_stock-alert-bot/requirements.txt
   ```

2. **Configure Environment**:
   Create a `.env` file in the task directory with:
   ```env
   DISCORD_BOT_TOKEN=your_token
   DISCORD_CHANNEL_ID=your_channel_id
   TELEGRAM_BOT_TOKEN=your_telegram_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```

3. **Configure Tickers**:
   Edit `tickers.json` to add your stocks or currency pairs:
   ```json
   {
       "S&P 500": "^GSPC",
       "NVDA": "NVDA"
   }
   ```

## Usage

Run the bot manually:
```bash
./venv/bin/python3 013_stock-alert-bot/stock_bot.py
```

### Automation (Cron)
To run every weekday at 4 PM:
```bash
0 16 * * 1-5 /path/to/venv/bin/python3 /path/to/013_stock-alert-bot/stock_bot.py
```

## Architecture
The bot follows a producer-consumer pattern where data is fetched first, formatted into a `MarketReport` dictionary, and then dispatched to multiple platform handlers.
