#!/usr/bin/env python
from typing import List, NamedTuple

import codefast as cf
import feedparser
from bs4 import BeautifulSoup

from codefast.patterns.pipeline import Component, Pipeline
from rss.data.db import db as rssdb
from rss.auth import auth 


class FreeApp(object):
    url = 'http://free.apprcn.com/category/ios/feed/'


class FeedBody(NamedTuple):
    title: str
    download_url: str
    date: str
    preview: str
    image: str

    def is_complete(self) -> bool:
        return all(field is not None for field in self)

    def tweets_format(self) -> str:
        return '{}\n\n{}\n\n下载链接: {}\n#iOS限免'.format(self.title, self.preview,
                                                     self.download_url)

    def __str__(self) -> str:
        return str(self._asdict())


class ContentRetriver(Component):
    def _get_feed_body(self, entry) -> FeedBody:
        import time
        e = entry
        title = e['title']
        download_url = None
        date = e.get('published', time.strftime('%Y-%m-%d %H:%M:%S'))
        preview = None
        image = None
        if 'content' in e:
            soup = BeautifulSoup(e['content'][0]['value'], 'html.parser')
            preview = next((p.text for p in soup.find_all('p') if p.text),
                           None)
            for a in soup.findAll('a'):
                if 'apps.apple.com' in a.attrs.get('href', ''):
                    download_url = a.attrs['href']
                    break
            for img in soup.findAll('img'):
                if 'freeapp.macapp8.com' in img.attrs.get('src', ''):
                    image = img.attrs['src']
                    break

        feedbody = FeedBody(title=title,
                            download_url=download_url,
                            date=date,
                            preview=preview,
                            image=image)
        return feedbody

    def process(self, url: str) -> List[FeedBody]:
        feeds = feedparser.parse(url)
        feed_list = []
        for e in feeds['entries']:
            feedbody = self._get_feed_body(e)
            cf.info('feedbody is {}'.format(feedbody))
            if feedbody.is_complete():
                feed_list.append(feedbody)
        return feed_list


class FilterPosted(Component):
    def process(self, feed_list: List[FeedBody]) -> List[FeedBody]:
        return [
            feed for feed in feed_list
            if not rssdb.exists(cf.md5sum(str(feed)))
        ]


class PostToTwitter(Component):
    def process(self, feed_list: List[FeedBody]) -> None:
        success_posts = []
        for feed in feed_list:
            cf.info('tweet feed {}'.format(feed.tweets_format()))
            try:
                cf.net.post(auth.cf_twitter_url, feed.tweets_format())
                success_posts.append(feed)
            except Exception as e:
                cf.error('post to twitter error {}'.format(e))
                rssdb.set(cf.md5sum(str(feed)), 1)
        return success_posts


class SavePosted(Component):
    def process(self, feed_list: List[FeedBody]) -> None:
        for feed in feed_list:
            rssdb.set(cf.md5sum(str(feed)), 1)


class SourceInputSetter(Component):
    def process(self)->str:
        return FreeApp.url

def free_ios_app_feeds():
    # iOS free app feeds
    pl = Pipeline([
        SourceInputSetter(),
        ContentRetriver(),
        FilterPosted(),
        PostToTwitter(),
        SavePosted(),
    ])
    pl.process()
