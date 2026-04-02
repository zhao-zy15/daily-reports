import urllib.request
import json
import ssl

def get_price(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        context = ssl._create_unverified_context()
        response = urllib.request.urlopen(req, context=context)
        data = json.loads(response.read())
        price = data['chart']['result'][0]['meta']['regularMarketPrice']
        return price
    except Exception as e:
        return str(e)

symbols = {
    'Brent Crude': 'BZ=F',
    'WTI Crude': 'CL=F',
    'Natural Gas': 'NG=F',
    'Gold': 'GC=F',
    'Silver': 'SI=F',
    'S&P 500': '^GSPC',
    'USD/IRR': 'USDIRR=X',
    'USD/CNY': 'CNY=X'
}

for name, sym in symbols.items():
    print(f"{name}: {get_price(sym)}")
