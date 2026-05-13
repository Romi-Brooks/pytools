import os
import requests

baseUrl = "https://free4.xyz"
SearchUrl = "https://free4.xyz/?s="

def Log(StatusCode, StatusMessage):
    # Log Function
    # INIT STATUS CODE
    # LogInfo = 0
    # LogWarning = 1
    # LogError = 2

    if StatusCode == 0:
        print("\033[1;32;40m" + "[INFO]" + "\033[0m" + ":" + StatusMessage)
    elif StatusCode == 1:
        print("\033[1;33;40m" + "[WARNING]" + "\033[0m" + ":" + StatusMessage)
    elif StatusCode == 2:
        print("\033[1;31;40m" + "[ERROR]" + "\033[0m" + ":" + StatusMessage)
    else:
        print("\033[1;35;40m" + "[UNKNOWN]" + "\033[0m" + ":" "Log Status Code is Not Defined")

def Log_Debug():
    Log(StatusCode=0, StatusMessage="Log Debug Mode")
    print("======================================================================")
    print("# INIT STATUS CODE")
    print("# LogInfo = 0")
    print("# LogWarning = 1")
    print("# LogError = 2")
    while True:
        Log(StatusCode=0, StatusMessage="Please Input Log Status Code:")
        Log(StatusCode=int(input()), StatusMessage="Log Debug Message:")

def today_solve():
    Log(StatusCode=0, StatusMessage="Getting Website Content...")
    solve_url()


def solve_url():
    # Get Main HTML Page
    r = requests.get(baseUrl)
    if r.status_code == 200:
        Log(StatusCode=0, StatusMessage="Get HTML Page Success")
        with open('index.html', 'w') as f:
            f.write(r.text)
    else:
        Log(StatusCode=2, StatusMessage="Get HTML Page Failed, Bad Code " + str(r.status_code))

        #查找文件中含有<a class="overlay-link" 的行，保存
    with open('index.html', 'r') as f:
        for line in f:
            if '<a class="overlay-link"' in line:
                with open('today_result.txt', 'a') as f:
                    f.write(line)
    today_resultCall()

    os.remove('index.html')

def today_resultCall():
    #创建列表
    resultTitleList = []
    resultHrefList = []
    with open('today_result.txt', 'r') as f:
        for i in range(5):
            # 取得aria-label标签的内容
            resultTitle = f.readline().split('aria-label="')[1].split('"')[0]
            # 取得href标签的内容
            resultHref = f.readline().split('href="')[1].split('"')[0]
            #存入列表
            resultTitleList.append(resultTitle)
            resultHrefList.append(resultHref)
    # 处理搜索结果的名字
    for i in range(5):
        resultTitleList[i] = resultTitleList[i].replace("&#8211;", "-")
        resultTitleList[i] = resultTitleList[i].replace("&#8217;", "'")
        resultTitleList[i] = resultTitleList[i].replace("&#038;", "&")
        resultTitleList[i] = resultTitleList[i].replace("&#8216;", "'")
        resultTitleList[i] = resultTitleList[i].replace("&#8220;", '"')
        resultTitleList[i] = resultTitleList[i].replace("&#amp;", "&")

    # 将resultTitleList逐行打印，并且标上序号
    for i in range(5):
        print(str(i) + "." + resultTitleList[i])

    # TIPS
    with open('today_result.txt', 'r') as f:
        if "aria-label" in f.read():
            with open('today_result.txt', 'r') as f:
                # 获取文件行数
                line_num = len(f.readlines())
                # print(line_num)
                if line_num == 0:
                    Log(StatusCode=2, StatusMessage="Something Wrong")
            Log(StatusCode=0, StatusMessage="There are a total of " + str(line_num) + " results for this page, only five are shown")
            Log(StatusCode=0, StatusMessage="More Results: " + baseUrl)
        else:
            Log(StatusCode=2, StatusMessage="No Result Found ,Something Wrong")

    # 选择序号,如果选择5则为全选
    while True:
        select = input("Please Select, 0-4 or 5 for all: ")
        if select == "5":
            for i in range(5):
                print("======================================================================")
                print("Title:" + resultTitleList[i])
                print("Url:" + resultHrefList[i])
                getResultNetPanUrl(resultHrefList[i])
            break
        elif select == "0":
            print("======================================================================")
            print("Title:" + resultTitleList[0])
            print("Url:" + resultHrefList[0])
            getResultNetPanUrl(resultHrefList[0])
            break
        elif select == "1":
            print("======================================================================")
            print("Title:" + resultTitleList[1])
            print("Url:" + resultHrefList[1])
            getResultNetPanUrl(resultHrefList[1])
            break
        elif select == "2":
            print("======================================================================")
            print("Title:" + resultTitleList[2])
            print("Url:" + resultHrefList[2])
            getResultNetPanUrl(resultHrefList[2])
            break
        elif select == "3":
            print("======================================================================")
            print("Title:" + resultTitleList[3])
            print("Url:" + resultHrefList[3])
            getResultNetPanUrl(resultHrefList[3])
            break
        elif select == "4":
            print("======================================================================")
            print("Title:" + resultTitleList[4])
            print("Url:" + resultHrefList[4])
            getResultNetPanUrl(resultHrefList[4])
            break
        else:
            Log(StatusCode=2, StatusMessage="Input Error!")

    # 删除today_result.txt
    os.remove('today_result.txt')

