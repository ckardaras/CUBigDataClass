import yfinance as yf
import numpy as np
import pandas as pd

btc_data = yf.download(tickers='BTC-USD', period='1mo', interval='1d')
eth_data = yf.download(tickers='ETH-USD', period='1mo', interval='1d')

btc_df = pd.DataFrame(btc_data)
eth_df = pd.DataFrame(eth_data)

