
RSS_URLS = [
    ('https://openai.com/blog/rss/', 'openai'),
    ('https://www.aitrends.com/feed/', 'aitrends'),
    ('https://venturebeat.com/category/ai/feed/', 'venturebeat'),
    ('https://www.wired.com/category/business/feed/', 'wired'),
    ('https://wanqu.co/feed/', '湾区日报'),
    ('https://feed.cnblogs.com/blog/u/409312/rss/', 'cnblogs-风雨中的小七'),
    ('https://rsshub.app/infoq/recommend', 'infoq'),
    ('https://sspai.com/feed', 'sspai'),
    ('https://rsshub.app/geektime/column/48', 'geektime'),
    ('https://rsshub.app/juejin/category/ai', '掘金AI'),
    ('https://rsshub.app/meituan/tech/home', '美团技术'),
    ('https://rsshub.app/blogs/paulgraham', 'PaulGraham'),
    ('https://www.msra.cn/feed', 'MSRADeepLearningArticles'),
    ('http://ai.stanford.edu/blog/feed.xml', 'standford nlp'),
    ('https://nullprogram.com/feed/', 'endless_author'),
    # ('https://kexue.fm/feed', '科学空间'),
    # ('https://stackoverflow.com/feeds/tag/nlp', 'StackoverFlowNLP'),
    # ('https://stackoverflow.com/feeds/tag/keras', 'StackOverFlowKeras'),
    # ('http://www.dydhhy.com/rsslatest.xml', '电影后花园'),
    # ('https://techcrunch.com/feed/', 'techcrunch'),
    # ('https://www.theverge.com/rss/frontpage', 'theverge'),
    # ('https://www.wired.com/feed/rss', 'wired'),
    ('https://rsshub.app/nasa/apod', 'NASADailyPicture'),
    ('https://sspai.com/feed', '少数派'),
    ('https://machinelearningmastery.com/feed/', 'mlmastery'),
    # ('https://nitter.it/seanwei001/rss', 'Twitter-seanwei001'),
    ('https://bird.trom.tf/Norathen/rss', 'Twitter-Norathen'),
    # ('https://bird.trom.tf/StephenKing/rss', 'Twitter-stephen-king'),
    ('https://bird.trom.tf/stanfordnlp/rss', 'Twitter-StanfordNLP'),
    # ('https://nitter.it/binanbijo_sekai/rss', 'Twitter-sekai'),
    ('https://cdn.werss.weapp.design/api/v1/feeds/dbea39f3-7e43-4df9-9f86-e78f4690ee10.xml', 'geekpark'),
    ('https://cdn.werss.weapp.design/api/v1/feeds/e7651950-5b24-4487-9995-b0b3468ea392.xml', 'almosthuman'),
    ('https://cdn.werss.weapp.design/api/v1/feeds/f63ef4b7-c6c4-4a94-8652-62a228a759c8.xml', 'ai_front'),
    ('https://cdn.werss.weapp.design/api/v1/feeds/e83b0f63-5c84-45f6-a44e-a5e1b1ea87f9.xml', 'paperweekly'),
    ('https://cdn.werss.weapp.design/api/v1/feeds/04db1eb7-f7b8-417d-8f42-5119feeb443e.xml', 'infoQ'),
    ('https://cdn.werss.weapp.design/api/v1/feeds/9e44c20a-b61b-44c6-9afd-800dd09a7508.xml', 'AIstuff'),
    ('https://cdn.werss.weapp.design/api/v1/feeds/1cfea1ef-3df6-47b1-9fd4-7f82ca026dd0.xml', 'TencentTech'),
    ('https://cdn.werss.weapp.design/api/v1/feeds/1c52f62d-1c3f-4fd5-9ffb-142253470fb9.xml', 'AINLP'),
    ('https://cdn.werss.weapp.design/api/v1/feeds/7ed2ef11-519c-4ea9-901b-6cf5cff952da.xml', '夕小瑶')
]

from rss.auth import auth 
WECHAT_PUBLIC = {
    'yuntoutiao': {
        'main_url': auth.werss_yuntoutiao,
        'source': '云头条',
        'sub_type': 'yuntoutiao',
    },
    'huxiu': {
        'main_url': 'https://www.wxkol.com/show/huxiu_com.html',
        'source': '虎嗅网',
        'sub_type': 'huxiu',
    },
}

TELEGRAM = {'bot_name': 'hema_bot', 'channel_name': 'global_news_podcast'}
