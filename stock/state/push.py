#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : lhr (airhenry@gmail.com)
# @Link    : http://about.me/air.henry
import json
import requests

#
# curl -X POST --header 'Access-Token: qpRvxuwgrmMGzpGBX1F3N0HVnnfZ16qa'
#
# https://api.pushbullet.com/v2/pushes --header 'Content-Type: application/json'
#
# --data-binary '{"type": "note", "title": "Note Title", "body": "Note Body"}'
#

def push_to_pushbullet(*message):
    url = 'https://api.pushbullet.com/v2/pushes'
    payload = {"type": "note", "title": "%s"%message[0], "body": "%s"%str(message)}
    headers = {'content-type': 'application/json','Access-Token': 'qpRvxuwgrmMGzpGBX1F3N0HVnnfZ16qa'}
    # return
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    # r = requests.get('http://127.0.0.1:5000/stock/api/push/%s'%message)
    # r = requests.push('https://api.pushbullet.com/v2/pushes'%message)
    return


if __name__ == '__main__':
    pass


