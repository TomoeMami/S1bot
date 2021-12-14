import json,os

with open ('./Rss.json',"r",encoding='utf-8') as f:
    RssData = json.load(f)
CachedRss = []
for i in RssData.values():
    CachedRss = CachedRss + list(i['bili'].values())
print(CachedRss)
