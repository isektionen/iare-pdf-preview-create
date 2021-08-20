import json
from os import getenv, path
import requests


def init():
    url = "https://cms.iare.se/remote-services/init"
    body = {"email": getenv("EMAIL"), "password": getenv("PASSWORD")}
    response = requests.post(url, data=body)
    return response.text


def sendThumbnailUrl(id, objectname, providerUrl):
    url = "https://cms.iare.se/remote-services/thumbnail"
    name = path.basename(objectname)
    ext = "." + name.split(".")[-1]
    _hash = name.replace(ext, "")
    size = int(path.getsize(objectname)) / 100
    body = {
        "id": id,
        "url": providerUrl,
        "name": name,
        "ext": ext,
        "hash": _hash,
        "path": None,
        "width": None,
        "height": None,
        "size": size,
    }
    token = init()
    response = requests.put(url, data=body, headers={"Authorization": f"Bearer {token}"})
    print("Strapi response:", response.text)