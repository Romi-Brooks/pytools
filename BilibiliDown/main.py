import os

def GetUrl():
    # 获取链接
    url = input("请输入链接：")
    return url

def GetAllVideoLink(url):
    # 使用BBDown获取所有视频链接
    os.system("BBDown " + url)

def ProcessTxtFile():
    # 检查目录中生成的txt文件
    for file in os.listdir():
        if file.endswith(".txt"):
            filename= file
    # 打开txt文件
    file = open(file, "r")
    # 读取txt文件
    lines = file.readlines()
    # 去除换行符
    for i in range(len(lines)):
        lines[i] = lines[i].strip('\n')
    # 获取文件行数
    lineCount = len(lines)
    print("共有" + str(lineCount) + "个视频")
    # 逐行取得视频链接
    videoLinks = []
    for line in lines:
        videoLinks.append(line.split(" ")[0])
    # 删除txt文件
    os.remove(filename)
    return videoLinks

def DownloadVideo(videoLinks):
    # 下载视频
    print("开始下载")
    for videoLink in videoLinks:
        print("正在下载：" + videoLink)
        os.system("BBDown " + "\"" + videoLink + "\"")
        print("下载完成")


if __name__ == '__main__':
    url = GetUrl()
    GetAllVideoLink(url)
    videoLinks = ProcessTxtFile()
    DownloadVideo(videoLinks)