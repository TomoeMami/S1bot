#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os,json,time,io,sys,requests,re,asyncio,aiohttp
from bilibili_api import user,sync

headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36 Edg/93.0.961.52'}

idlist= ['672346917','703007996','672353429','672342685','351609538','672328094']
uid_list = {'672342685':'MS4wLjABAAAAxCiIYlaaKaMz_J1QaIAmHGgc3bTerIpgTzZjm0na8w5t2KTPrCz4bm_5M5EMPy92','672353429':'MS4wLjABAAAAlpnJ0bXVDV6BNgbHUYVWnnIagRqeeZyNyXB84JXTqAS5tgGjAtw0ZZkv0KSHYyhP','351609538':'MS4wLjABAAAAuZHC7vwqRhPzdeTb24HS7So91u9ucl9c8JjpOS2CPK-9Kg2D32Sj7-mZYvUCJCya','672346917':'MS4wLjABAAAAxOXMMwlShWjp4DONMwfEEfloRYiC1rXwQ64eydoZ0ORPFVGysZEd4zMt8AjsTbyt','672328094':'MS4wLjABAAAA5ZrIrbgva_HMeHuNn64goOD2XYnk4ItSypgRHlbSh1c','703007996':'MS4wLjABAAAAflgvVQ5O1K4RfgUu3k0A2erAZSK7RsdiqPAvxcObn93x2vk4SKk1eUb6l_D4MX-n'}

username = 'ubuntu'

with open ('/home/'+username+'/dycookie.txt','r',encoding='utf-8') as f:
        cookie_str1 = f.read()
cookie_str = repr(cookie_str1)[1:-1]
#把cookie字符串处理成字典，以便接下来使用
cookies = {}
for line in cookie_str.split(';'):
    key, value = line.split('=', 1)
    cookies[key] = value

async def post_pics(imgurl):
    url = 'https://p.sda1.dev/api/v1/upload_external_noform'
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(imgurl,cookies=cookies) as response:
            data = await response.read()
        inttime = int(time.time())
        params={'filename':str(inttime)+'.png'}
        async with session.post(url,data=data,params=params) as response:
            resp2 = await response.json()
        if(resp2['success']):
            print(imgurl+str(resp2))
            rurl = '[img]'+resp2['data']['url']+'[/img]'
        else:
            rurl = '⟦尺寸过大图片，请至原链接查看⟧'
        return rurl

async def get_douyin(uid):
    url = 'https://www.douyin.com/user/'+uid_list[uid]
    async with aiohttp.ClientSession(headers=headers,cookies=cookies) as session:
        async with session.get(url) as response:
            result = await response.content.read()
        res = result.decode('utf-8')
        dlinks = re.findall(r'<a href="(//www\.douyin\.com/video/\d+)"',str(res))
        dlinks = list(dlinks)
        for i in range(len(dlinks)):
            dlinks[i] = 'https:'+dlinks[i]
        datalinks = list(RssData[uid]['douyin'].keys())
        newlinks = list(set(dlinks) - set(datalinks))
        if(newlinks):
            for dlink in newlinks:
                print(dlink)
                async with session.get(dlink) as response:
                    html = await response.content.read()
                dy = html.decode('utf-8')
                summary = re.search(r'<h1.*?</h1>',str(dy))
                summary = re.sub(r'<.*?>','',summary.group(0))
                dy_pic_url = 'https://www.iesdouyin.com/web/api/v2/aweme/post/?sec_uid='+uid_list[uid]
                async with session.get(dy_pic_url) as response:
                    dy_pic_info = await response.text()
                dy_pic_json = json.loads(dy_pic_info)
                pics =await  post_pics(dy_pic_json['aweme_list'][0]['video']['dynamic_cover']['url_list'][0])
                summary = summary + '\n'+pics
                RssData[uid]['douyin'][dlink]='[b][url='+ dlink +']发布抖音[/url][/b]\n[quote]'+ summary +'[/quote]'
                New[uid]['douyin'][dlink]= '[b][url='+ dlink +']发布抖音[/url][/b]\n[quote]'+ summary +'[/quote]'


async def main():
    tasks = []
    dynamics = {"672342685":{},"703007996":{},"672353429":{},"351609538":{},"672346917":{},"672328094":{}}
    for uid in idlist:
        # tasks.append(get_bili(int(uid),dynamics))
        tasks.append(get_douyin(uid))
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    New = {"672342685":{"bili":{},"douyin":{}},"703007996":{"bili":{},"douyin":{}},"672353429":{"bili":{},"douyin":{}},"351609538":{"bili":{},"douyin":{}},"672346917":{"bili":{},"douyin":{}},"672328094":{"bili":{},"douyin":{}}}
    with open ('./Rss.json',"r",encoding='utf-8') as f:
        RssData = json.load(f)
    asyncio.run(main())
    with open ('./Rss.json',"w",encoding='utf-8') as f:
        f.write(json.dumps(RssData,indent=2,ensure_ascii=False))
    with open ('./New.json',"w",encoding='utf-8') as f:
        f.write(json.dumps(New,indent=2,ensure_ascii=False))
    os.system("python reply.py")
    exit()
