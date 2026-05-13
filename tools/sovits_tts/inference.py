import requests
import os

def text_to_speech(text, text_lang, ref_audio_path, prompt_lang, prompt_text="", output_file="output.wav", top_k=5, top_p=1.0, temperature=1.0, batch_size=1, text_split_method="cut5", batch_threshold=0.75, split_bucket=True, speed_factor=1.0, fragment_interval=0.3, seed=-1, parallel_infer=True, repetition_penalty=1.35, sample_steps=32, super_sampling=False):
    """
    调用GPT-SoVITS API将文本转换为语音
    
    Args:
        text: 要合成的文本
        text_lang: 文本语言，如"zh"、"en"等
        ref_audio_path: 参考音频路径
        prompt_lang: 参考音频文本的语言
        prompt_text: 参考音频的文本（可选）
        output_file: 输出音频文件路径
        top_k: top k sampling
        top_p: top p sampling
        temperature: 温度参数
        batch_size: 批处理大小
        text_split_method: 文本分割方法
        batch_threshold: batch splitting的阈值
        split_bucket: 是否将batch分割成多个bucket
        speed_factor: 控制合成音频的速度
        fragment_interval: 控制音频片段的间隔
        seed: 随机种子
        parallel_infer: 是否使用并行推理
        repetition_penalty: T2S模型的重复惩罚
        sample_steps: VITS模型V3的采样步数
        super_sampling: 使用VITS模型V3时是否使用超采样
    
    Returns:
        bool: 成功返回True，失败返回False
    """
    # API端点
    url = "http://127.0.0.1:9880/tts"
    
    # 请求参数
    data = {
        "text": text,
        "text_lang": text_lang,
        "ref_audio_path": ref_audio_path,
        "prompt_text": prompt_text,
        "prompt_lang": prompt_lang,
        "top_k": top_k,
        "top_p": top_p,
        "temperature": temperature,
        "text_split_method": text_split_method,
        "batch_size": batch_size,
        "batch_threshold": batch_threshold,
        "split_bucket": split_bucket,
        "speed_factor": speed_factor,
        "fragment_interval": fragment_interval,
        "seed": seed,
        "parallel_infer": parallel_infer,
        "repetition_penalty": repetition_penalty,
        "sample_steps": sample_steps,
        "super_sampling": super_sampling,
        "media_type": "wav",
        "streaming_mode": False
    }
    
    try:
        print(f"正在调用API合成语音...")
        print(f"文本: {text}")
        print(f"参考音频: {ref_audio_path}")
        
        # 发送POST请求
        response = requests.post(url, json=data)
        
        # 检查响应状态码
        if response.status_code == 200:
            # 保存音频文件
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"语音合成成功！音频已保存到: {output_file}")
            return True
        else:
            # 打印错误信息
            error_msg = response.json().get("message", "未知错误")
            print(f"语音合成失败: {error_msg}")
            return False
    except Exception as e:
        print(f"调用API时发生错误: {str(e)}")
        return False

def change_gpt_model(weights_path):
    """
    切换GPT模型
    
    Args:
        weights_path: GPT模型权重路径
    
    Returns:
        bool: 成功返回True，失败返回False
    """
    url = f"http://127.0.0.1:9880/set_gpt_weights?weights_path={weights_path}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"GPT模型切换成功: {weights_path}")
            return True
        else:
            error_msg = response.json().get("message", "未知错误")
            print(f"GPT模型切换失败: {error_msg}")
            return False
    except Exception as e:
        print(f"切换GPT模型时发生错误: {str(e)}")
        return False

def change_sovits_model(weights_path):
    """
    切换Sovits模型
    
    Args:
        weights_path: Sovits模型权重路径
    
    Returns:
        bool: 成功返回True，失败返回False
    """
    url = f"http://127.0.0.1:9880/set_sovits_weights?weights_path={weights_path}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Sovits模型切换成功: {weights_path}")
            return True
        else:
            error_msg = response.json().get("message", "未知错误")
            print(f"Sovits模型切换失败: {error_msg}")
            return False
    except Exception as e:
        print(f"切换Sovits模型时发生错误: {str(e)}")
        return False

if __name__ == "__main__":
    # 示例用法
    text = "先帝创业未半而中道崩殂，今天下三分，益州疲弊，此诚危急存亡之秋也。"
    text_lang = "zh"
    # 手动输入参考音频路径
    ref_audio_path = input("请输入参考音频路径: ")
    prompt_lang = "zh"
    # 手动输入参考文本
    prompt_text = input("请输入参考音频对应的文本: ")
    output_file = "output.wav"
    
    # 调用语音合成
    success = text_to_speech(
        text=text,
        text_lang=text_lang,
        ref_audio_path=ref_audio_path,
        prompt_lang=prompt_lang,
        prompt_text=prompt_text,
        output_file=output_file
    )
    
    if success:
        print("任务完成！")
    else:
        print("任务失败！")