def search_url():
    # Get Search HTML Page
    KeyWord = input("Please Input KeyWord:")
    TrueSearchUrl = SearchUrl + KeyWord
    print("Searching...")
    # print(TrueSearchUrl)
    r = requests.get(TrueSearchUrl)
    if r.status_code == 200:
        # 写入内容到search.html
        with open('search.html', 'w') as f:
            f.write(r.text)
    else:
        Log(StatusCode=2, StatusMessage="Get HTML Page Failed, Bad Code " + str(r.status_code))

    # 查找文件中含有<h2 class="penci-entry-title entry-title grid-title">的行，保存
    with open('search.html', 'r') as f:
        for line in f:
            if '<a class="penci-image-holder penci-lazy"' in line:
                with open('search_result.txt', 'a') as f:
                        f.write(line)

    # 查看文件，如果有KeyWord则调用log函数
    with open('search_result.txt', 'r') as f:
        if KeyWord in f.read():
            with open('search_result.txt', 'r') as f:
                # 获取文件行数
                line_num = len(f.readlines())
                # print(line_num)
                if line_num == 0:
                    Log(StatusCode=2, StatusMessage="Something Wrong")
            search_resultCall()
            Log(StatusCode=0, StatusMessage="There are a total of " + str(line_num) + " results for this page, only five are shown")
            Log(StatusCode=0, StatusMessage="More Results: " + TrueSearchUrl)
            Log(StatusCode=0, StatusMessage="Search Success")
        else:
            search_resultDelete()
            Log(StatusCode=1, StatusMessage="No Result Found")
            Log(StatusCode=1, StatusMessage="Please check what you have entered")

    os.remove('search.html')

def search_resultCall():
    # Get Title And Url
    with open('search_result.txt', 'r') as f:
        for i in range(5):
            print("======================================================================")
            #取得title标签的内容
            resultTitle = f.readline().split('title="')[1].split('"')[0]
            resultTitle = search_resultNameProcess(resultTitle)
            print("Title:" + resultTitle)
            #取得href标签的内容
            resultHref = f.readline().split('href="')[1].split('"')[0]
            print("Url:" + resultHref)
            getResultNetPanUrl(resultHref)
    print("======================================================================")
    search_resultDelete()

def getResultNetPanUrl(Href):
    # Get NetCloud Download URL
    r = requests.get(Href)
    if r.status_code == 200:
        with open('result.html', 'w') as f:
            f.write(r.text)

    # 查找文件中的<p>KatFile Download Link</p>这一行，打印下面一行
    with open('result.html', 'r') as f:
        for line in f:
            if '<p>KatFile Download Link</p>' in line:
                KatFileresultNetCloudHref = f.readline().split('href="')[1].split('"')[0]
                print("KatFile Download Url:" + KatFileresultNetCloudHref)

    # 查找文件中的<p>RapidGator Download Link</p>这一行，打印下面一行
    with open('result.html', 'r') as f:
        for line in f:
            if '<p>RapidGator Download Link</p>' in line:
                RapidGatorResultNetCloudHref = f.readline().split('href="')[1].split('"')[0]
                print("RapidGator Download Url:" + RapidGatorResultNetCloudHref)

    # 查找文件中的<p>NitroFlare Download Link</p>这一行，打印下面一行
    with open('result.html', 'r') as f:
        for line in f:
            if '<p>NitroFlare Download Link</p>' in line:
                NitroFlareResultNetCloudHref = f.readline().split('href="')[1].split('"')[0]
                print("NitroFlare Download Url:" + NitroFlareResultNetCloudHref)

    os.remove('result.html')


def search_resultNameProcess(Name):
    # 处理搜索结果的名字
    # 写的稀烂
    Name = Name.replace("&#8211;", "-")
    Name = Name.replace("&#8217;", "'")
    Name = Name.replace("&#038;", "&")
    Name = Name.replace("&#8216;", "'")
    Name = Name.replace("&#8220;", '"')
    Name = Name.replace("&#amp;", "&")
    return Name

def search_resultDelete():
    os.remove('search_result.txt')

def MainFunction_Help():
    print("search : Search the website for the content you want")
    print("today : Get the latest content on the website")
    print("help : Get help")
    print("exit : Exit the program")

if __name__ == '__main__':
    Log(StatusCode=0, StatusMessage="Init Complete")
    print("Use help or ? to get some help")

    # MAKE CHOICE
    while True:
        Input = input(">>>")
        if Input == "help":
            MainFunction_Help()
        elif Input == "?":
            MainFunction_Help()
        elif Input == "today":
            today_solve()
        elif Input == "search":
            search_url()
        elif Input == "exit":
            Log(StatusCode=0, StatusMessage="Exit")
            break
        elif Input == "LOG_DEBUG_MOD":
            Log_Debug()
            break
        else:
            Log(StatusCode=1, StatusMessage="Please enter the correct command")
