from rss.base.anynews import Article, AnyNews
from typing import List
import base64

class DummyItem(object):
    def __init__(self):
        self.text = 'dummy'

class LeiPhoneAI(AnyNews):
    def __init__(self):
        self.url = 'https://leiphone.com/category/ai'
        self.type = 'anynews:leiphone'

    def search_articles(self) -> List[Article]:
        articles = []
        soup = self.get_soup()
        for div in soup.find_all('div', class_='word'):
            article = Article()
            title = div.find('a', class_='headTit') or DummyItem()
            date = div.find('div', class_='time') or DummyItem()
            author = div.find('a', class_='aut') or DummyItem()
            url = div.find('a').get('href')
            article = Article(title=title.text.strip(),
                              uid=base64.b64encode(
                                  url.encode('utf-8')).decode('utf-8'),
                              url=url,
                              author=author.text.strip(),
                              date=date.text.strip(),
                              extra_url=url)
            articles.append(article)
        return articles
