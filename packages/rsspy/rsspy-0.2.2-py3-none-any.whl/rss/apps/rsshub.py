#!/usr/bin/env python
""" rss feed
"""
import traceback
from typing import List, Tuple
import codefast as cf
import feedparser

from rss.base.anynews import Article
from rss.base.pipeline import Component, Pipeline, PostToTelegram, FilterPosted, MarkPostedArticlesToDB, SaveToDB, FilterPostedBM25
from rss.core.tg import tcp
from rss.data import RSS_URLS


def get_exception_str(e: Exception) -> str:
    return str(e) + '\n' + traceback.format_exc()

class GetRssSources(Component):
    def process(self, sources_url:str):
        try:
            raise Exception('use build in rss urls')
            resp = cf.net.get(sources_url).text
            resp = cf.eval(resp)
            cf.info('Get rss urls: {}'.format(resp))
            return resp
        except Exception as e:
            cf.error(e)
            return RSS_URLS


class GetArticles(Component):
    def process(self, rss_urls:List[Tuple[str, str]])->List[Article]:
        articles = []
        for url, source in rss_urls:
            cf.info('parsing rss url: {}, source: {}'.format(url, source))
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    article = Article(
                        uid = entry.id if 'id' in entry else 'empty_id',
                        title = entry.title if 'title' in entry else 'empty_title',
                        url = entry.link if 'link' in entry else 'empty_link',
                        source = source,
                        author = entry.author if 'author' in entry else 'empty_author',
                        date = entry.published if 'published' in entry else 'empty_published')
                    # cf.info('found rss entry: {}'.format(article))
                    articles.append(article)
            except Exception as e:
                exception_str = f'{url}\n{get_exception_str(e)}'
                cf.error(exception_str)
                tcp.post(exception_str)

        return articles

class FilterSpam(Component):
    def _is_spam(self, title:str)->bool:
        if '满足条件每人补贴8000元' in title.lower():
            return True
        return False 
    
    def process(self, articles: List[Article]) -> List[Article]:
        return [article for article in articles if not self._is_spam(article.title)]

def rsshub_pipe():
    pipeline = Pipeline()
    pipeline.set_source_input('https://host.ddot.cc/rssurls')
    pipeline\
        .add(GetRssSources())\
        .add(GetArticles())\
        .add(FilterSpam())\
        .add(FilterPosted())\
        .add(FilterPostedBM25())\
        .add(SaveToDB())\
        .add(PostToTelegram())\
        .add(MarkPostedArticlesToDB())
    pipeline.process()     

if __name__ == '__main__':
    rsshub_pipe()
    
    