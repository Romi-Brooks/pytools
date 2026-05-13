import os
import re
import time
import json
import subprocess


def clean_filename(filename):
    if not filename:
        return "未命名视频"
    cleaned = re.sub(r'[^\w\.\u4e00-\u9fa5]', '', filename)
    cleaned = cleaned.replace(' ', '')
    cleaned = cleaned.strip('.')
    if len(cleaned) > 100:
        cleaned = cleaned[:100]
    return cleaned if cleaned else "未命名视频"


def run_ffmpeg(cmd, ffmpeg_path="ffmpeg"):
    full_cmd = f'"{ffmpeg_path}" {cmd}'
    try:
        result = subprocess.run(
            full_cmd, shell=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            encoding="utf-8", errors="ignore"
        )
        if result.returncode != 0:
            error_msg = result.stderr.strip() if result.stderr else "未知错误"
            return False, error_msg
        return True, ""
    except Exception as e:
        return False, str(e)


def find_entry_json_paths(root_dir):
    entry_paths = []
    for root, dirs, files in os.walk(root_dir):
        if "entry.json" in files:
            entry_paths.append(os.path.join(root, "entry.json"))
    return entry_paths


def parse_entry_json(entry_path):
    with open(entry_path, encoding="utf-8") as f:
        data = json.load(f)

    title = data.get("title", "未命名视频").strip()
    page_data = data.get("page_data", {})
    part = page_data.get("part", "").strip()
    download_subtitle = data.get("download_subtitle", "").strip()

    if part:
        video_name = f"{title} - {part}"
    elif download_subtitle:
        video_name = download_subtitle
    else:
        video_name = title

    return video_name


def find_m4s_files(entry_dir):
    audio_file = None
    video_file = None
    for root, dirs, files in os.walk(entry_dir):
        if "audio.m4s" in files and "video.m4s" in files:
            audio_file = os.path.abspath(os.path.join(root, "audio.m4s"))
            video_file = os.path.abspath(os.path.join(root, "video.m4s"))
            break
    return audio_file, video_file


def merge_single_entry(entry_path, output_dir, ffmpeg_path="ffmpeg"):
    entry_dir = os.path.dirname(entry_path)
    rel_path = os.path.relpath(entry_dir, os.path.commonpath([entry_dir]))

    video_name = parse_entry_json(entry_path)
    cleaned_name = clean_filename(video_name)

    audio_file, video_file = find_m4s_files(entry_dir)
    if not audio_file or not video_file:
        return {"status": "skip", "name": video_name, "reason": "未找到 audio.m4s 或 video.m4s"}

    temp_mp4 = os.path.join(entry_dir, f"{cleaned_name}.mp4")
    ffmpeg_cmd = f'-i "{video_file}" -i "{audio_file}" -c copy -y "{temp_mp4}"'
    success, error = run_ffmpeg(ffmpeg_cmd, ffmpeg_path)

    if not success or not os.path.exists(temp_mp4):
        return {"status": "fail", "name": video_name, "reason": error or "合并失败，未生成输出文件"}

    target_mp4 = os.path.join(output_dir, f"{cleaned_name}.mp4")
    if os.path.exists(target_mp4):
        timestamp = int(time.time())
        target_mp4 = os.path.join(output_dir, f"{cleaned_name}_{timestamp}.mp4")

    try:
        os.replace(temp_mp4, target_mp4)
        return {"status": "success", "name": video_name, "path": target_mp4}
    except Exception as e:
        return {"status": "fail", "name": video_name, "reason": f"移动文件失败: {e}"}


def merge_all(input_dir, output_dir=None, ffmpeg_path="ffmpeg"):
    if output_dir is None:
        output_dir = os.path.join(input_dir, "output")

    os.makedirs(output_dir, exist_ok=True)

    entry_paths = find_entry_json_paths(input_dir)

    if not entry_paths:
        return [], "未找到包含 entry.json 的缓存文件夹"

    results = []
    for entry_path in entry_paths:
        result = merge_single_entry(entry_path, output_dir, ffmpeg_path)
        results.append(result)

    return results, ""
