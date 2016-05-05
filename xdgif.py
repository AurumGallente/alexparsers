import re
import urllib.request
from selenium import webdriver
import lxml.html  as lh
import json

#parse init
urls = ["http://xdgif.ru/page/%s"%(i) for i in range(1, 53)]
results = []
for url in urls:
    print(url)
    req = urllib.request.Request(url, headers={
                    'Connection': 'close',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'
                    })
    site = urllib.request.urlopen(req)
    html = site.read().decode("utf-8")
    doc = lh.fromstring(html)
    meta = doc.xpath('//meta')
    allmeta = ""
    for el in meta:
        allmeta += lh.tostring(el,encoding='unicode')
    for elem in doc.xpath('//div[@class="post"]'):
        title = elem.xpath('.//div[@class="title"]//h2//a//text()')[0]
        post_url = elem.xpath('.//div[@class="title"]//h2//a//@href')[0]
        content_url = elem.xpath('.//div[@class="entry"]//p//a//img//@src')[0]
        tags_elem = elem.xpath('.//div[@class="title"]//div[@class="postmeta"]//span[@class="tags"]//text()')
        tags = [x for x in tags_elem if x !=', ']
        date_elem = elem.xpath('.//div[@class="title"]//div[@class="postmeta"]//comment()')
        date = re.search('>.+<', lh.tostring(date_elem[0], encoding='unicode')).group(0)[1:-1]
        rating = elem.xpath('.//div[@class="entry"]//noindex//div[@class="likeblockmain"]//ul//li//div[@class="post-ratings"]//text()')
        if len(rating) == 1:
            rating = "";
        else:
            rating = rating[1]
        iframe = elem.xpath('.//iframe//@src')
        '''
        req_fb = urllib.request.Request(iframe[0], headers={
                    'Connection': 'close',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'
                    })
        site_fb = urllib.request.urlopen(req)
        fb_html = lh.fromstring(site_fb.read().decode("utf-8"))
        fb_likes = fb_html.xpath('//span[@class="pluginCountTextDisconnected"]//text()')[0]
        
        req_vk = urllib.request.Request(iframe[1], headers={
                    'Connection': 'close',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'
                    })
        site_vk = urllib.request.urlopen(req)
        vk_html = lh.fromstring(site_vk.read().decode("utf-8"))
        vk_likes = vk_html.xpath('//span[@id="stats_num"]//text()')[0]
        '''
        result = {
            "url":url,
            "title":title,
            "date":date,
            "tags":tags,
            "rating":rating,
            "post":post_url,
            "content_url":content_url,
            "meta":allmeta,
            "html":html
        }
        print(title,post_url)
        f = open('xdgif.json', 'a')
        js = json.dumps(result, ensure_ascii=False)
        f.write(js+'\n')
        f.close()
