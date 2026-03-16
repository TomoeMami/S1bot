#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os,json,time,io,sys,requests,re
import feedparser as fp

def rep_content(input):
    output = re.sub(r'<br />','\n',input)
    output = re.sub(r'<.+?>','',output)
    return output

if __name__ == '__main__':
    idlist= ['672346917','703007996','672353429','672342685','351609538','672328094','3493082517474232','3493085336046382','3537115310721181','3537115310721781','3546730823944886']
    New = {"672342685":{},"703007996":{},"672353429":{},"351609538":{},"672346917":{},"672328094":{},"3493082517474232":{},"3493085336046382":{},"3537115310721181":{},"3537115310721781":{},"3546730823944886":{}}
    with open ('./Rss.json',"r",encoding='utf-8') as f:
        RssData = json.load(f)
    temp_rss = []
    for i in RssData.values():
        temp_rss = temp_rss + list(i.values())
    cached_rss = set(temp_rss)
    for id in idlist:
        feed = fp.parse('http://127.0.0.1:1200/bilibili/user/dynamic/'+id)
        for entry in feed.entries:
            RssData[id][entry.link] = idict[id] + '[b][url=' + entry.link +']发布动态[/b][/url]：\n[b]' + entry.title + '[/b]\n' + rep_content(entry.description)
    with open ('./Rss.json',"w",encoding='utf-8') as f:
        f.write(json.dumps(RssData,indent=2,ensure_ascii=False))
    with open ('./New.json',"w",encoding='utf-8') as f:
        f.write(json.dumps(New,indent=2,ensure_ascii=False))
    # with open ('./Live.json',"w",encoding='utf-8') as f:
    #     f.write(json.dumps(LiveData,indent=2,ensure_ascii=False))
    os.system("python reply.py")
    exit()
