# by hx7 cyber team



import requests
import datetime

today = datetime.date.today()


def sendMsg(webhook, message):

    webhook = webhook

    alert = {
        "avatar_url":"https://i.imgur.com/tavZoYq.gif",
        "name":"hx7 Team",
        "embeds": [
            {
                "author": {
                    "name": "hx7 Team Bot",
                    "url": "https://github.com/hx7CyBerTeam"
                    },
                "description": message,
                "color": 14177041,
                "footer": {
                  "text": f"this message was send at・{today}"
                }
            }
        ]
    }
    requests.post(webhook, json=alert)