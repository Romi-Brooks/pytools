import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys


class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PyTools - 自用 Python 小工具集")
        self.root.geometry("460x380")
        self.root.resizable(False, False)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 460) // 2
        y = (screen_height - 380) // 2
        self.root.geometry(f"460x380+{x}+{y}")

        title_label = ttk.Label(
            root, text="PyTools 工具集",
            font=("微软雅黑", 16, "bold")
        )
        title_label.pack(pady=(15, 5))

        desc_label = ttk.Label(
            root, text="选择一个工具启动",
            font=("微软雅黑", 10)
        )
        desc_label.pack(pady=(0, 10))

        button_frame = ttk.Frame(root)
        button_frame.pack(fill=tk.BOTH, expand=True, padx=40)

        tools = [
            ("图像预处理切分工具", self.open_pic_clipper,
             "对图片进行固定尺寸或自定义尺寸切割"),
            ("GPT-SoVITS API 调用", self.open_sovits_tts,
             "GPT-SoVITS 语音合成客户端"),
            ("B站缓存视频合并", self.open_m4s_merger,
             "将 B站缓存的 audio.m4s + video.m4s 合并为 mp4"),
            ("free4.xyz 内容获取", self.open_free4_get,
             "获取 free4.xyz 最新内容或搜索"),
        ]

        for text, command, desc in tools:
            btn = tk.Button(
                button_frame,
                text=text,
                command=command,
                width=22,
                height=2,
                font=("微软雅黑", 11),
                bg="#f0f0f0",
                relief=tk.RIDGE,
                cursor="hand2"
            )
            btn.pack(pady=(0, 3))

            desc_label = ttk.Label(
                button_frame, text=desc,
                font=("微软雅黑", 8), foreground="#666666"
            )
            desc_label.pack(pady=(0, 8))

    def open_pic_clipper(self):
        script_path = os.path.join(
            os.path.dirname(__file__), "tools", "pic_clipper", "gui.py"
        )
        self._launch_subprocess(script_path, "图像预处理切分工具")

    def open_sovits_tts(self):
        script_path = os.path.join(
            os.path.dirname(__file__), "tools", "sovits_tts", "gui.py"
        )
        self._launch_subprocess(script_path, "GPT-SoVITS API 调用")

    def open_m4s_merger(self):
        script_path = os.path.join(
            os.path.dirname(__file__), "tools", "m4s_merger", "gui.py"
        )
        self._launch_subprocess(script_path, "B站缓存视频合并")

    def open_free4_get(self):
        script_path = os.path.join(
            os.path.dirname(__file__), "tools", "free4_get", "gui.py"
        )
        self._launch_subprocess(script_path, "free4.xyz 内容获取")

    def _launch_subprocess(self, script_path, tool_name):
        if not os.path.exists(script_path):
            messagebox.showerror("错误", f"{tool_name} 脚本不存在:\n{script_path}")
            return
        try:
            subprocess.Popen([sys.executable, script_path])
        except Exception as e:
            messagebox.showerror("错误", f"启动 {tool_name} 失败:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()
