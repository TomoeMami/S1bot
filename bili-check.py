#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os,json,time,io,sys,requests,re,asyncio,aiohttp
from bilibili_api import user,sync

headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78'}

idlist= ['672346917','703007996','672353429','672342685','351609538','672328094','3493082517474232']
dylist = {'672342685':'https://www.douyin.com/user/MS4wLjABAAAAxCiIYlaaKaMz_J1QaIAmHGgc3bTerIpgTzZjm0na8w5t2KTPrCz4bm_5M5EMPy92','672353429':'https://www.douyin.com/user/MS4wLjABAAAAlpnJ0bXVDV6BNgbHUYVWnnIagRqeeZyNyXB84JXTqAS5tgGjAtw0ZZkv0KSHYyhP','351609538':'https://www.douyin.com/user/MS4wLjABAAAAuZHC7vwqRhPzdeTb24HS7So91u9ucl9c8JjpOS2CPK-9Kg2D32Sj7-mZYvUCJCya','672346917':'https://www.douyin.com/user/MS4wLjABAAAAxOXMMwlShWjp4DONMwfEEfloRYiC1rXwQ64eydoZ0ORPFVGysZEd4zMt8AjsTbyt','672328094':'https://www.douyin.com/user/MS4wLjABAAAA5ZrIrbgva_HMeHuNn64goOD2XYnk4ItSypgRHlbSh1c','703007996':'https://www.douyin.com/user/MS4wLjABAAAAflgvVQ5O1K4RfgUu3k0A2erAZSK7RsdiqPAvxcObn93x2vk4SKk1eUb6l_D4MX-n'}

async def post_pics(imgurl):
    url = 'https://p.sda1.dev/api/v1/upload_external_noform'
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(imgurl) as response:
            data = await response.read()
        if(sys.getsizeof(data) < 2000000):
            inttime = int(time.time())
            pic_suffix = imgurl.split(".")[-1]
            params={'filename':str(inttime)+'.'+pic_suffix}
            async with session.post(url,data=data,params=params) as response:
                resp2 = await response.json()
            if(resp2['success']):
                print(imgurl+str(resp2))
                rurl = '[img]'+resp2['data']['url']+'[/img]'
            else:
                rurl = '⟦尺寸过大图片，请至原链接查看⟧'
        else:
            rurl = '⟦尺寸过大图片，请至原链接查看⟧'
        return rurl

