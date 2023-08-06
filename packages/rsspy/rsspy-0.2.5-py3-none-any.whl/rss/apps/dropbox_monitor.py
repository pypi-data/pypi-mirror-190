#!/usr/bin/env python
""" virmatch flash sale monitor
"""
import os
import time
from abc import ABC, abstractmethod
from typing import List

import codefast as cf
import feedparser
from codefast.patterns.pipeline import Component, Pipeline
from pydantic import BaseModel

from rss.auth import auth
from rss.core.tg import tcp
from rss.data.db import db as rssdb
from rss.utils import get_exception_str


class FeedBody(BaseModel):
    title: str
    link: str
    summary: str

    def __str__(self) -> str:
        return "{}\n{}".format(self.title, self.summary)


class ContentRetriver(ABC):

    def __init__(self, url: str):
        super().__init__()
        self.url = url

    @abstractmethod
    def run(self) -> List[str]:
        pass


class GetContent(Component):

    def process(self, url: str) -> List[str]:
        feeds = feedparser.parse(url)
        res = []
        for feed in feeds.entries:
            feed = FeedBody(**feed)
            res.append(feed.title)
        return res


class GetNewestContent(Component):
    """The getcontent component has delays"""

    def process(self, url: str) -> List[str]:
        lb, hb = 1200, 10000
        mid = (lb + hb) // 2
        url = f'{url}/searchQuery={mid}'
        feeds = feedparser.parse(url)
        res = []
        for feed in feeds.entries:
            feed = FeedBody(**feed)
            res.append(feed.title)
        return res


class FilterEmpty(Component):

    def process(self, contents: List[str]) -> List[str]:
        return list(filter(lambda x: x, contents))


class FilterPosted(Component):

    def process(self, contents: List[str]) -> List[str]:
        return list(filter(lambda x: not rssdb.exists(cf.md5sum(x)), contents))


class FilterHighQuality(Component):

    def format(self, c: str) -> str:
        c = c.replace('&', "%26").replace('#', "")
        return c

    def interest(self, c: str) -> bool:
        keys = ['pikpak']
        return any([k in c.lower() for k in keys])

    def process(self, contents: List[str]) -> List[str]:
        return [self.format(c) for c in contents if self.interest(c)]


class PostToTelegram(Component):

    def process(self, contents: List[str]) -> List[str]:
        for c in contents:
            cf.net.post(auth.telegram_api,
                        json={
                            'channel': auth.tg_channel,
                            'message': c
                        })
        return contents


class PopWindowsMessage(Component):

    def process(self, contents: List[str]) -> List[str]:

        for c in contents:
            os.system(f'notify-send "VirFlash" "{c}"')
        return contents


class CacheSuccessPosts(Component):

    def process(self, contents: List[str]) -> List[str]:
        for content in contents:
            md5 = cf.md5sum(content)
            rssdb.set(md5, 1, ex=60 * 60 * 24 * 7)
        return contents


class TimeSleeper(Component):

    def process(self, contents: List[str]) -> List[str]:
        time.sleep(10)
        return contents


def api():
    url = 'https://cf.ddot.cc/rss/telegram/channel/hezu2'
    Pipeline()\
        .add(GetContent())\
        .add(FilterEmpty())\
        .add(FilterHighQuality())\
        .add(FilterPosted())\
        .add(PostToTelegram())\
        .add(CacheSuccessPosts())\
        .process(url)


if __name__ == "__main__":
    while True:
        api()
