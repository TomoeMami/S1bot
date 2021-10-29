import requests,json

qqmsg = []

qqurl = 'http://127.0.0.1:1314'
qqdata = {'type' : 'ReplyPush','msg':qqmsg}
qqreq = requests.post(qqurl,json=qqdata)

