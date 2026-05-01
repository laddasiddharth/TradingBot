# Binance Futures Testnet Trading Bot
A simplified trading bot in Python to place market and limit orders on the Binance Futures Testnet (USDT-M), created for an application task.

## Features
- Place MARKET and LIMIT orders
- Support for BUY and SELL sides 
- Interactive, user-friendly CLI with standard parameters and interactive prompts powered by `Click` and `Rich`
- Comprehensive input validation
- Dedicated configuration for API network, handling timeouts and requests efficiently
- Distinct application structure (separating client connection, orders, and CLI interaction)
- Extensive logging to both console and a rotating rolling file (`trading_bot.log`)

## Setup Instructions

**1. Create a Virtual Environment**
It's recommended to run this project in a virtual environment.
```bash
python -m venv venv
```
Activate it:
- **Windows:** `venv\Scripts\activate`
- **Linux/Mac:** `source venv/bin/activate`

**2. Install Requirements**
```bash
pip install -r requirements.txt
```

**3. Configure Environment Variables**
Rename `.env.example` to `.env` or create a new `.env` file in the project root:
```env
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
```
*(You can generate testnet API keys from [Binance Futures Testnet](https://testnet.binancefuture.com/))*

## How to Run Examples

There are two primary ways to interact with the bot: **Interactive Mode** and **Argument Mode**.

### 1. Interactive Mode
Simply run the script with no arguments. It will safely prompt you for everything:
```bash
python cli.py
```

### 2. Argument Mode (One-liners)
You can directly pass the flags if you know your order exacts.

**MARKET ORDER EXAMPLE (BUY):**
```bash
python cli.py --symbol BTCUSDT --side BUY --order-type MARKET --quantity 0.01
```

**LIMIT ORDER EXAMPLE (SELL):**
```bash
python cli.py --symbol ETHUSDT --side SELL --order-type LIMIT --quantity 0.05 --price 4000.00
```

## Logs
All network interactions and application flows are tracked in the local `trading_bot.log` file, handling standard logs alongside exceptions cleanly.

## Assumptions & Notes
- The network is routed to Binance's Futures Testnet `https://testnet.binancefuture.com/` exclusively per task requirements. DO NOT put production API credentials in the environment variables.
- You have enough isolated margin and valid balances on the testnet to place the order configuration you have chosen.
- A dummy execution without real API credentials will immediately cleanly fail out using our pre-flight connection exceptions handling, maintaining pure internal state integrity.
