import requests
from codefast.patterns.singleton import SingletonMeta
from rss.auth import auth


class Spider(metaclass=SingletonMeta):
    # Simulate a normal web user
    def __init__(self) -> None:
        pass

    def born(self) -> requests.Session:
        spider = requests.Session()
        spider.encoding = 'utf-8'
        spider.headers.update({
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
        })
        return spider


class AuthOnce(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._info = {}

    def info(self):
        if not self._info:
            self._info = {'hema_bot': auth.hema_bot, 'global_news_podcast': auth.news_channel}
        return self._info
