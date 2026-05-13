import os
import time
import re
import json
import subprocess
import sys


# 设置控制台编码为UTF-8
def set_console_encoding():
    if sys.platform == 'win32':
        try:
            os.system('chcp 65001 > nul')
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
            print("控制台编码已设置为UTF-8")
        except Exception as e:
            print(f"设置编码时警告: {e}")


set_console_encoding()

# 进入目录
customDir = input('输入文件夹绝对路径：')
customDir = os.path.abspath(customDir)
os.chdir(customDir)


# 检查output文件夹
def mkDir():
    output_dir = os.path.join(customDir, 'output')
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        print('output文件夹创建成功,合并后的文件将会被移动到output文件夹')
    else:
        print('output文件夹已存在,合并后的文件将会被移动到output文件夹')
    return output_dir


output_dir = mkDir()

# FFmpeg路径配置
ffmpeg_path = 'ffmpeg'


# 清理文件名
def clean_filename(filename):
    if not filename:
        return '未命名视频'
    # 保留汉字、字母、数字、下划线和点，移除其他非法字符
    cleaned_name = re.sub(r'[^\w\.\u4e00-\u9fa5]', '', filename)
    cleaned_name = cleaned_name.replace(' ', '')
    cleaned_name = cleaned_name.strip('.')
    # 限制长度，避免Windows路径过长
    if len(cleaned_name) > 100:
        cleaned_name = cleaned_name[:100]
    return cleaned_name if cleaned_name else '未命名视频'


def run_ffmpeg_command(cmd):
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',
            errors='ignore'
        )
        if result.stderr and "Press [q] to stop" not in result.stderr:
            print(f"FFmpeg错误信息: {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"执行FFmpeg命令失败: {e}")
        return False


def Main():
    for root, dirs, files in os.walk('.'):
        if 'entry.json' in files:
            entry_json_path = os.path.join(root, 'entry.json')
            print(f'\n========== 处理 {entry_json_path} ==========')

            try:
                # 读取并解析entry.json
                with open(entry_json_path, encoding='utf-8') as entryFile:
                    entry_data = json.load(entryFile)

                # 读取page_data下的part字段
                # 提取基础信息
                title = entry_data.get('title', '未命名视频').strip()
                # 从page_data里读part（分P标识）
                page_data = entry_data.get('page_data', {})
                part = page_data.get('part', '').strip()
                download_subtitle = entry_data.get('download_subtitle', '').strip()

                # 确定最终文件名（优先级：part > download_subtitle > title）
                if part:
                    # 用「主标题 - 分P标题」作为文件名
                    video_name = f"{title} - {part}"
                    print(f'读取到分P标识: {part}')
                    print(f'最终文件名: {video_name}')
                elif download_subtitle:
                    video_name = download_subtitle
                    print(f'使用download_subtitle作为文件名: {video_name}')
                else:
                    video_name = title
                    print(f'使用主标题作为文件名: {video_name}')

                # 清理文件名
                cleaned_videoName = clean_filename(video_name)
                print(f'清理后的文件名: {cleaned_videoName}')

                # 查找m4s文件
                audioFile = None
                videoFile = None
                for sub_root, sub_dirs, sub_files in os.walk(root):
                    if 'audio.m4s' in sub_files and 'video.m4s' in sub_files:
                        audioFile = os.path.abspath(os.path.join(sub_root, 'audio.m4s'))
                        videoFile = os.path.abspath(os.path.join(sub_root, 'video.m4s'))
                        print(f'找到音频文件: {audioFile}')
                        print(f'找到视频文件: {videoFile}')
                        break

                if not audioFile or not videoFile:
                    print(f'未找到audio.m4s或video.m4s，跳过该分P')
                    continue

                # 拼接输出路径
                output_mp4 = os.path.join(root, f'{cleaned_videoName}.mp4')
                # FFmpeg合并命令
                ffmpeg_cmd = f'"{ffmpeg_path}" -i "{videoFile}" -i "{audioFile}" -c copy -y "{output_mp4}"'
                print(f'执行FFmpeg命令: {ffmpeg_cmd[:100]}...')  # 截断长命令，避免日志刷屏

                # 执行合并
                ffmpeg_success = run_ffmpeg_command(ffmpeg_cmd)
                if not ffmpeg_success or not os.path.exists(output_mp4):
                    print(f'合并失败，未生成 {output_mp4}')
                    continue

                # 仅当文件真的重复时加时间戳（现在分P名不同，基本不会触发） ==========
                target_mp4 = os.path.join(output_dir, f'{cleaned_videoName}.mp4')
                if os.path.exists(target_mp4):
                    timestamp = int(time.time())
                    target_mp4 = os.path.join(output_dir, f'{cleaned_videoName}_{timestamp}.mp4')
                    print(f'目标文件已存在，添加时间戳后缀: {target_mp4}')

                # 移动文件
                try:
                    os.replace(output_mp4, target_mp4)
                    print(f'合并成功，文件路径: {target_mp4}')
                except Exception as e:
                    print(f'移动文件失败: {e}')
                    print(f'文件仍保存在: {output_mp4}')

                time.sleep(1)

            except json.JSONDecodeError:
                print(f'{entry_json_path} 不是有效的JSON文件，跳过')
                continue
            except Exception as e:
                print(f'处理 {entry_json_path} 时出错: {str(e)}')
                continue


def doneMessage():
    print('\n========== 所有文件处理完成 ==========')
    print('请查看output文件夹获取合并后的视频')


if __name__ == '__main__':
    Main()
    doneMessage()
