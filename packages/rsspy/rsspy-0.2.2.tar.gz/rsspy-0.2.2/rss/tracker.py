import json
import random
from typing import Dict, List, Tuple

import codefast as cf

from rss.apps.data import BLOG_SOURCES
from rss.base.urlparser import TextBody, UrlParser
from rss.core.tg import tcp
from rss.data.db import db as rssdb


class BlogTracker(object):
    def __init__(self, parser: UrlParser):
        self.parser = parser

    def _query_new(self) -> Dict:
        soup = self.parser.fetch_soup()
        results = self.parser.parse(soup)
        return dict((key, value.dict()) for key, value in results.items())

    def _query_old(self) -> Dict:
        res = rssdb.get('rss_{}'.format(self.parser.name))
        return json.loads(res) if res else {}

    def _query_digest(self, old: Dict, new: Dict) -> List[Tuple]:
        # Get to be posted contents.
        diff = new.keys() - old.keys()
        if not diff:
            return random.sample([(k, v) for k, v in new.items()], 1)
        parser_name = 'rss_{}'.format(self.parser.name)
        cf.info('found new blog', str(diff))
        cf.info('results stored in database', parser_name)
        new.update(old)
        rssdb.set(parser_name, json.dumps(new))
        return [(key, new[key]) for key in diff]

    def track(self) -> List[Dict]:
        q_new = self._query_new()
        q_old = self._query_old()
        digest = self._query_digest(q_old, q_new)
        return [d[1] for d in digest]

    def format(self, dict_: Dict) -> str:
        tb = TextBody(**dict_)
        return str(tb)

    def telegram_format(self, dict_: Dict) -> str:
        tb = TextBody(**dict_)
        msg = '{} ({}) %23Blog \n\n{}'.format(tb.title, tb.date, tb.url)
        return msg


def main():
    for _, v in BLOG_SOURCES.items():
        parser = v['parser'](v['host'], v['url'])
        bt = BlogTracker(parser)

        for digest in bt.track():
            cf.info(bt.format(digest))
            tcp.post(bt.telegram_format(digest))
