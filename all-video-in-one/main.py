import os
import time

def getFileName():
    #查找videos文件夹下的所有文件,如果没找到就打印 无法寻找到videos文件夹
    if not os.path.exists('videos'):
        print('无法寻找到videos文件夹')
        return
    #获取videos文件夹下的所有文件
    files = os.listdir('videos')
    #进入videos文件夹
    os.chdir('videos')
    #将文件名存入一个名为tempfile.txt的文件中
    with open('tempfile.txt', 'w') as f:
        for file in files:
            f.write("file " + "'" + file + "'" +'\n')

def letVideosTogether():
    #获取到当前时间,打印时间
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    #使用ffmpeg将tempfile.txt中的文件合并,文件名为 当前时间.mp4
    os.system("ffmpeg -f concat -i tempfile.txt -c copy " + now + ".mp4")
    #取得文件名
    global fileName
    fileName = now + ".mp4"
    #删除tempfile.txt
    os.system('rm tempfile.txt')
    print('视频合并完成')

def moveVideos():
    #返回上级目录
    os.chdir('..')
    #检查outVideos文件夹是否存在,不存在则创建
    if not os.path.exists('outVideos'):
        os.mkdir('outVideos')
    #进入videos文件夹
    os.chdir('videos')
    # 将合并后的视频移动到outVideos文件夹下
    os.system("mv " + fileName + " ../outVideos")
    print('视频移动完成')
    print('输出文件夹为outVideos')

if __name__ == '__main__':
    getFileName()
    letVideosTogether()
    moveVideos()

