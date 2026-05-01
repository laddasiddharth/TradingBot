import logging
from typing import Optional, Dict, Any
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

logger = logging.getLogger("trading_bot.orders")

def place_order(
    client: Client,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None
) -> Dict[str, Any]:
    """Places an order on Binance Futures Testnet."""
    # Convert parameters to required Binance formats
    params = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity
    }
    
    if order_type.upper() == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"  # Good Till Cancel required for Limits
        
    logger.info(f"Sending order request: {params}")
    
    try:
        # Create futures order
        response = client.futures_create_order(**params)
        logger.info(f"Order response received: {response}")
        return response
    except BinanceAPIException as e:
        logger.error(f"Binance API Exception: Status {e.status_code} - {e.message}")
        raise
    except BinanceRequestException as e:
        logger.error(f"Binance Request Exception: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error while placing order: {e}")
        raise
