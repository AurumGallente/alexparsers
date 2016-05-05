import re
import urllib.request
import lxml.html  as lh
import json

#parse init
urls = ["http://votrube.ru/gif/page/%s/"%(i) for i in range(1, 21)]
results = []

for url in urls:
    req = urllib.request.Request(url, headers={
                    'Connection': 'close',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'
                    })
    site = urllib.request.urlopen(req)
    html = site.read().decode("windows-1251")
    doc = lh.fromstring(html)
    meta = doc.xpath('//meta')
    allmeta = ""
    for el in meta:
        allmeta += lh.tostring(el,encoding='unicode')
    print("Page url: "+url)
    print("Number of posts: %s"%len(doc.xpath('//div[@class="nblock"]')))
    for elem in doc.xpath('//div[@class="nblock"]'):
        try:
            title = elem.xpath('.//h2//a//text()')[0]
            post_url = elem.xpath('.//h2//a//@href')[0]
            date = elem.xpath('.//div[@class="date"]//span//text()')[0]
            #content_urls = elem.xpath('.//div[@class="story__wrapper"]//a[contains(concat(" ", normalize-space(@class), " "), "b-gifx__state ")]//@href')
            print("Post url: "+post_url)
        except Exception:
            print('Empty data on page')
            continue
        try:
            post_req = urllib.request.Request(post_url, headers={
                        'Connection': 'close',
                        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'
                        })
            post_site = urllib.request.urlopen(post_req)
            post_html = post_site.read().decode("windows-1251")
            post_doc = lh.fromstring(post_html)
        except Exception:
            print("Post url error")
            continue
        id = post_url[18:23]
        gif_elems = post_doc.xpath('.//div[@class="text"]//div[@id="news-id-%s"]//img//@src'%id)
        gifs = []
        for el in gif_elems:
            gifs.append("http://votrube.ru"+el)
        print("Gifs: %s"%len(gifs))
        result = {
            "url":url,
            "title":title,
            "date":date,
            "post":post_url,
            "gifs":gifs,
            "meta":allmeta,
            "html":html
        }

        f = open('votrube.json', 'a')
        js = json.dumps(result, ensure_ascii=False)
        f.write(js+'\n')
        f.close()