async def get_bili(uid,dynamics):
    data=[]
    u = user.User(int(uid))
    offset = 0
    page = await u.get_dynamics(offset)
        #if time.strftime("%H:%M", time.localtime()) in ['18:50','20:00','21:10']:
    # live = await u.get_live_info()
    # liveurl = live['live_room']['url']
    # livetitle = live['live_room']['liveStatus']
    # if(RssData[uid]['livetitle'] != livetitle and livetitle == 1):
    #     New[uid]['bili'][liveurl] = '[b]开播了！直播间标题为 -> [url='+liveurl+']'+ live['live_room']['title'] +'[/url][/b]\n'
    #     RssData[uid]['livetitle'] = livetitle
    #        pics = await post_pics(live['cover'])
    #        New[uid]['bili'][liveurl]= '[b]开始直播了 -> [url='+liveurl+']'+ livetitle +'[/url][/b]\n'+ pics
    if 'cards' in page:
        data.extend(page['cards'])
    for sdata in data:
        url = 'https://t.bilibili.com/'+sdata['desc']['dynamic_id_str']
        dynamics[uid][url] = {}
    datalinks = list(RssData[uid]['bili'].keys())
    links = list(dynamics[uid].keys())
    newlinks = list(set(links) - set(datalinks))
    if(newlinks):
        for link in newlinks:
            for sdata in data:
                if link == ('https://t.bilibili.com/'+sdata['desc']['dynamic_id_str']):
                    if 'dimension' in  sdata['card'].keys():
                        #发布视频
                        dynamics[uid][link]['title'] = sdata['card']['title']
                        pics =await  post_pics(sdata['card']['pic'])
                        dynamics[uid][link]['summary'] = {"txt":'[quote]' +sdata['card']['desc']+'\n',"pic":pics+'[/quote]'}
                    elif 'origin' in sdata['card'].keys():
                        #转发
                        origindyna = json.loads(sdata['card']['origin'])
                        dynamics[uid][link]['title'] = '转发动态'
                        if 'desc' in origindyna.keys():
                            #转发视频
                            pics =await  post_pics(origindyna['pic'])
                            dynamics[uid][link]['summary'] = {"txt":sdata['card']['item']['content']+'\n[quote][b]'+'@'+origindyna['owner']['name']+'[/b]: '+origindyna['dynamic'] + '\n----\n[b]'+origindyna['title']+'[/b]\n'+origindyna['desc']+'\n',"pic":pics+'[/quote]'}
                        elif 'words' in origindyna.keys():
                            #转发文章
                            dynamics[uid][link]['summary'] = {"txt":sdata['card']['item']['content']+'\n[quote][b]'+'@'+origindyna['author']['name']+'[/b]:[b] '+origindyna['title']+'[/b]\n'+origindyna['summary']+'[/quote]',"pic":'\n'}
                        elif 'description' in origindyna['item'].keys():
                            #转发图片动态
                            dynamics[uid][link]['summary'] = {"txt":sdata['card']['item']['content']+'\n[quote][b]'+'@'+origindyna['user']['name']+'[/b]: '+origindyna['item']['description'],"pic":'\n'}
                            for i in origindyna['item']['pictures']:
                                pics =await  post_pics(i['img_src'])
                                dynamics[uid][link]['summary']['pic'] = dynamics[uid][link]['summary']['pic'] + '\n'+ pics
                            dynamics[uid][link]['summary']['pic'] = dynamics[uid][link]['summary']['pic'] +'[/quote]'
                        else:
                            #转发普通动态
                            dynamics[uid][link]['summary'] = {"txt":sdata['card']['item']['content']+'\n[quote][b]'+'@'+origindyna['user']['uname']+'[/b]: '+origindyna['item']['content']+'[/quote]',"pic":'\n'}
                    elif 'words' in sdata['card'].keys():
                        #发文章
                        dynamics[uid][link]['title'] = sdata['card']['title']
                        pics =await  post_pics(sdata['card']['origin_image_urls'][0])
                        dynamics[uid][link]['summary'] = {"txt":'[quote]' + sdata['card']['summary']+'\n',"pic":pics+'[/quote]'}
                    else:
                        #发动态,
                        dynamics[uid][link]['title'] = '发布动态'
                        # 带图动态
                        if 'description' in sdata['card']['item'].keys():
                            dynamics[uid][link]['summary'] = {"txt":'[quote]' +sdata['card']['item']['description'],"pic":'\n'}
                            for i in sdata['card']['item']['pictures']:
                                pics = await post_pics(i['img_src'])
                                dynamics[uid][link]['summary']['pic'] = dynamics[uid][link]['summary']['pic'] + '\n'+ pics
                            dynamics[uid][link]['summary']['pic'] = dynamics[uid][link]['summary']['pic'] +'[/quote]'
                        else:
                            dynamics[uid][link]['summary'] = {"txt":'[quote]' + sdata['card']['item']['content']+'[/quote]',"pic":'\n'}
            print(link+'-')
            title = dynamics[uid][link]['title']
            summary = title +'[/url][/b]\n'+ dynamics[uid][link]['summary']['txt']
            #title = dynamics[uid][link]['title']
            print(title)
            RssData[uid]['bili'][link] = summary
            if summary not in cached_rss:
                New[uid]['bili'][link]= '[b][url='+link+']'+ summary + dynamics[uid][link]['summary']['pic']

async def main():
    tasks = []
    dynamics = {"672342685":{},"703007996":{},"672353429":{},"351609538":{},"672346917":{},"672328094":{},"3493082517474232":{}}
    for uid in idlist:
        tasks.append(get_bili(uid,dynamics))
        # tasks.append(get_douyin(uid,dylist[uid]))
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    # count = 0
    # while 1:
    New = {"672342685":{"bili":{},"douyin":{}},"703007996":{"bili":{},"douyin":{}},"672353429":{"bili":{},"douyin":{}},"351609538":{"bili":{},"douyin":{}},"672346917":{"bili":{},"douyin":{}},"672328094":{"bili":{},"douyin":{}},"3493082517474232":{"bili":{},"douyin":{}}}
    with open ('./Rss.json',"r",encoding='utf-8') as f:
        RssData = json.load(f)
    temp_rss = []
    for i in RssData.values():
        temp_rss = temp_rss + list(i['bili'].values())
    cached_rss = set(temp_rss)
    # with open ('./Live.json',"r",encoding='utf-8') as f:
    #     LiveData = json.load(f)
    #asyncio.get_event_loop().run_until_complete(main())
    asyncio.run(main())
    with open ('./Rss.json',"w",encoding='utf-8') as f:
        f.write(json.dumps(RssData,indent=2,ensure_ascii=False))
    with open ('./New.json',"w",encoding='utf-8') as f:
        f.write(json.dumps(New,indent=2,ensure_ascii=False))
    # with open ('./Live.json',"w",encoding='utf-8') as f:
    #     f.write(json.dumps(LiveData,indent=2,ensure_ascii=False))
    os.system("python reply.py")
    exit()
