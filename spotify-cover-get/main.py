import os
import wget
import json

def convert():
    print("输入从Spotify所获取到的分享连接：")
    orin_url = input()
    get_url = "https://open.spotify.com/oembed?url="
    global true_url
    true_url = get_url + orin_url
convert()

def download_Source():
    print("开始下载源文件...")
    wget.download(true_url, "source.json")
    print("源文件下载完成！")
download_Source()

def analyse():
    print("查找Title,Cover Url...")
    with open("source.json", "r") as f:
        global title
        global cover_url
        data = json.load(f)
        title = data["title"]
        cover_url = data["thumbnail_url"]
        print("Title: " + title)
        print("Cover Url: " + cover_url)
        # 删除source.json
        os.remove("source.json")
analyse()

def download():
    print("开始下载封面...")
    wget.download(cover_url, title + ".jpg")
    print("封面下载完成！")
download()