import os
import click
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

from bot.logging_config import setup_logging
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from bot.client import BinanceTestnetClient
from bot.orders import place_order

console = Console()

@click.command()
@click.option("--symbol", prompt="Trading Symbol (e.g. BTCUSDT)", help="The trading pair symbol.")
@click.option("--side", prompt="Order Side (BUY / SELL)", help="BUY or SELL")
@click.option("--order-type", prompt="Order Type (MARKET / LIMIT)", help="MARKET or LIMIT")
@click.option("--quantity", prompt="Quantity", type=float, help="Amount of the asset to trade")
@click.option("--price", type=float, default=None, help="Required if order-type is LIMIT")
def main(symbol, side, order_type, quantity, price):
    """Binance Futures Testnet Trading Bot"""
    
    # Validation phase
    try:
        symbol = validate_symbol(symbol)
        side = validate_side(side)
        order_type = validate_order_type(order_type)
        quantity = validate_quantity(quantity)
        price = validate_price(order_type, price)
        if order_type == "LIMIT" and price is None:
            # Re-prompt
            price_input = click.prompt("Price for LIMIT order", type=float)
            price = validate_price(order_type, price_input)
    except ValueError as ve:
        console.print(f"[bold red]Validation Error:[/bold red] {ve}")
        return

    # Logging phase
    logger = setup_logging()
    
    # Start summary
    summary = (
        f"[bold]Symbol:[/bold] {symbol}\n"
        f"[bold]Side:[/bold] {side}\n"
        f"[bold]Type:[/bold] {order_type}\n"
        f"[bold]Quantity:[/bold] {quantity}\n"
    )
    if order_type == "LIMIT":
        summary += f"[bold]Price:[/bold] {price}\n"
        
    console.print(Panel(summary, title="Order Request Summary", border_style="cyan"))

    # Load credentials
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        console.print("[bold red]Configuration Error:[/bold red] Missing BINANCE_API_KEY or BINANCE_API_SECRET in environment variables.")
        logger.error("Missing API credentials.")
        return

    # Execute
    try:
        with console.status(f"[bold green]Connecting to Binance Testnet & Placing Order...[/bold green]"):
            binance_client = BinanceTestnetClient(api_key, api_secret)
            client = binance_client.get_client()
            
            response = place_order(client, symbol, side, order_type, quantity, price)
        
        # Display Success Response
        order_id = response.get("orderId")
        status = response.get("status")
        executed_qty = response.get("executedQty")
        avg_price = response.get("avgPrice")
        
        resp_details = (
            f"[bold green]Order Placed Successfully![/bold green]\n\n"
            f"[bold]Order ID:[/bold] {order_id}\n"
            f"[bold]Status:[/bold] {status}\n"
            f"[bold]Executed Qty:[/bold] {executed_qty}\n"
            f"[bold]Avg Price:[/bold] {avg_price}\n"
        )
        console.print(Panel(resp_details, title="Order Response Details", border_style="green"))
        
    except Exception as e:
        console.print(Panel(f"[bold red]Failed to place order:[/bold red]\n{str(e)}", title="Order Failure", border_style="red"))

if __name__ == "__main__":
    main()
