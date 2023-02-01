import urllib.request
import gzip
import xml.etree.ElementTree as ET


def gethaifuandplace(haifu, url, ban):
    '''
    Download the haifu and return the placing and rate before match
    '''

    HEADER = {
        'Host': 'e.mjv.jp',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }
    t = open(f'./{haifu}/'+url[26:]+'.xml', 'w')
    url = 'https://tenhou.net/0/log/?'+url[26:-5]
    req = urllib.request.Request(url=url, headers=HEADER)
    opener = urllib.request.build_opener()
    response = opener.open(req)
    response = gzip.decompress(response.read()).decode('utf-8')
    root = ET.fromstring(response)
    t.write(response)
    t.close()
    o0, s0, o1, s1, o2, s2, o3, s3 = root[-1].get('owari').split(',')
    sp = [float(s0), float(s1), float(s2), float(s3)]
    placing = [1, 1, 1, 1]
    for i in range(4):
        for j in range(4):
            if(sp[i] < sp[j]):
                placing[i] += 1
    R = root[2].get('rate').split(',')
    return [placing[ban], R[ban]]
