#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os,json,time,io,sys,requests,re,asyncio,aiohttp
import bilibili_api as ba

headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

idlist= ['672346917','703007996','672353429','672342685','351609538','672328094','3493082517474232','3493085336046382','3537115310721181','3537115310721781','3546730823944886']
# uid_list = {'672342685':'MS4wLjABAAAAxCiIYlaaKaMz_J1QaIAmHGgc3bTerIpgTzZjm0na8w5t2KTPrCz4bm_5M5EMPy92','672353429':'MS4wLjABAAAAlpnJ0bXVDV6BNgbHUYVWnnIagRqeeZyNyXB84JXTqAS5tgGjAtw0ZZkv0KSHYyhP','351609538':'MS4wLjABAAAAuZHC7vwqRhPzdeTb24HS7So91u9ucl9c8JjpOS2CPK-9Kg2D32Sj7-mZYvUCJCya','672346917':'MS4wLjABAAAAxOXMMwlShWjp4DONMwfEEfloRYiC1rXwQ64eydoZ0ORPFVGysZEd4zMt8AjsTbyt','672328094':'MS4wLjABAAAA5ZrIrbgva_HMeHuNn64goOD2XYnk4ItSypgRHlbSh1c','703007996':'MS4wLjABAAAAflgvVQ5O1K4RfgUu3k0A2erAZSK7RsdiqPAvxcObn93x2vk4SKk1eUb6l_D4MX-n'}

async def get_bili(uid,dynamics):
    data=[]
    u = ba.user.User(int(uid))
    offset = ""
    page = await u.get_dynamics_new(offset)
    # live = await u.get_live_info()
    # livetitle = live['live_room']['title']
    with open ('./test.json',"w",encoding='utf-8') as f:
        f.write(json.dumps(page,indent=2,ensure_ascii=False))
    if 'items' in page:
        data.extend(page['items'])
    for sdata in data:
        url = 'https://t.bilibili.com/'+sdata['id_str']
        RssData[str(uid)]['bili'][url]= '发布动态'
    # RssData[str(uid)]['livetitle'] = livetitle

async def main():
    tasks = []
    dynamics = {"672342685":{},"703007996":{},"672353429":{},"351609538":{},"672346917":{},"672328094":{},"3493082517474232":{},"3493085336046382":{},"3537115310721181":{},"3537115310721781":{},"3546730823944886":{}}
    for uid in idlist:
        await get_bili(uid,dynamics)

if __name__ == '__main__':
    RssData = {"672342685":{"bili":{},"douyin":{}},"703007996":{"bili":{},"douyin":{}},"672353429":{"bili":{},"douyin":{}},"351609538":{"bili":{},"douyin":{}},"672346917":{"bili":{},"douyin":{}},"672328094":{"bili":{},"douyin":{}},"3493082517474232":{"bili":{},"douyin":{}},"3493085336046382":{"bili":{},"douyin":{}},"3537115310721181":{"bili":{},"douyin":{}},"3537115310721781":{"bili":{},"douyin":{}},"3546730823944886":{"bili":{},"douyin":{}}}
    asyncio.run(main())
    with open ('./Rss.json',"w",encoding='utf-8') as f:
        # origin_data = json.load(f)
        # for i in origin_data.keys():
            # origin_data[i]['bili'] = RssData[i]['bili']
        f.write(json.dumps(RssData,indent=2,ensure_ascii=False))
