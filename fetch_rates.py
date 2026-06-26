import ccxt
import pandas as pd
import os
def fetch_market_snapshot():
    exchange = ccxt.kraken({'enableRateLimit': True})
    target_currencies = {
        'BTC', 'ETH', 'USDT', 'USDC', 'SOL', 'BNB', 'XRP', 'ADA', 
        'AVAX', 'DOT', 'LINK', 'MATIC', 'LTC', 'UNI', 'BCH', 
        'ATOM', 'XLM', 'ALGO', 'NEAR', 'VET'
    }
    tickers = exchange.fetch_tickers()
    edges = []
    for symbol,ticker in tickers.items():
        if '/' not in symbol:
            continue
        base,quote = symbol.split('/')
        if base in target_currencies and quote in target_currencies:
            bid = ticker.get('bid')
            ask = ticker.get('ask')
            if not bid or not ask or bid <= 0 or ask <= 0:
                continue
            edges.append({
                'source': base,
                'target': quote,
                'rate': bid
            })
            edges.append({
                'source': quote,
                'target': base,
                'rate': 1.0 / ask
            })
    df = pd.DataFrame(edges)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'market_edges.csv')
    df.to_csv(file_path, index=False)
    print(f"Data successfully saved to {file_path}")

if __name__ == "__main__":
    fetch_market_snapshot()