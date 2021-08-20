import logging
from strapi import sendThumbnailUrl
from aws import upload, url
from typing import Union
from fastapi import FastAPI
from model import MediaCreate, MediaUpdate
from pprint import pprint
import fitz
import requests
from os import path

app = FastAPI()


def downloadFile(url, fileName):
    with open(fileName, "wb") as file:
        response = requests.get(url)
        file.write(response.content)


def createSvg(page, objectname):
    with open(objectname, "w") as f:
        svgImage = page.get_svg_image(text_as_path=False)
        print("Convertion completed")
        f.write(svgImage)
        print(f"Svg preview created:", objectname)


def createPreview(url, filename, objectname, filetype="svg"):
    downloadFile(url, filename)
    print("PDF file downloaded")
    doc = fitz.open(filename)
    if doc.page_count > 0:
        page = doc[0]
        objectname = "/tmp/thumbnail_" + objectname + f".{filetype}"
        if filetype == "svg":
            createSvg(page, objectname)
        return objectname


def uploadPreview(objectname):
    return upload(objectname)


def createUrl(objectname):
    return url(objectname)


@app.post("/")
async def handler(payload: MediaCreate):
    if payload.event == "media.create" and payload.media.mime == "application/pdf":
        name = payload.media.name
        hash = payload.media.hash
        id = payload.media.id
        filename = "/tmp/" + name
        objectname = path.basename(hash)
        url = payload.media.url

        objectname = createPreview(url, filename, objectname)
        if objectname:
            uploadPreview(objectname)
            imageUrl = createUrl(path.basename(objectname))
            sendThumbnailUrl(id, objectname, imageUrl)
