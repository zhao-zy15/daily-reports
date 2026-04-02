import urllib.request
url = "http://export.arxiv.org/rss/cs.AI+cs.CL+cs.LG+cs.IR"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req)
print(resp.read().decode('utf-8')[:1000])
