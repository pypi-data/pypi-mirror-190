#!/usr/bin/env python
""" rss feed
"""

import asyncio as aio
import traceback
from abc import ABC, abstractmethod
from typing import List, Tuple

import codefast as cf
import jieba
from codefast.exception import get_exception_str

from rss.base.bm25 import BM25
from rss.base.sif import sif_embeddings, top_k_similar_sentences, word2vec
from rss.base.todb import insert_many, load_all
from rss.base.types import Article
from rss.core.tg import tcp
from rss.data.db import db as rssdb


def get_exception_str(e: Exception) -> str:
    return str(e) + '\n' + traceback.format_exc()


class Component(ABC):
    @abstractmethod
    def process(self, *args, **kwargs):
        pass

    def exec(self, *args, **kwargs):
        class_name = self.__class__.__name__
        file_name = self.__class__.__module__.split('.')[-1]
        cf.info('pipeline starts exec [{}], args {}, kwargs {}'.format(
            file_name + "." + class_name, args, kwargs))
        results = self.process(*args, **kwargs)
        cf.info('pipeline finish exec [{}], results: {}'.format(
            class_name, results))
        return results


class Pipeline(object):
    def add(self, component: Component):
        self.components.append(component)
        return self

    def __init__(self) -> None:
        self.components = []
        self.source_input = None

    def set_source_input(self, source_input):
        self.source_input = source_input
        return self

    def process(self):
        results = self.source_input
        try:
            for c in self.components:
                if results is not None:
                    results = c.exec(results)
                else:
                    results = c.exec()
        except Exception as e:
            cf.error(get_exception_str(e))
            tcp.post(get_exception_str(e))
        return results


class PostToTelegram(Component):
    def process(self, articles: List[Article]) -> List[Article]:
        succ_posts = []
        for article in articles:
            try:
                cf.info('posting new article: {}'.format(article))
                tcp.post(article.telegram_format())
                succ_posts.append(article)
            except Exception as e:
                exception_str = get_exception_str(e)
                cf.error(exception_str)
                tcp.post(exception_str)
        return succ_posts


class SaveToDB(Component):
    def process(self, articles: List[Article]) -> List[Article]:
        if not articles:
            return articles
        d = {'rss_title_' + str(a.title): str(a) for a in articles}
        try:
            loop = aio.get_event_loop()
        except RuntimeError:
            loop = aio.new_event_loop()
            aio.set_event_loop(loop)
        loop.run_until_complete(insert_many(d))
        return articles


class MarkPostedArticlesToDB(Component):
    def process(self, articles: List[Article]) -> List[Article]:
        for article in articles:
            rssdb.set(article.uid, 1)
        return articles


class FilterPosted(Component):
    def process(self, articles: List[Article]) -> List[Article]:
        nposts = [
            article for article in articles if not rssdb.exists(article.uid)
        ]
        for article in nposts:
            cf.info('found new article: {}'.format(article))
        return nposts


def get_posted(update=False):
    local = 'posted.json'
    if not update:
        return cf.js(local)

    try:
        loop = aio.get_event_loop()
    except RuntimeError:
        loop = aio.new_event_loop()
        aio.set_event_loop(loop)

    resp = loop.run_until_complete(load_all())
    js = {r[1]: r[2] for r in resp}
    cf.js.write(js, local)
    return js


class FilterPostedBM25(Component):
    def __get_corpus(self) -> List[List[str]]:
        js = get_posted(update=True)
        cf.js.write(js, 'posted.json')
        corpus = [_.replace('rss_title_', '') for _ in js.keys()]
        return corpus

    def __is_article_posted(self, title: str, model, corpus_embedding,
                            corpus) -> bool:
        top1 = top_k_similar_sentences(title,
                                       corpus,
                                       model=model,
                                       k=1,
                                       candidate_embedding=corpus_embedding)
        cf.info(top1)
        score = top1[0][0]
        return score > 0.8

    def __get_model(self):
        corpus = self.__get_corpus()
        model = word2vec(corpus)
        corpus_embedding = sif_embeddings(corpus, model)
        return model, corpus_embedding, corpus

    def process(self, articles: List[Article]) -> List[Article]:
        model, corpus_embedding, corpus = self.__get_model()
        return [
            a for a in articles if not self.__is_article_posted(
                a.title, model, corpus_embedding, corpus)
        ]
