from email import message
import requests
import os
import codefast as cf
from rss.apps.device import DeviceInfo


class BarkErrorAlert(object):
    def __init__(self, title: str, message: str) -> None:
        self.barkhost = cf.b64decode('aHR0cHM6Ly9hcGkuZGF5LmFwcC8zbjhiUzZKNU1XSlBWS1h2a2ZVR1JZCg==')
        self.icon = 'https://s3.bmp.ovh/imgs/2022/04/13/9b774ff9ca72aea3.png'
        self.title = title
        self.message = message

    def send(self):
        try:
            msg = f'{DeviceInfo()}: {self.message}'
            path = f'{self.barkhost}/{self.title}/{msg}?icon={self.icon}'
            path = path.replace(' ', '%20')
            requests.post(path)
        except Exception as e:
            cf.error(f'{self.__class__.__name__}: {e}')


class ErrorAlert(object):
    @classmethod
    def send(cls, title: str, message: str):
        BarkErrorAlert(title, message).send()
