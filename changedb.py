import sqlite3
import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
import base64
from PIL import Image
import io
import new_requests

dbpath = "./db.sqlite3"

def download(url: str) -> bytes:
    # this might be not downloadable
    req = new_requests.get(url, retries=5)
    return req.content

def url_to_blob(src: str) -> str:
    images: bytes = download(src)
    base64images: bytes = base64.standard_b64encode(images)
    t: str = Image.open(io.BytesIO(images)).format.lower() # "jpeg", "png", etc
    print(f"image type: {t}")
    new_src = f"data:image/{t};base64,{base64images.decode()}"
    return new_src

with sqlite3.connect(dbpath) as conn:
    c = conn.cursor()
    c.execute('SELECT id, body FROM myapp_excardinfo')
    bodylist: [tuple] = c.fetchall()

no_downloaded = []
with sqlite3.connect(dbpath) as conn:
    c = conn.cursor()
    for id, body in bodylist:
        if 'src="http' in body: # lazy
            soup = BeautifulSoup(body, 'html.parser')
            imgs: [Tag] = soup.find_all('img')
            for img_tag in imgs:
                src: str = img_tag["src"]
                # src should start with "https or http",  otherwise ignore
                if src[:4] == "http":
                    print(f"url to download: {src}")
                    try:
                        new_src: str = url_to_blob(src)
                    except:
                        print(f"no downloaded. {(id, src)} Skip")
                        no_downloaded.append((id, src))
                        continue
                    print(f"blob to update: {new_src[:40]} ..")
                    print()
                    # update soup
                    img_tag["src"] = new_src
            new_body = str(soup)
            c.execute('UPDATE myapp_excardinfo SET body = ? WHERE id = ?', (new_body, id))


print(f"no downloaded, {no_downloaded}")
print("finished")
