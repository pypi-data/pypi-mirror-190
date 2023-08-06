#!/usr/bin/env python
from abc import ABC, abstractmethod
from typing import List

import codefast as cf
from bs4 import BeautifulSoup

from rss.base.pipeline import (Component, FilterPosted, FilterPostedBM25,
                               MarkPostedArticlesToDB, Pipeline,
                               PostToTelegram, SaveToDB)
from rss.base.types import Article
from rss.core import Spider


class FilterEmpty(Component):

    def process(self, articles: List[Article]) -> List[Article]:
        return [article for article in articles if article.uid]


class AnyNews(Component):
    """ check whether any new articles posted in a certain website
    """

    @abstractmethod
    def search_articles(self) -> List[Article]:
        pass

    def get_soup(self) -> BeautifulSoup:

        try:
            cont = Spider().born().get(self.url).text
            return BeautifulSoup(cont, 'html.parser')
        except Exception as e:
            cf.warning(e)
            return BeautifulSoup('', 'html.parser')

    def process(self) -> List[Article]:
        return self.search_articles()


class Aggerate(Component):

    def __init__(self, components: List[Component]) -> None:
        self.components = components

    def process(self) -> List[Article]:
        articles = []
        for component in self.components:
            articles.extend(component.search_articles())
        return articles


def post_news(news_sources: List[Component]):
    pipeline = Pipeline()
    pipeline.add(Aggerate(news_sources))
    pipeline.add(FilterPosted())
    pipeline.add(FilterPostedBM25())
    pipeline.add(FilterEmpty())
    pipeline.add(SaveToDB())
    pipeline.add(PostToTelegram())
    pipeline.add(MarkPostedArticlesToDB())
    pipeline.process()
