import yfinance as yf
import json
from datetime import datetime

symbols_map = {
    'Brent': 'BZ=F',
    'WTI': 'CL=F',
    'Natural Gas': 'NG=F',
    'Gold': 'GC=F',
    'Silver': 'SI=F',
    'S&P 500': '^GSPC',
    'USD/IRR': 'USDIRR=X',
    'USD/CNY': 'CNY=X'
}

data_out = {}

for name, symbol in symbols_map.items():
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="15d")
        if not hist.empty:
            dates = [d.strftime('%Y-%m-%d') for d in hist.index][-10:]
            closes = [round(c, 3) if name == 'Natural Gas' else round(c, 2) for c in hist['Close']][-10:]
            latest = closes[-1]
            data_out[name] = {
                'latest': latest,
                'dates': dates,
                'closes': closes
            }
        else:
            data_out[name] = {'error': 'No data'}
    except Exception as e:
        data_out[name] = {'error': str(e)}

with open('yf_data.json', 'w') as f:
    json.dump(data_out, f, indent=2)
print("Data saved to yf_data.json")
