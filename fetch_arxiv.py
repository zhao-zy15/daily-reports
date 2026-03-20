import urllib.request
import xml.etree.ElementTree as ET
import json
import datetime

# Fix search query syntax: %2B is '+', so we just need to urlencode properly, or just use string
url = "https://export.arxiv.org/api/query?search_query=cat:cs.CL+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.IR&sortBy=submittedDate&sortOrder=descending&max_results=200"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urllib.request.urlopen(req)
data = response.read()

root = ET.fromstring(data)
ns = {'atom': 'http://www.w3.org/2005/Atom'}

papers = []
for entry in root.findall('atom:entry', ns):
    title_elem = entry.find('atom:title', ns)
    if title_elem is None:
        continue
    title = title_elem.text.strip().replace('\n', ' ')
    summary = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
    published = entry.find('atom:published', ns).text
    updated = entry.find('atom:updated', ns).text
    link = entry.find("atom:link[@title='pdf']", ns)
    if link is not None:
        pdf_url = link.attrib['href']
    else:
        pdf_url = entry.find('atom:id', ns).text
    
    arxiv_id = entry.find('atom:id', ns).text.split('/')[-1]
    
    papers.append({
        'title': title,
        'summary': summary,
        'published': published,
        'pdf_url': pdf_url,
        'id': arxiv_id
    })

print(json.dumps(papers, indent=2))
