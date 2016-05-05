import facebook
import re
from selenium import webdriver
import lxml.html  as lh
import json
import urllib.request
token = '1730411920529630|PWxCtFhJTCg2xGBqRHOxDVAoN_k'
graph = facebook.GraphAPI(access_token=token)
'''
https://graph.facebook.com/v2.5/204324616421942/posts?fields=id,caption,description,message,created_time,link,name,picture,shares,likes.limit%280%29.summary%28true%29,story,type&limit=25&__paging_token=enc_AdDlAJLdj2gPKlblKrtsQE5xTtUL1Y4hiGP7kpMzZCTx44MVf47ZAGIVX3ShY8ZC2uJukmZCZBfTbILggHYfUEqUWnJFmO3qLjCfVBnt0tB3pvZC6X1wZDZD&access_token=1730411920529630|PWxCtFhJTCg2xGBqRHOxDVAoN_k&until=1417944600

'''
url = "https://graph.facebook.com/204324616421942/posts?fields=id,caption,description,message,created_time,link,name,picture,shares,likes.limit%280%29.summary%28true%29,story,type&access_token=1730411920529630"
browser = webdriver.Firefox()

is_next = True
while is_next:
    
    response = urllib.request.urlopen(url)
    js = json.loads(response.read().decode('utf-8'),encoding='unicode-escape')
    if len(js['data']) == 0:
        data = None
    else:
        data = js['data']
    if len(js['paging']) == 0:
        paging = None
    else:
        paging = js['paging']
        
    if len(paging['next']) == 0:
        is_next = False
        break
        
    url = paging['next']
    print(url+'\n')
    
    for post in data:
        print(post['link'])
        browser.get(post['link'])
        html = browser.page_source
        try:
            doc = lh.fromstring(html)
        except Exception:
            print("parse error")
            continue
        created_time = post['created_time']
        post_image = post['picture']
        print()
        try:
            body = doc.xpath('//div[@class="post-content"]')[0]
            body = lh.tostring(body, encoding='unicode')
        except Exception:
            body = ""
        meta = doc.xpath('//meta')
        allmeta = ""
        for el in meta:
            allmeta += lh.tostring(el, encoding='unicode').strip('\n').strip()

        link = post['link']

        try:
            name = post['description']
        except Exception:
            name = ""
        try:
            name = post['name']
        except Exception:
            name = ""
        result = {
            "url":link,
            "name":name,
            "image":post_image,
            "content":body,
            "meta":allmeta,
            "html":html
        }
        f = open('heftig.json', 'a')
        js = json.dumps(result, ensure_ascii=False)
        f.write(js+'\n')
        f.close()

browser.quit()

