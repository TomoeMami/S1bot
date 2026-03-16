#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re, time,requests,io,sys,json,os
import feedparser as fp

def rep_content(input):
    output = re.sub(r'<br />','\n',input)
    output = re.sub(r'<.+?>','',output)
    return output

username = 'riko'

idlist= ['672346917','703007996','672353429','672342685','351609538','672328094','3493082517474232','3493085336046382','3537115310721181','3537115310721781','3546730823944886']

New = {"672342685":{},"703007996":{},"672353429":{},"351609538":{},"672346917":{},"672328094":{},"3493082517474232":{},"3493085336046382":{},"3537115310721181":{},"3537115310721781":{},"3546730823944886":{}}

idict = {'672346917':'[b][color=#9Ac8E2]向晚大魔王[/color][/b]','703007996':'[b][color=#689D6A]A-SOUL_Official[/color][/b]','672353429':'[b][color=#DB7D74]贝拉kira[/color][/b]','672342685':'[b][color=#576690]乃琳Queen[/color][/b]','351609538':'[b][color=#B8A6D9]珈乐Carol[/color][/b]','672328094':'[b][color=#E799B0]嘉然今天吃什么[/color][/b]','3493082517474232':'[b][color=#3c3836]枝江娱乐的小黑[/color][/b]','3493085336046382':'[b][color=#282828]枝江娱乐官方[/color][/b]','3537115310721181':'[b][color=#c83872]心宜不是心仪[/color][/b]','3537115310721781':'[b][color=#7253c2]思诺snow[/color][/b]','3546730823944886':'[b][color=#fcdbdf]来芙Laffey[/color][/b]'}

if __name__ == '__main__':
    msg = u''
    with open ('./Rss.json',"r",encoding='utf-8') as f:
        RssData = json.load(f)
    temp_rss = []
    for i in RssData.values():
        temp_rss = temp_rss + list(i.keys())
    cached_rss = set(temp_rss)
    for id in idlist:
        feed = fp.parse('http://127.0.0.1:1200/bilibili/user/dynamic/'+id)
        for entry in feed.entries:
            if not entry.link in cached_rss:
                RssData[id][entry.link] = idict[id] + '[b][url=' + entry.link +']发布动态[/b][/url]：\n[quote]'+ rep_content(entry.description) + '[/quote]\n\n'
                msg = msg + RssData[id][entry.link]
    with open ('./Rss.json',"w",encoding='utf-8') as f:
        f.write(json.dumps(RssData,indent=2,ensure_ascii=False))
    print(msg)
    # msg = False
    if msg:
        while 1:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
            # # 浏览器登录后得到的cookie，也就是刚才复制的字符串
            # cookie_str1 = os.getenv('S1_BOT_COOKIE')
            with open ('/home/'+username+'/s1cookie-1.txt','r',encoding='utf-8') as f:
                cookie_str1 = f.read()
            cookie_str = repr(cookie_str1)[1:-1]
            # #把cookie字符串处理成字典，以便接下来使用
            cookies = {}
            for line in cookie_str.split(';'):
                key, value = line.split('=', 1)
                cookies[key] = value
            # 设置请求头
            headers = {'User-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78'}
            ''' 获取formhash'''
            RURL = 'https://stage1st.com/2b/forum.php?mod=viewthread&fid=6&tid=751272&extra=page%3D1'
            s1 = requests.get(RURL, headers=headers,  cookies=cookies)
            content = s1.content
            rows = re.findall(r'<input type=\"hidden\" name=\"formhash\" value=\"(.*?)\" />', str(content)) #正则匹配找到formhash值
            if len(rows)!=0:
                formhash = rows[0]
                print('formhash is: ' + formhash)
                subject = u''
                with open ('/home/'+username+'/S1PlainTextBackup/A-Thread-id.txt','r') as f:
                    threadid = f.read()
                '''A综ID，手动修改'''
                # threadid = 2028372
                '''A综ID，手动修改'''
                replyurl = 'https://stage1st.com/2b/forum.php?mod=post&action=reply&fid=151&tid='+str(threadid)+'&extra=page%3D1&replysubmit=yes'
                #url为要回帖的地址
                Data = {'formhash': formhash,'message': msg,'subject': subject,'posttime':int(time.time()),'wysiwyg':1,'usesig':1}
                req = requests.post(replyurl,data=Data,headers=headers,cookies=cookies)
                print(req)
                break
            else:
                print('none formhash!')
                continue
