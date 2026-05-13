import wave
import os

def get_audio_duration(file_path):
    """
    获取音频文件的时长（秒）
    
    Args:
        file_path: 音频文件路径
    
    Returns:
        float: 音频时长（秒）
    """
    try:
        with wave.open(file_path, 'r') as wav_file:
            # 获取帧数和帧率
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            # 计算时长
            duration = frames / float(rate)
            return duration
    except Exception as e:
        print(f"计算音频时长时出错: {str(e)}")
        return 0.0

def get_total_duration(folder_path):
    """
    获取文件夹中所有音频文件的总时长
    
    Args:
        folder_path: 文件夹路径
    
    Returns:
        float: 总时长（秒）
    """
    total_duration = 0.0
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.wav'):
            file_path = os.path.join(folder_path, filename)
            duration = get_audio_duration(file_path)
            total_duration += duration
    
    return total_duration

if __name__ == "__main__":
    # 测试音频时长计算功能
    test_file = "output/test.wav"
    if os.path.exists(test_file):
        duration = get_audio_duration(test_file)
        print(f"音频时长: {duration:.2f}秒")
    else:
        print("测试文件不存在")
    
    # 测试总时长计算功能
    total_duration = get_total_duration("output")
    print(f"output文件夹中音频总时长: {total_duration:.2f}秒")
