#!/usr/bin/env python
""" virmatch flash sale monitor
"""
import re
import os
import time
from abc import ABC, abstractmethod
from typing import Any, List

import codefast as cf
import feedparser
from pydantic import BaseModel
from dofast.network import bitly

from codefast.patterns.pipeline import Component, Pipeline
from rss.core.tg import tcp
from rss.data.db import db as rssdb
from rss.utils import get_exception_str
from rss.auth import auth

QUALITY = 67


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

    def isvalid(self, c: str) -> bool:
        match = re.search(r"(?P<rate>\d+)%", c)
        if match and float(match.group('rate')) >= QUALITY:
            return True
        match = re.search(r"(?P<rate>\d+)GB Disk", c)
        if match and float(match.group('rate')) >= 50:
            return True
        return False

    def high_price(self, c: str) -> bool:
        match = re.search(r"(?P<price>\$\d+)", c)
        if match and float(match.group('price').lstrip('$')) >= 25:
            return True
        return False

    def append_short_url(self, c: str) -> str:
        url = re.search(r"(?P<url>https?://\S+)", c)
        short_url = bitly(url.group('url'))
        c = c.replace('&', "%26")
        c += f"\n{short_url}"
        return c

    def process(self, contents: List[str]) -> List[str]:
        # res = [c for c in contents if self.isvalid(c)]
        res = [c for c in contents if self.high_price(c)]
        return [self.append_short_url(c) for c in res]


class PostToTelegram(Component):

    def process(self, contents: List[str]) -> List[str]:
        for c in contents:
            cf.net.post(auth.telegram_api, json={'channel': auth.tg_channel, 'message': c})
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
            rssdb.set(md5, 1)
        return contents


class TimeSleeper(Component):

    def process(self, contents: List[str]) -> List[str]:
        time.sleep(60)
        return contents


def media_port():
    url = 'https://cf.ddot.cc/rss/telegram/channel/monitor_virmach'
    Pipeline()\
        .add(GetContent())\
        .add(FilterEmpty())\
        .add(FilterHighQuality())\
        .add(FilterPosted())\
        .add(PostToTelegram())\
        .add(PopWindowsMessage())\
        .add(CacheSuccessPosts())\
        .add(TimeSleeper())\
        .process(url)


if __name__ == "__main__":
    while True:
        media_port()
