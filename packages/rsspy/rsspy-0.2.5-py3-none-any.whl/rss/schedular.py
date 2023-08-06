import socket
import time

from codefast.concurrent.scheduler import BackgroundScheduler

from rss.apps.dropbox_monitor import api as rent_monitor
from rss.apps.freeapp import free_ios_app_feeds
from rss.apps.huggingface import HuggingFace
from rss.apps.leiphone import LeiPhoneAI
from rss.apps.rsshub import rsshub_pipe
from rss.base.anynews import post_news

socket.setdefaulttimeout(300)


def rsspy():
    components = [LeiPhoneAI(), HuggingFace()]
    post_news(components)


def rss():
    BackgroundScheduler(trigger='interval', interval=180) \
        .add_job(free_ios_app_feeds)\
        .start()

    BackgroundScheduler(trigger='interval', interval=20) \
        .add_job(rent_monitor)\
        .start()

    BackgroundScheduler(trigger='cron', hour='9-21', minute='01') \
        .add_job(rsspy) \
        .add_job(rsshub_pipe) \
        .start()


if __name__ == '__main__':
    rss()
    while True:
        time.sleep(1)
