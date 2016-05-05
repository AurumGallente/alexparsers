import lxml.html  as lh
import json
import urllib.request

response = urllib.request.urlopen('https://api.twitch.tv/kraken/streams')
result = json.loads(response.read().decode('utf-8'))
for stream in result['streams']:
    num = 0
    print("Channel name: %s"%(stream['channel']['display_name']))
    fl = stream['channel']['_links']['follows'].replace('http','https')
    followers = json.loads(urllib.request.urlopen(fl).read().decode('utf-8'))['follows']
    
    for user in followers:
        local_f = json.loads(urllib.request.urlopen("https://api.twitch.tv/kraken/users/%s/follows/channels"%(user['user']['name'])).read().decode('utf-8'))
        if local_f['_total'] > 400:
            num = num+1
        
    
    print("More than 400 followed: %s"%(num))
    print("Viewers: %s"%(stream['viewers']))
    chatters = json.loads(urllib.request.urlopen('https://tmi.twitch.tv/group/user/%s/chatters'%(stream['channel']['name'])).read().decode('utf-8'))
    print("Chatters: %s"%(chatters['chatter_count']))
    print("Percent: %s %%"%((chatters['chatter_count']/stream['viewers'])*100))