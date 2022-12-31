import requests


class WebhookClient:
    def __init__(self, url):
        self.webhook_url = url

    def send(self, data):
        requests.post(self.webhook_url, json=data)

    def send_embed(self, **kwargs):
        self.send({
            "embeds": [
                kwargs
            ]
        })
