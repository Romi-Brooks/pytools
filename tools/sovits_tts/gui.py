import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time

class TTSGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("GPT-SoVITS 语音合成")
        self.master.geometry("800x600")
        
        # 创建主框架
        self.main_frame = ttk.Frame(self.master, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 文本输入区域
        self.text_frame = ttk.LabelFrame(self.main_frame, text="输入文本", padding="10")
        self.text_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.text_input = scrolledtext.ScrolledText(self.text_frame, width=80, height=10)
        self.text_input.pack(fill=tk.BOTH, expand=True)
        
        # 创建左右两栏布局
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 左栏 - 参考音频设置和模型设置
        self.left_frame = ttk.Frame(self.content_frame)
        self.left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # 导入filedialog
        from tkinter import filedialog
        
        # 参考音频和文本输入
        self.ref_frame = ttk.LabelFrame(self.left_frame, text="参考音频设置", padding="10")
        self.ref_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.ref_frame, text="参考音频路径:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ref_audio_entry = ttk.Entry(self.ref_frame, width=35)
        self.ref_audio_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Button(self.ref_frame, text="浏览", command=self.browse_ref_audio).grid(row=0, column=2, sticky=tk.W, pady=5)
        
        ttk.Label(self.ref_frame, text="参考文本:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.ref_text_entry = ttk.Entry(self.ref_frame, width=40)
        self.ref_text_entry.grid(row=1, column=1, columnspan=2, sticky=tk.W, pady=5)
        
        # 模型设置
        self.model_frame = ttk.LabelFrame(self.left_frame, text="模型设置", padding="10")
        self.model_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.model_frame, text="GPT模型路径:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.gpt_model_entry = ttk.Entry(self.model_frame, width=35)
        self.gpt_model_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        ttk.Button(self.model_frame, text="浏览", command=self.browse_gpt_model).grid(row=0, column=2, sticky=tk.W, pady=5)
        
        ttk.Label(self.model_frame, text="Sovits模型路径:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.sovits_model_entry = ttk.Entry(self.model_frame, width=35)
        self.sovits_model_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        ttk.Button(self.model_frame, text="浏览", command=self.browse_sovits_model).grid(row=1, column=2, sticky=tk.W, pady=5)
        
        # 右栏 - 推理设置
        self.right_frame = ttk.Frame(self.content_frame)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        # 推理设置
        self.emotion_frame = ttk.LabelFrame(self.right_frame, text="推理设置", padding="10")
        self.emotion_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 第一行
        ttk.Label(self.emotion_frame, text="batch_size:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.batch_size_entry = ttk.Entry(self.emotion_frame, width=10)
        self.batch_size_entry.insert(0, "1")
        self.batch_size_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.emotion_frame, text="采样步数:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.sample_steps_var = tk.StringVar(value="32")
        self.sample_steps_combobox = ttk.Combobox(self.emotion_frame, textvariable=self.sample_steps_var, values=["4", "8", "16", "32", "64", "128"], width=8)
        self.sample_steps_combobox.grid(row=0, column=3, sticky=tk.W, pady=5)
        
        # 第二行
        ttk.Label(self.emotion_frame, text="文本分割方法:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.text_split_var = tk.StringVar(value="cut5")
        self.text_split_combobox = ttk.Combobox(self.emotion_frame, textvariable=self.text_split_var, values=["cut5", "cut10", "cut15", "cut20"], width=8)
        self.text_split_combobox.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.emotion_frame, text="分段间隔(秒):").grid(row=1, column=2, sticky=tk.W, pady=5)
        self.fragment_interval_entry = ttk.Entry(self.emotion_frame, width=10)
        self.fragment_interval_entry.insert(0, "0.3")
        self.fragment_interval_entry.grid(row=1, column=3, sticky=tk.W, pady=5)
        
        # 第三行
        ttk.Label(self.emotion_frame, text="top_k:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.top_k_entry = ttk.Entry(self.emotion_frame, width=10)
        self.top_k_entry.insert(0, "5")
        self.top_k_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.emotion_frame, text="top_p:").grid(row=2, column=2, sticky=tk.W, pady=5)
        self.top_p_entry = ttk.Entry(self.emotion_frame, width=10)
        self.top_p_entry.insert(0, "1.0")
        self.top_p_entry.grid(row=2, column=3, sticky=tk.W, pady=5)
        
        # 第四行
        ttk.Label(self.emotion_frame, text="温度:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.temperature_entry = ttk.Entry(self.emotion_frame, width=10)
        self.temperature_entry.insert(0, "1.0")
        self.temperature_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.emotion_frame, text="语速:").grid(row=3, column=2, sticky=tk.W, pady=5)
        self.speed_factor_entry = ttk.Entry(self.emotion_frame, width=10)
        self.speed_factor_entry.insert(0, "1.0")
        self.speed_factor_entry.grid(row=3, column=3, sticky=tk.W, pady=5)
        
        # 第五行
        ttk.Label(self.emotion_frame, text="重复惩罚:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.repetition_penalty_entry = ttk.Entry(self.emotion_frame, width=10)
        self.repetition_penalty_entry.insert(0, "1.35")
        self.repetition_penalty_entry.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        ttk.Label(self.emotion_frame, text="batch_threshold:").grid(row=4, column=2, sticky=tk.W, pady=5)
        self.batch_threshold_entry = ttk.Entry(self.emotion_frame, width=10)
        self.batch_threshold_entry.insert(0, "0.75")
        self.batch_threshold_entry.grid(row=4, column=3, sticky=tk.W, pady=5)
        
        # 第六行
        ttk.Label(self.emotion_frame, text="随机种子:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.seed_entry = ttk.Entry(self.emotion_frame, width=10)
        self.seed_entry.insert(0, "-1")
        self.seed_entry.grid(row=5, column=1, sticky=tk.W, pady=5)
        
        # 第七行 - 复选框
        self.split_bucket_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.emotion_frame, text="按数据桶并行推理", variable=self.split_bucket_var).grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        self.parallel_infer_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self.emotion_frame, text="并行推理", variable=self.parallel_infer_var).grid(row=6, column=2, columnspan=2, sticky=tk.W, pady=5)
        
        # 第八行
        self.super_sampling_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.emotion_frame, text="音频超采样(仅V3模型)", variable=self.super_sampling_var).grid(row=7, column=0, columnspan=4, sticky=tk.W, pady=5)
        
        # 控制按钮
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=5)
        
        self.start_button = ttk.Button(self.button_frame, text="开始合成", command=self.start_synthesis)
        self.start_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(self.button_frame, text="停止", command=self.stop_synthesis, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        # 状态显示区域
        self.status_frame = ttk.LabelFrame(self.main_frame, text="状态", padding="10")
        self.status_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 正在播放的文本
        ttk.Label(self.status_frame, text="正在播放的文本:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.playing_text = scrolledtext.ScrolledText(self.status_frame, width=70, height=3, state=tk.DISABLED)
        self.playing_text.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E, pady=2)
        
        # 正在转换的文本
        ttk.Label(self.status_frame, text="正在转换的文本:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.converting_text = scrolledtext.ScrolledText(self.status_frame, width=70, height=3, state=tk.DISABLED)
        self.converting_text.grid(row=3, column=0, columnspan=2, sticky=tk.W+tk.E, pady=2)
        
        # 进度条
        ttk.Label(self.status_frame, text="进度:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.status_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=4, column=1, sticky=tk.W+tk.E, pady=5)
        
        # 进度文本
        self.progress_text = ttk.Label(self.status_frame, text="0% - 0.00秒 / 0.00秒")
        self.progress_text.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # 线程控制
        self.synthesis_thread = None
        self.stop_event = threading.Event()
        
    def start_synthesis(self):
        """开始语音合成"""
        # 获取输入文本
        input_text = self.text_input.get(1.0, tk.END).strip()
        if not input_text:
            self.show_message("请输入要合成的文本")
            return
        
        # 获取参考音频路径和文本
        ref_audio_path = self.ref_audio_entry.get().strip()
        if not ref_audio_path:
            self.show_message("请输入参考音频路径")
            return
        
        ref_text = self.ref_text_entry.get().strip()
        if not ref_text:
            self.show_message("请输入参考文本")
            return
        
        # 禁用按钮
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        
        # 重置停止事件
        self.stop_event.clear()
        
        # 启动合成线程
        self.synthesis_thread = threading.Thread(
            target=self.synthesis_task,
            args=(input_text, ref_audio_path, ref_text)
        )
        self.synthesis_thread.daemon = True
        self.synthesis_thread.start()
    
    def stop_synthesis(self):
        """停止语音合成"""
        self.stop_event.set()
        self.stop_button.config(state=tk.DISABLED)
    
    def synthesis_task(self, input_text, ref_audio_path, ref_text):
        """合成任务"""
        # 导入所需模块
        import os
        import sys
        import pygame
        import queue
        
        # 获取当前脚本所在目录
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 将当前目录添加到Python路径
        sys.path.insert(0, current_dir)
        
        from text_processor import split_text_by_period
        from audio_utils import get_total_duration, get_audio_duration
        from inference import text_to_speech, change_gpt_model, change_sovits_model
        
        # 初始化pygame.mixer
        pygame.mixer.init()
        
        # 创建音频队列
        audio_queue = queue.Queue()
        
        # 创建输出目录
        output_dir = os.path.join(current_dir, "..", "..", "output")
        os.makedirs(output_dir, exist_ok=True)
        
        # 获取模型路径
        gpt_model_path = self.gpt_model_entry.get().strip()
        sovits_model_path = self.sovits_model_entry.get().strip()
        
        # 切换模型
        if gpt_model_path:
            change_gpt_model(gpt_model_path)
        if sovits_model_path:
            change_sovits_model(sovits_model_path)
        
        # 获取推理参数
        try:
            top_k = int(self.top_k_entry.get())
        except ValueError:
            top_k = 5
        
        try:
            top_p = float(self.top_p_entry.get())
        except ValueError:
            top_p = 1.0
        
        try:
            temperature = float(self.temperature_entry.get())
        except ValueError:
            temperature = 1.0
        
        try:
            batch_size = int(self.batch_size_entry.get())
        except ValueError:
            batch_size = 1
        
        text_split_method = self.text_split_var.get()
        
        try:
            batch_threshold = float(self.batch_threshold_entry.get())
        except ValueError:
            batch_threshold = 0.75
        
        split_bucket = self.split_bucket_var.get()
        
        try:
            speed_factor = float(self.speed_factor_entry.get())
        except ValueError:
            speed_factor = 1.0
        
        try:
            fragment_interval = float(self.fragment_interval_entry.get())
        except ValueError:
            fragment_interval = 0.3
        
        try:
            seed = int(self.seed_entry.get())
        except ValueError:
            seed = -1
        
        parallel_infer = self.parallel_infer_var.get()
        
        try:
            repetition_penalty = float(self.repetition_penalty_entry.get())
        except ValueError:
            repetition_penalty = 1.35
        
        try:
            sample_steps = int(self.sample_steps_var.get())
        except ValueError:
            sample_steps = 32
        
        super_sampling = self.super_sampling_var.get()
        
        # 分割文本
        sentences = split_text_by_period(input_text)
        total_sentences = len(sentences)
        
        # 存储所有生成的音频文件路径
        audio_files = []
        
        def render_thread():
            """渲染线程"""
            for i, sentence in enumerate(sentences):
                if self.stop_event.is_set():
                    break
                
                # 更新正在转换的文本
                self.update_converting_text(sentence)
                
                # 生成音频文件路径
                output_file = os.path.join(output_dir, f"sentence_{i+1}.wav")
                
                # 调用API合成语音
                success = text_to_speech(
                    text=sentence,
                    text_lang="zh",
                    ref_audio_path=ref_audio_path,
                    prompt_lang="zh",
                    prompt_text=ref_text,
                    output_file=output_file,
                    top_k=top_k,
                    top_p=top_p,
                    temperature=temperature,
                    batch_size=batch_size,
                    text_split_method=text_split_method,
                    batch_threshold=batch_threshold,
                    split_bucket=split_bucket,
                    speed_factor=speed_factor,
                    fragment_interval=fragment_interval,
                    seed=seed,
                    parallel_infer=parallel_infer,
                    repetition_penalty=repetition_penalty,
                    sample_steps=sample_steps,
                    super_sampling=super_sampling
                )
                
                if success:
                    audio_files.append(output_file)
                    # 将音频文件和句子放入队列
                    audio_queue.put((output_file, sentence))
                else:
                    self.show_message(f"合成第{i+1}句失败")
            
            # 渲染完成，放入结束标记
            audio_queue.put(None)
        
        def play_thread():
            """播放线程"""
            processed_sentences = 0
            total_duration = 0.0
            current_play_time = 0.0
            
            while not self.stop_event.is_set():
                # 从队列中获取音频文件
                item = audio_queue.get()
                
                # 检查是否结束标记
                if item is None:
                    break
                
                output_file, sentence = item
                processed_sentences += 1
                
                # 更新总时长
                total_duration = get_total_duration(output_dir)
                
                # 计算当前进度（基于总时长）
                progress = (processed_sentences / total_sentences) * 100
                self.update_progress(progress, total_duration)
                
                # 更新正在播放的文本
                self.update_playing_text(sentence)
                
                # 播放音频
                pygame.mixer.music.load(output_file)
                pygame.mixer.music.play()
                
                # 等待音频播放完成
                while pygame.mixer.music.get_busy() and not self.stop_event.is_set():
                    time.sleep(0.1)
                    # 更新进度
                    if total_duration > 0:
                        # 计算已经播放的时间
                        elapsed_time = pygame.mixer.music.get_pos() / 1000
                        # 计算已播放的所有音频时长
                        played_duration = sum(get_audio_duration(audio_files[j]) for j in range(processed_sentences-1))
                        current_play_time = played_duration + elapsed_time
                        progress = (current_play_time / total_duration) * 100
                        self.update_progress(progress, total_duration)
            
            # 等待最后一个音频播放完成
            while pygame.mixer.music.get_busy() and not self.stop_event.is_set():
                time.sleep(0.1)
                # 更新进度
                if total_duration > 0:
                    # 计算已经播放的时间
                    elapsed_time = pygame.mixer.music.get_pos() / 1000
                    if audio_files:
                        # 计算已播放的所有音频时长（除了最后一个）
                        played_duration = sum(get_audio_duration(audio_files[j]) for j in range(len(audio_files)-1))
                        current_play_time = played_duration + elapsed_time
                        progress = (current_play_time / total_duration) * 100
                        self.update_progress(progress, total_duration)
                    else:
                        progress = 0
                        self.update_progress(progress, total_duration)
            
            # 播放完成后，将进度设置为100%
            if total_duration > 0 and not self.stop_event.is_set():
                self.update_progress(100, total_duration)
            
            # 完成后启用按钮
            self.master.after(0, lambda: self.start_button.config(state=tk.NORMAL))
            self.master.after(0, lambda: self.stop_button.config(state=tk.DISABLED))
            
            if not self.stop_event.is_set():
                self.show_message(f"合成完成！共处理{processed_sentences}句，总时长{total_duration:.2f}秒")
            else:
                self.show_message("合成已停止")
        
        # 启动渲染线程和播放线程
        render_thread = threading.Thread(target=render_thread)
        play_thread = threading.Thread(target=play_thread)
        
        render_thread.daemon = True
        play_thread.daemon = True
        
        render_thread.start()
        play_thread.start()
        
        # 等待两个线程完成
        render_thread.join()
        play_thread.join()
    
    def update_playing_text(self, text):
        """更新正在播放的文本"""
        def _update():
            self.playing_text.config(state=tk.NORMAL)
            self.playing_text.delete(1.0, tk.END)
            self.playing_text.insert(tk.END, text)
            self.playing_text.config(state=tk.DISABLED)
        self.master.after(0, _update)
    
    def update_converting_text(self, text):
        """更新正在转换的文本"""
        def _update():
            self.converting_text.config(state=tk.NORMAL)
            self.converting_text.delete(1.0, tk.END)
            self.converting_text.insert(tk.END, text)
            self.converting_text.config(state=tk.DISABLED)
        self.master.after(0, _update)
    
    def update_progress(self, progress, total_duration):
        """更新进度条"""
        def _update():
            self.progress_var.set(progress)
            self.progress_text.config(text=f"{progress:.1f}% - {total_duration:.2f}秒")
        self.master.after(0, _update)
    
    def browse_ref_audio(self):
        """浏览参考音频文件"""
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="选择参考音频文件",
            filetypes=[("音频文件", "*.wav *.mp3 *.flac *.ogg")]
        )
        if file_path:
            self.ref_audio_entry.delete(0, tk.END)
            self.ref_audio_entry.insert(0, file_path)
    
    def browse_gpt_model(self):
        """浏览GPT模型文件"""
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="选择GPT模型文件",
            filetypes=[("模型文件", "*.ckpt")]
        )
        if file_path:
            self.gpt_model_entry.delete(0, tk.END)
            self.gpt_model_entry.insert(0, file_path)
    
    def browse_sovits_model(self):
        """浏览Sovits模型文件"""
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(
            title="选择Sovits模型文件",
            filetypes=[("模型文件", "*.pth")]
        )
        if file_path:
            self.sovits_model_entry.delete(0, tk.END)
            self.sovits_model_entry.insert(0, file_path)
    
    def show_message(self, message):
        """显示消息"""
        def _show():
            # 创建临时消息窗口
            msg_window = tk.Toplevel(self.master)
            msg_window.title("消息")
            msg_window.geometry("300x100")
            
            ttk.Label(msg_window, text=message, padding=20).pack(fill=tk.BOTH, expand=True)
            ttk.Button(msg_window, text="确定", command=msg_window.destroy).pack(pady=10)
            
            # 居中显示
            msg_window.transient(self.master)
            msg_window.grab_set()
            self.master.wait_window(msg_window)
        self.master.after(0, _show)

if __name__ == "__main__":
    root = tk.Tk()
    app = TTSGUI(root)
    root.mainloop()
