# Stock Alert Bot Implementation Plan (Final)

## Goal Description
Create a Python script that fetches market data for a user-defined list of stocks and currencies (from `tickers.json`) and sends a daily summary to Discord and Telegram.

## Architecture
The bot uses a decoupled Producer-Consumer pattern:
1.  **Data Fetching (Producer)**: Fetches raw data from Yahoo Finance via `yfinance`.
2.  **Schema Object**: Unified `MarketReport` class (inheriting from `dict`) that holds formatted report data (Title, Description, Items, Footer).
3.  **Messaging (Consumers)**: Parallel async tasks for Discord and Telegram that consume the same `MarketReport` object to compose platform-specific messages (Embeds for Discord, Markdown for Telegram).

## User Review Required
- **Environment Variables**: Requires `DISCORD_BOT_TOKEN`, `DISCORD_CHANNEL_ID`, `TELEGRAM_BOT_TOKEN`, and `TELEGRAM_CHAT_ID` in `.env`.
- **Tickers**: Customizable via `tickers.json`.

## Final Implementation

### 013_stock-alert-bot

#### requirements.txt
- `yfinance`
- `python-dotenv`
- `discord.py` (includes `aiohttp`)

#### tickers.json
- External configuration file for the watchlist.

#### stock_bot.py
- **MarketReport**: Central data structure for the report payload.
- **format_ticker_data**: Central logic for price/change formatting and emoji selection.
- **DiscordOneShotBot**: Discord-specific sender logic.
- **run_telegram_task**: Telegram-specific sender logic using `aiohttp`.

## Verification
- Verified concurrent delivery to both platforms.
- Verified graceful handling of missing credentials.
- Verified correct formatting of stock and currency tickers.
