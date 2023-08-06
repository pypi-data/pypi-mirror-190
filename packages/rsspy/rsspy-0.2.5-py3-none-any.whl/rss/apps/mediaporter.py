#!/usr/bin/env python
""" 资源搬运工 
"""
from abc import ABC, abstractmethod
from typing import Any, List

import codefast as cf
import feedparser
from bs4 import BeautifulSoup
from pydantic import BaseModel

from rss.base.pipeline import Component, Pipeline
from rss.core.tg import tcp
from rss.data.db import db as rssdb
from rss.utils import get_exception_str


class FeedBody(BaseModel):
    title: str
    link: str
    summary: str
    url: str = None
    text: str = None

    def __str__(self) -> str:
        return "{}\n\n{}".format(self.text, self.url)


class ContentRetriver(ABC):
    def __init__(self, url: str):
        super().__init__()
        self.url = url

    @abstractmethod
    def run(self) -> List[str]:
        pass


class TelegramChannelRetriver(ContentRetriver):
    def run(self) -> List[str]:
        feeds = feedparser.parse(self.url)
        contents = []
        for feed in feeds.entries:
            feed = FeedBody(**feed)
            if '每日消费电子观' in feed.summary: continue
            summary = BeautifulSoup(feed.summary, 'html.parser')
            try:
                feed.url = summary.find_all('a').pop().get('href')
                feed.text = summary.find_all('p')[0].text
                feed.text = feed.text.split('==')[0]
                feed.text = feed.text.split(' | ')[0]
                feed.text = feed.text.split(' - ')[0]
                feed.text = feed.text.split("http")[0]
                if not feed.text.endswith('。'): feed.text += '。'
            except:
                pass
            if feed.url and feed.text:
                contents.append(str(feed))
        return contents


class GetContent(Component):
    def process(self, retriver: ContentRetriver) -> List[str]:
        return retriver.run()


class FilterEmpty(Component):
    def process(self, contents: List[str]) -> List[str]:
        return list(filter(lambda x: x, contents))


class FilterPosted(Component):
    def process(self, contents: List[str]) -> List[str]:
        return list(filter(lambda x: not rssdb.exists(cf.md5sum(x)), contents))

class FilterIthome(Component):
    # 过滤掉 ithome 的文章，在 twitter 上没有预览 
    def process(self, contents: List[str]) -> List[str]:
        return list(filter(lambda x: 'ithome' not in x, contents))

from rss.auth import auth 
class PostToTwitter(Component):
    def process(self, contents: List[str]) -> List[str]:
        success_posts = []
        for content in contents:
            try:
                cf.net.post(auth.cf_twitter_url, content)
                cf.info('posting a tweet: {}'.format(content))
                success_posts.append(content)
            except Exception as e:
                rssdb.set(cf.md5sum(content), 1)
                exception_str = f'{content}\n{get_exception_str(e)}'
                cf.error(exception_str)
                tcp.post(exception_str)
        return success_posts


class CacheSuccessPosts(Component):
    def process(self, contents: List[str]) -> List[str]:
        for content in contents:
            md5 = cf.md5sum(content)
            rssdb.set(md5, 1)
        return contents


def media_port():
    url = 'https://rsshub.app/telegram/channel/CE_Observe'
    retriver = TelegramChannelRetriver(url)
    (Pipeline() 
        .set_source_input(retriver) 
        .add(GetContent()) 
        .add(FilterIthome())
        .add(FilterEmpty()) 
        .add(FilterPosted()) 
        .add(PostToTwitter()) 
        .add(CacheSuccessPosts()) 
        .process()
    )

if __name__ == "__main__":
    media_port()
