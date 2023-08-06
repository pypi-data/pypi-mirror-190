#!/usr/bin/env python
from typing import NamedTuple
from rss.core import shorten_url
import pyshorteners

shortener = pyshorteners.Shortener()

class Article(NamedTuple):
    uid: str = None
    title: str = None
    url: str = None
    source: str = None
    author: str = None
    date: str = None
    extra_url: str = None
    type: str = None

    def __str__(self):
        return str(self._asdict())

    def telegram_format(self) -> str:
        short_url = shorten_url(self.url) if len(self.url) > 30 else self.url
        source = '%23' + (self.source if self.source else 'source_unknown')
        msg = '{}, {}, {}'.format(self.title, source, short_url)
        return msg

    def tweet_format(self) -> str:
        short_url = shortener.dagd.short(self.url)
        return self.title + '\n' + short_url

