import urllib.request
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta

# Target categories
categories = ["cs.CL", "cs.AI", "cs.LG", "cs.IR"]
query = "+OR+".join([f"cat:{cat}" for cat in categories])

# Fetch latest 100 papers
url = f"http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results=300"

try:
    response = urllib.request.urlopen(url)
    data = response.read()
    root = ET.fromstring(data)
    
    papers = []
    ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
    
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.replace('\n', ' ').strip()
        summary = entry.find('atom:summary', ns).text.replace('\n', ' ').strip()
        published = entry.find('atom:published', ns).text
        link = entry.find('atom:id', ns).text
        pdf_link = link.replace('abs', 'pdf')
        authors = [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)]
        
        papers.append({
            "title": title,
            "summary": summary,
            "published": published,
            "link": link,
            "pdf_link": pdf_link,
            "authors": authors
        })
        
    with open("arxiv_today.json", "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)
    print(f"Fetched {len(papers)} papers.")
except Exception as e:
    print(f"Error: {e}")

