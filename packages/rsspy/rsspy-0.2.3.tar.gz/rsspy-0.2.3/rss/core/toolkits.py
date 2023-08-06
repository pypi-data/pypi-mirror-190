import codefast as cf


def shorten_url(url: str) -> str:
    host = 'https://bitly.ddot.cc'
    js = cf.net.post(host, json={'url': url}).json()
    return js['url']
