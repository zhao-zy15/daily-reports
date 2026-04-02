import urllib.request
import xml.etree.ElementTree as ET
import re

url = "http://export.arxiv.org/rss/cs.AI+cs.CL+cs.LG+cs.IR"
headers = {'User-Agent': 'Mozilla/5.0'}
try:
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    xml_data = response.read()
    
    # Strip namespaces for easier parsing
    xml_str = xml_data.decode('utf-8')
    xml_str = re.sub(r'\sxmlns="[^"]+"', '', xml_str, count=1)
    
    root = ET.fromstring(xml_str)
    items = root.findall('.//item')
    print(f"Found {len(items)} items in RSS.")
    if len(items) > 0:
        print("First item title:", items[0].find('title').text)
except Exception as e:
    print("Error:", e)
