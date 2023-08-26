import os
import time

# 进入目录
customDir = input('输入文件夹绝对路径：')
os.chdir(customDir)

# 检查是否存在output文件夹
def mkDir():
    if not os.path.exists('output'):
        os.mkdir('output')
        print('output文件夹创建成功,合并后的文件将会被移动到output文件夹')
    else:
        print('output文件夹已存在,合并后的文件将会被移动到output文件夹')
mkDir()

# 测试:
# 打印当前目录
# print(os.getcwd())


def Main():
    # 从当前的文件夹下查找entry.json文件
    for folderName, folders, filenames in os.walk('.'):
        if 'entry.json' in filenames:
            os.chdir(folderName)
            # 读取entry.json文件,输出获取到的文件夹名称
            print('找到了entry.json:' + folderName)
            entryFile = open('entry.json')
            entryFileContent = entryFile.read()
            entryFile.close()

            # 从entry.json文件中查找"download_subtitle":字段
            if '"download_subtitle":' in entryFileContent:
                videoName = entryFileContent.split('"title":')[1].split('"')[1]

            # 查找当前目录下所有文件夹内是否含有audio.m4s和video.m4s文件
            for folderName, folders, filenames in os.walk('.'):
                if 'audio.m4s' in filenames and 'video.m4s' in filenames:
                    audioFile = os.path.abspath(folderName) + '/audio.m4s'
                    videoFile = os.path.abspath(folderName) + '/video.m4s'
                    print('找到了audio.m4s文件,路径为：' + audioFile)
                    print('找到了video.m4s文件,路径为：' + videoFile)
            print('视频名称应是: ' + videoName)
            print('开始将audio.m4s与video.m4s合并为mp4文件, 注意: 合并完成后延迟5s')

            # 使用ffmpeg合并音频与视频
            os.system('ffmpeg -i ' + videoFile + ' -i ' + audioFile + ' -codec copy ' + '"' + videoName + '"' + '.mp4')
            # 移动生成文件到工作目录下的output文件夹
            # print('mv ' +  videoName + '.mp4 ' + customDir + 'output')
            os.system('mv ' + '"' + videoName + '"' + '.mp4 ' + customDir + 'output')
            print('合并完成,文件名为：' + videoName + '.mp4')
            print('文件已移动到output文件夹')
            # 延迟五秒
            time.sleep(5)
            # 退回上级目录继续执行
            os.chdir('../..')

            # 测试
            # 获取完整命令
            # print('ffmpeg -i ' + videoFile + ' -i ' + audioFile + ' -codec copy ' + '"' + videoName + '.mp4"')

Main()

def doneMessage():
    print('所有文件已合并完成,请查看output文件夹')

doneMessage()
