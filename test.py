import requests,json,re

qqmsg = []

link ="https://t.bilibili.com/587030370470553294"

summary = "[b][url=https://t.bilibili.com/587030370470553294]发布动态[/url][/b]\n[quote]“提前晚安   关心我都看到辣～” [/quote]"

qqmsg.append({"type":"Plain", "text":str(link)})

tempmsg = re.sub(r'\[.+?\]','',summary)

qqmsg.append({"type":"Plain", "text":str(tempmsg)})

qqmsg_img = re.findall(r'\[img\](.*?)\[/img\]',summary)

if(len(qqmsg_img)!=0):
    for i in qqmsg_img:
        qqmsg.append({"type":"Image", "url":str(i)})
print(qqmsg)
qqurl = 'http://127.0.0.1:1314'
qqdata = {'type' : 'ReplyPush','msg':qqmsg}
qqreq = requests.post(qqurl,json=qqdata)
