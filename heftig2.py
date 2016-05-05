import facebook
import re
#from selenium import webdriver
import lxml.html  as lh
import json
import urllib.request


with open('heftig2.json', 'w') as nf:
    with open('heftig.json', 'r') as f:
        for line in f:
            obj = json.loads(line)
            if obj['content'] == "" and obj["url"].find("facebook.com") == -1:
                req = urllib.request.Request(obj["url"], headers={
                    'Connection': 'close',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'
                    })
                try:
                    site = urllib.request.urlopen(req)
                except Exception:
                    print("open error")
                    continue
                html = site.read().decode("utf-8")
                doc = lh.fromstring(html)
                content = lh.tostring(doc.xpath('//div[@class="post-content"]')[0],encoding='unicode')
                obj['content'] = content
                obj['html'] = html
                res = json.dumps(obj,ensure_ascii=False)
                nf.write(res+'\n')
                print(obj["url"])