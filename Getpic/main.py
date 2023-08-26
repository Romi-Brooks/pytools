import os
import time
import wget
from datetime import datetime

print("api来自MirlKoi,单个ip在60s请求120次会被拉黑")
print("因此做了延迟,每5s下载一次")
print("请选择下载的图片类型")
print("a. 全站随机")
print("b. 全站随机(无NSFW)")
print("c. MirlKoi推荐")
print("d. 横屏")
print("e. 竖屏")

def urlSelect():
    while True:
        a = input("请输入选项:")
        if a == "a":
            url = "https://iw233.cn/api.php?sort=random"
            break
        elif a == "b":
            url = "https://iw233.cn/api.php?sort=iw233"
            break
        elif a == "c":
            url = "https://iw233.cn/api.php?sort=top"
            break
        elif a == "d":
            url = "https://iw233.cn/api.php?sort=pc"
            break
        elif a == "e":
            url = "https://iw233.cn/api.php?sort=mp"
            break
        else:
            print("输入错误，请重新输入")
    return url

trueUrl = urlSelect()

def mkDir():
    if not os.path.exists("img"):
        os.mkdir("img")
        print("创建img文件夹成功")
        print("文件将下载到img文件夹中")
    else:
        print("文件将下载到img文件夹中")
mkDir()

def getFileName():
    dt02 = datetime.today()
    return dt02.strftime("%Y-%m-%d-%H-%M-%S") + ".jpg"

def downloadFile():
    while True:
        print("开始下载")
        file_name = wget.download(trueUrl, out=getFileName())
        print("文件名: ", getFileName())
        os.rename(file_name, "img/" + file_name)
        time.sleep(5)

downloadFile()
