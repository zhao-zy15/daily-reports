import urllib.request
import json
import re

symbols_map = {
    'Brent': 'OIL',
    'WTI': 'CL',
    'Natural Gas': 'NG',
    'Gold': 'GC',
    'Silver': 'SI'
}

data_out = {}

for name, symbol in symbols_map.items():
    try:
        url = f"https://stock2.finance.sina.com.cn/futures/api/jsonp.php/var/GlobalFuturesService.getGlobalFuturesDailyKLine?symbol={symbol}"
        req = urllib.request.Request(url, headers={'Referer': 'https://finance.sina.com.cn'})
        resp = urllib.request.urlopen(req).read().decode('gbk')
        
        # parse json from jsonp
        match = re.search(r'\[.*\]', resp)
        if match:
            kline_data = json.loads(match.group(0))
            last_10 = kline_data[-10:]
            dates = [item['date'] for item in last_10]
            closes = [float(item['close']) for item in last_10]
            latest = closes[-1]
            data_out[name] = {
                'latest': latest,
                'dates': dates,
                'closes': closes
            }
        else:
            data_out[name] = {'error': 'No data matched'}
    except Exception as e:
        data_out[name] = {'error': str(e)}

# Add S&P 500, USD/IRR, USD/CNY from list API
try:
    url = "https://hq.sinajs.cn/list=gb_inx,fx_susdcny,fx_susdirr"
    req = urllib.request.Request(url, headers={"Referer": "https://finance.sina.com.cn"})
    resp = urllib.request.urlopen(req).read().decode("gbk")
    lines = resp.strip().split('\n')
    for line in lines:
        if 'gb_inx' in line:
            parts = line.split('"')[1].split(',')
            data_out['S&P 500'] = {'latest': float(parts[1])}
        elif 'fx_susdcny' in line:
            parts = line.split('"')[1].split(',')
            data_out['USD/CNY'] = {'latest': float(parts[8])}
        elif 'fx_susdirr' in line:
            parts = line.split('"')[1].split(',')
            data_out['USD/IRR'] = {'latest': float(parts[8])}
except Exception as e:
    data_out['Indices'] = {'error': str(e)}

with open('yf_data.json', 'w') as f:
    json.dump(data_out, f, indent=2)
print("Data saved to yf_data.json")
