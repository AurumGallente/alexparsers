import re
import urllib.request
import lxml.html  as lh
import json

#parse init
urls = ["http://pikabu.ru/search.php?q=gif&page=%s"%(i) for i in range(1, 53)]
results = []

for url in urls:
    req = urllib.request.Request(url, headers={
                    'Connection': 'close',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'
                    })
    site = urllib.request.urlopen(req)
    html = site.read().decode(site.headers.get_content_charset())
    doc = lh.fromstring(html)
    meta = doc.xpath('//meta')
    allmeta = ""
    for el in meta:
        allmeta += lh.tostring(el,encoding='unicode')
    print("Page url:"+url)
    print("Number of posts: %s"%len(doc.xpath('//div[@class="story"]')))
    for elem in doc.xpath('//div[@class="story"]'):
        try:
            title = elem.xpath('.//a[@class="story__title-link "]//text()')[0]
            post_url = elem.xpath('.//div[@class="story__header"]//a[@class="story__title-link "]//@href')[0]
            content_urls = elem.xpath('.//div[@class="story__wrapper"]//a[contains(concat(" ", normalize-space(@class), " "), "b-gifx__state ")]//@href')
            tag_elems = elem.xpath('.//div[@class="story__header"]//a[@class="story__tag"]//text()')
            rating = elem.xpath('.//div[@class="story__left"]//div[@class="story__rating-count"]//text()')[0].strip()
            print("Post url:"+post_url)
        except Exception:
            print('Empty data')
            continue
        if len(content_urls) < 1:
            print('No gif')
            continue
        tags=[]
        for tag in tag_elems:
            tags.append(tag.strip())
        result = {
            "url":url,
            "title":title,
            "tags":tags,
            "rating":rating,
            "post":post_url,
            "gifs":content_urls,
            "meta":allmeta,
            "html":html
        }

        f = open('pikabu.json', 'a')
        js = json.dumps(result, ensure_ascii=False)
        f.write(js+'\n')
        f.close()
