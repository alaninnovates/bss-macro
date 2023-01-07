import requests


def send_embed(webhook_url, **kwargs):
    if not webhook_url:
        return
    requests.post(webhook_url, json={
        "embeds": [
            kwargs
        ]
    })
