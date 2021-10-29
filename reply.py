#! /usr/bin/env python
# -*- coding: utf-8 -*-

import re, time,requests,io,sys,json,os

idict = {'672346917':'[b][color=#9Ac8E2]向晚大魔王[/color][/b]','703007996':'[b][color=#689D6A]A-SOUL_Official[/color][/b]','672353429':'[b][color=#DB7D74]贝拉kira[/color][/b]','672342685':'[b][color=#576690]乃琳Queen[/color][/b]','351609538':'[b][color=#B8A6D9]珈乐Carol[/color][/b]','672328094':'[b][color=#E799B0]嘉然今天吃什么[/color][/b]'}

if __name__ == '__main__':
    msg = u''
    with open ('./New.json',"r",encoding='utf-8') as f:
        NewData = json.load(f)
    for uid in NewData.keys():
        for name in NewData[uid].keys():
            if name == 'bili':
                for link in NewData[uid]['bili'].keys():
                    summary = NewData[uid]['bili'][link]
                    if '管家代转' not in summary and '运营代转' not in summary:
                        msg = msg + idict[uid] +':' + summary +'\n\n'
            if name == 'douyin':
                for link in NewData[uid]['douyin'].keys():
                    summary = NewData[uid]['douyin'][link]
                    msg = msg + idict[uid] +':'+ summary +'\n\n'
    if msg:
        while 1:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码
            # # 浏览器登录后得到的cookie，也就是刚才复制的字符串
            # cookie_str1 = os.getenv('S1_BOT_COOKIE')
            with open ('/home/riko/s1cookie-2.txt','r',encoding='utf-8') as f:
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
            RURL = 'https://bbs.saraba1st.com/2b/forum.php?mod=viewthread&tid=334540&extra=page%3D1'
            s1 = requests.get(RURL, headers=headers,  cookies=cookies)
            content = s1.content
            rows = re.findall(r'<input type=\"hidden\" name=\"formhash\" value=\"(.*?)\" />', str(content)) #正则匹配找到formhash值
            if len(rows)!=0:
                formhash = rows[0]
                print('formhash is: ' + formhash)
                subject = u''
                with open ('/home/riko/S1PlainTextBackup/A-Thread-id.txt','r') as f:
                    threadid = f.read()
                '''A综ID，手动修改'''
                # threadid = 2028372
                '''A综ID，手动修改'''
                replyurl = 'https://bbs.saraba1st.com/2b/forum.php?mod=post&action=reply&fid=151&tid='+str(threadid)+'&extra=page%3D1&replysubmit=yes'
                #url为要回帖的地址
                Data = {'formhash': formhash,'message': msg,'subject': subject,'posttime':int(time.time()),'wysiwyg':1,'usesig':1}
                req = requests.post(replyurl,data=Data,headers=headers,cookies=cookies)
                print(req)
                New = {}
                with open ('./New.json',"w",encoding='utf-8') as f:
                    f.write(json.dumps(New,indent=2,ensure_ascii=False))
                os.system("./push.sh")
                break
            else:
                print('none formhash!')
