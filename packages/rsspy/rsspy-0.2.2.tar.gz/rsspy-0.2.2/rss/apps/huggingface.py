import codefast as cf
from rss.base.anynews import Article, AnyNews
from typing import List
import re
from bs4 import BeautifulSoup
import base64
import requests

class HuggingFace(AnyNews):
    def __init__(self):
        self.url =  'https://huggingface.co/blog/'
        self.type = 'anynews:huggingface'

    def search_articles(self) -> List[Article]:
        soup = requests.get(self.url).text
        blogs = []
        for div in soup.split("\n"):
            if re.search(
                    r'flex lg:col-span-1 flex-col group overflow-hidden relative border-gray-100 rounded-xl border shadow-sm hover:shadow-alternate transition-shadow',
                    div):
                blog = re.search(r'(/blog/.*?)\"', div)
                if blog:
                    blogs.append([blog.group(1)])

            if re.search(
                    r'font-semibold group-hover:underline font-serif text-xl',
                    div):
                soup = BeautifulSoup(div, 'html.parser')
                title = soup.find('h2').text.strip()
                blogs[-1].append(title)

        articles = []
        for blog in blogs:
            if len(blog) < 2:
                continue
            uid = base64.b64encode(blog[0].encode('utf-8')).decode('utf-8')
            url = cf.urljoin(self.url, blog[0].replace('blog/', ''))
            articles.append(Article(uid=uid, title=blog[1], url=url))
        return articles
