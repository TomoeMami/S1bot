import requests,json,re

qqmsg = 'test'
qqurl = 'http://127.0.0.1:7890/send_msg'
qqdata = {
  "message_type": "group",
  "group_id":822519722,
  "message":qqmsg
}
qqreq = requests.post(qqurl,json=qqdata)
