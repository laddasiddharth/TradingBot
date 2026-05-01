import os
import logging
from binance.client import Client
from binance.enums import FuturesType
from binance.exceptions import BinanceAPIException, BinanceRequestException

logger = logging.getLogger("trading_bot.client")

class BinanceTestnetClient:
    def __init__(self, api_key: str, api_secret: str):
        if not api_key or not api_secret:
            logger.error("API Key or Secret is missing.")
            raise ValueError("API Key and Secret must be provided.")
        
        try:
            # Initialize Binance Client for Futures Testnet
            self.client = Client(api_key, api_secret, testnet=True)
            self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
            
            # Ping testnet to verify connection
            self.client.futures_ping()
            logger.info("Successfully connected to Binance Futures Testnet.")
            
        except BinanceAPIException as e:
            logger.error(f"Binance API Error during initialization: {e}")
            raise
        except BinanceRequestException as e:
            logger.error(f"Binance Request Error (Network): {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error connecting to Binance: {e}")
            raise

    def get_client(self) -> Client:
        return self.client
