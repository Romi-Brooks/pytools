import os
import time
import re

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

# 确保ffmpeg路径正确
# 如果ffmpeg已添加到PATH，可以直接使用'ffmpeg'
ffmpeg_path = 'ffmpeg'  # 如果未添加到PATH，请替换为ffmpeg的完整路径，例如 r'C:\path\to\ffmpeg\bin\ffmpeg.exe'

# 清理文件名，保留汉字、字母、数字、下划线和点，去掉空格和其他不规范字符
def clean_filename(filename):
    # 保留汉字、字母、数字、下划线和点
    cleaned_name = re.sub(r'[^\w\.\u4e00-\u9fa5]', '', filename)
    # 去掉空格
    cleaned_name = cleaned_name.replace(' ', '')
    # 去掉开头和结尾的点
    cleaned_name = cleaned_name.strip('.')
    return cleaned_name

def Main():
    # 从当前的文件夹下查找entry.json文件
    for folderName, folders, filenames in os.walk('.'):
        if 'entry.json' in filenames:
            os.chdir(folderName)
            # 读取entry.json文件,输出获取到的文件夹名称
            print('找到了entry.json:' + folderName)
            with open('entry.json', encoding='utf-8') as entryFile:
                entryFileContent = entryFile.read()

            # 从entry.json文件中查找"title"字段
            if '"title":' in entryFileContent:
                videoName = entryFileContent.split('"title":')[1].split('"')[1]

            # 清理视频名称
            cleaned_videoName = clean_filename(videoName)
            print('原始视频名称: ' + videoName)
            print('清理后的视频名称: ' + cleaned_videoName)

            # 查找当前目录下所有文件夹内是否含有audio.m4s和video.m4s文件
            for folderName, folders, filenames in os.walk('.'):
                if 'audio.m4s' in filenames and 'video.m4s' in filenames:
                    audioFile = os.path.abspath(os.path.join(folderName, 'audio.m4s'))
                    videoFile = os.path.abspath(os.path.join(folderName, 'video.m4s'))
                    print('找到了audio.m4s文件,路径为：' + audioFile)
                    print('找到了video.m4s文件,路径为：' + videoFile)

            # 使用ffmpeg合并音频与视频
            os.system(f'ffmpeg -i "{videoFile}" -i "{audioFile}" -codec copy "{cleaned_videoName}.mp4"')
            # 移动生成文件到工作目录下的output文件夹
            os.system(f'move "{cleaned_videoName}.mp4" "{customDir}\\output"')
            print('合并完成,文件名为：' + cleaned_videoName + '.mp4')
            print('文件已移动到output文件夹')
            # 延迟五秒
            time.sleep(5)
            # 退回上级目录继续执行
            os.chdir('../..')

def doneMessage():
    print('所有文件已合并完成,请查看output文件夹')

Main()
doneMessage()
