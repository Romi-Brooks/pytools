# 一个自用的Python小工具库
## all-video-in-one
### 将一个文件夹下的所有视频文件合并成一个视频文件
#### 环境准备
##### Python 环境：
确保已安装 Python（代码适用于 Python 3.x）。

##### FFmpeg 工具：

确保系统中已安装 ffmpeg，并且可以通过命令行访问。

#### 文件目录结构：

在运行代码的目录下，创建一个名为 videos 的文件夹，并将需要合并的视频文件放入其中。

确保视频文件格式是 ffmpeg 支持的格式（如 .mp4、.avi 等）。

#### 运行代码

打开终端或命令提示符，导航到保存代码的目录。

```bash
python main.py
```

#### 输出结果
合并后的视频文件会保存在 outVideos 文件夹中，文件名是当前时间字符串。

如果 videos 文件夹为空或不存在，代码会打印相应的提示信息。

## (NSFW) free4_get
#### 环境准备
##### Python 环境：
确保已安装 Python 3.x。
##### 依赖库：
安装 requests 库（如果尚未安装）：
```bash
pip install requests
```
#### 运行代码
打开终端或命令提示符，导航到保存代码的目录。
```bash
python main.py
```
在程序启动后，输入以下命令之一：

today：获取网站的最新内容。

search：搜索网站上的内容。

help 或 ?：获取帮助信息。

exit：退出程序。

#### 示例操作
##### 获取最新内容：

输入 today，会从网站获取最新内容

#####  搜索内容：
输入 search，会提示用户输入搜索关键词，返回与关键词匹配的内容。

## (NSFW) Getpic
#### 环境准备
##### Python 环境：
确保已安装 Python 3.x。
##### 依赖库：
安装 requests, wget 库（如果尚未安装）：
```bash
pip install wget
```
#### 运行代码
打开终端或命令提示符，导航到保存代码的目录。
```bash
python main.py
```

#### 示例操作
输入a：下载全站随机图片。  
输入b：下载全站随机图片（无NSFW，即不含成人内容）。  
输入c：下载MirlKoi推荐的图片。  
输入d：下载横屏图片。  
输入e：下载竖屏图片。  

如果输入错误，脚本会提示用户重新输入。  

> 下载的图片会以当前时间戳命名（格式为YYYY-MM-DD-HH-MM-SS.jpg），并保存到img文件夹中。  

## Let-m4s-together  / 哔哩哔哩缓存视频合并
#### 环境准备
##### Python 环境：
确保已安装 Python 3.x。
##### 依赖库：
确保系统能够调用ffmpeg

#### 运行代码
打开终端或命令提示符，导航到保存代码的目录。
```bash
python main.py
```

#### 示例操作
输入文件夹路径  
输入包含entry.json文件和audio.m4s/video.m4s文件的文件夹的绝对路径。  


## spotify-cover-get
#### 环境准备
##### Python 环境：
确保已安装 Python 3.x。
##### 依赖库：
安装wget 库（如果尚未安装）：
```bash
pip install wget
```
#### 运行代码
打开终端或命令提示符，导航到保存代码的目录。
```bash
python main.py
```

#### 示例操作
输入Spotify分享链接  
输入一个Spotify的分享链接（例如：https://open.spotify.com/track/ 或 https://open.spotify.com/album/）。