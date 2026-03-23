import urllib.request
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta

rss_urls = [
    'http://feeds.bbci.co.uk/news/world/middle_east/rss.xml',
    'https://www.aljazeera.com/xml/rss/all.xml'
]

news_items = []

for url in rss_urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urllib.request.urlopen(req).read()
        root = ET.fromstring(resp)
        for item in root.findall('.//item'):
            title = item.find('title').text if item.find('title') is not None else ''
            link = item.find('link').text if item.find('link') is not None else ''
            pubDate = item.find('pubDate').text if item.find('pubDate') is not None else ''
            description = item.find('description').text if item.find('description') is not None else ''
            
            # Simple check if related to Iran or Middle East conflicts
            if any(keyword in title.lower() or keyword in description.lower() for keyword in ['iran', 'israel', 'tehran', 'us', 'strike', 'military', 'gaza', 'sanctions']):
                news_items.append({
                    'title': title,
                    'link': link,
                    'pubDate': pubDate,
                    'summary': description,
                    'category': 'Military' if any(k in title.lower() for k in ['strike', 'military', 'war', 'attack', 'missile', 'forces', 'killed']) else 'Diplomatic'
                })
    except Exception as e:
        print(f"Error fetching {url}: {e}")

# Sort by pubDate, although RSS format might need proper parsing. Let's just return top 12.
with open('news_out.json', 'w') as f:
    json.dump(news_items[:15], f, indent=2)
print(f"Saved {len(news_items)} news items to news_out.json")
