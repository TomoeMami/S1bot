#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os,json,time,io,sys,requests,re
import feedparser as fp

idlist= ['672346917','703007996','672353429','672342685','351609538','672328094','3493082517474232','3493085336046382','3537115310721181','3537115310721781','3546730823944886']

def rep_content(input):
    output = re.sub(r'<br />','\n',input)
    output = re.sub(r'<.+?>','',output)
    return output

if __name__ == '__main__':
    RssData = {"672342685":{},"703007996":{},"672353429":{},"351609538":{},"672346917":{},"672328094":{},"3493082517474232":{},"3493085336046382":{},"3537115310721181":{},"3537115310721781":{},"3546730823944886":{}}
    idlist= ['672346917','703007996','672353429','672342685','351609538','672328094','3493082517474232','3493085336046382','3537115310721181','3537115310721781','3546730823944886']
    idict = {'672346917':'[b][color=#9Ac8E2]向晚大魔王[/color][/b]','703007996':'[b][color=#689D6A]A-SOUL_Official[/color][/b]','672353429':'[b][color=#DB7D74]贝拉kira[/color][/b]','672342685':'[b][color=#576690]乃琳Queen[/color][/b]','351609538':'[b][color=#B8A6D9]珈乐Carol[/color][/b]','672328094':'[b][color=#E799B0]嘉然今天吃什么[/color][/b]','3493082517474232':'[b][color=#3c3836]枝江娱乐的小黑[/color][/b]','3493085336046382':'[b][color=#282828]枝江娱乐官方[/color][/b]','3537115310721181':'[b][color=#c83872]心宜不是心仪[/color][/b]','3537115310721781':'[b][color=#7253c2]思诺snow[/color][/b]','3546730823944886':'[b][color=#fcdbdf]来芙Laffey[/color][/b]'}
    for id in idlist:
        feed = fp.parse('http://127.0.0.1:1200/bilibili/user/dynamic/'+id)
        for entry in feed.entries:
            RssData[id][entry.link] = idict[id] + '[b][url=' + entry.link +']发布动态[/b][/url]：\n[b]' + entry.title + '[/b]\n' + rep_content(entry.description)
    with open ('./Rss.json',"w",encoding='utf-8') as f:
        # origin_data = json.load(f)
        # for i in origin_data.keys():
            # origin_data[i]['bili'] = RssData[i]['bili']
        f.write(json.dumps(RssData,indent=2,ensure_ascii=False))
