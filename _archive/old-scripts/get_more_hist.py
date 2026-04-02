import urllib.request
import json
import ssl
from datetime import datetime

symbols = {'NG': 'NG=F', 'Gold': 'GC=F', 'Silver': 'SI=F'}
for name, sym in symbols.items():
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}?interval=1d&range=14d"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    context = ssl._create_unverified_context()
    try:
        response = urllib.request.urlopen(req, context=context)
        data = json.loads(response.read())
        timestamps = data['chart']['result'][0]['timestamp']
        closes = data['chart']['result'][0]['indicators']['quote'][0]['close']
        
        valid_dates = []
        valid_closes = []
        for t, c in zip(timestamps, closes):
            if c is not None:
                valid_dates.append(datetime.fromtimestamp(t).strftime('%m-%d'))
                valid_closes.append(round(c, 3) if name == 'NG' else round(c, 2))
                
        print(f"{name}_Dates:", valid_dates[-10:])
        print(f"{name}_Closes:", valid_closes[-10:])
    except Exception as e:
        print("Error:", e)
