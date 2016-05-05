import urllib.request
import lxml.html  as lh
import json

init_url = "http://riffsy.com/reactions"
req = urllib.request.Request(init_url, headers={
                    'Connection': 'close',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'
                    })
site = urllib.request.urlopen(req)
doc = lh.fromstring(site.read().decode("utf-8"))
urls = doc.xpath('//a[@class="tag"]//@href')

for url in urls:
    print("http://riffsy.com/"+url)
    if url.find('gifkeyboard') != -1:
        print("gifkeyboard skipped")
        continue
    exists = True
    page = 1
    while exists:
        if page == 1:
            page_url = ""
        else:
            page_url = "?page={0}".format(page)
        try:
            req = urllib.request.Request("http://riffsy.com/"+url+page_url, headers={
                    'Connection': 'close',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'
                    })
            site = urllib.request.urlopen(req)
        except Exception:
            print("exception")
            break
        print("http://riffsy.com/"+url+page_url)
        doc = lh.fromstring(site.read().decode("utf-8"))
        lastpage = doc.xpath('//div[@class="zool"]//text()')

        if len(lastpage) != 0:
            exists = False
            break

        post_urls = doc.xpath('//a[@class="sceneheight"]//@href')
        print(len(post_urls))
        for post_url in post_urls:
            print("http://riffsy.com/"+post_url)
            req = urllib.request.Request("http://riffsy.com/"+post_url, headers={
                    'Connection': 'close',
                    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/49.0.2623.108 Chrome/49.0.2623.108 Safari/537.36'
                    })
            site = urllib.request.urlopen(req)
            try:
                html = site.read().decode("utf-8")
            except Exception:
                print("read error")
                continue
            doc = lh.fromstring(html)
            video_url_html = doc.xpath('//div[@class="scenemedia"]//@video')[0]
            raw_url_html = doc.xpath('//div[@class="scenemedia"]//@image')[0]
            video_url = lh.fromstring(video_url_html).xpath("//video//source//@src")
            raw_url = lh.fromstring(raw_url_html).xpath("//img//@src")[0]
            mp4_url = video_url[0]
            try:
                webm_url = video_url[1]
            except Exception:
                webm_url = ""
            tags_elem = doc.xpath('//ul[@class="tags"]//li[@class="tag"]//a//text()')
            tags = []
            for tag in tags_elem:
                tags.append(tag.strip('\n').strip())
            meta = doc.xpath('//meta')
            allmeta = ""
            for el in meta:
                allmeta += lh.tostring(el, encoding='unicode').strip('\n').strip()
            
            result = {
                "url":"http://riffsy.com/"+post_url,
                "raw_url": raw_url,
                "mp4_url": mp4_url,
                "webm_url": webm_url,
                "tags":tags,
                "meta":allmeta,
                "html":html
            }
            #print(html)
            f = open('riffsy.json', 'a')
            js = json.dumps(result, ensure_ascii=False)
            f.write(js+'\n')
            f.close()
        page = page + 1
