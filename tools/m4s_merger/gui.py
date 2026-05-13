import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from tools.m4s_merger.merger import merge_all, find_entry_json_paths


class M4sMergerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("B站缓存视频合并工具")
        self.root.geometry("700x550")
        self.root.minsize(600, 400)

        self._center_window()
        self._build_ui()

    def _center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 700) // 2
        y = (screen_height - 550) // 2
        self.root.geometry(f"700x550+{x}+{y}")

    def _build_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        folder_frame = ttk.LabelFrame(main_frame, text="缓存文件夹", padding=10)
        folder_frame.pack(fill=tk.X, pady=(0, 10))

        folder_row = ttk.Frame(folder_frame)
        folder_row.pack(fill=tk.X)

        self.folder_var = tk.StringVar()
        self.folder_entry = ttk.Entry(
            folder_row, textvariable=self.folder_var, font=("微软雅黑", 10)
        )
        self.folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        ttk.Button(folder_row, text="浏览...", command=self._browse_folder).pack(side=tk.RIGHT)

        cfg_frame = ttk.Frame(folder_frame)
        cfg_frame.pack(fill=tk.X, pady=(5, 0))

        ttk.Label(cfg_frame, text="FFmpeg 路径:").pack(side=tk.LEFT, padx=(0, 5))
        self.ffmpeg_var = tk.StringVar(value="ffmpeg")
        ttk.Entry(cfg_frame, textvariable=self.ffmpeg_var, width=25).pack(side=tk.LEFT)

        ttk.Label(cfg_frame, text=" 输出目录:").pack(side=tk.LEFT, padx=(10, 5))
        self.output_dir_var = tk.StringVar(value="")
        ttk.Entry(cfg_frame, textvariable=self.output_dir_var, width=20).pack(side=tk.LEFT)

        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 10))

        self.merge_btn = ttk.Button(
            action_frame, text="开始合并", command=self._on_merge, width=15
        )
        self.merge_btn.pack(side=tk.LEFT, padx=(0, 10))

        self.preview_btn = ttk.Button(
            action_frame, text="预览文件结构", command=self._on_preview, width=15
        )
        self.preview_btn.pack(side=tk.LEFT)

        self.status_label = ttk.Label(action_frame, text="就绪")
        self.status_label.pack(side=tk.RIGHT)

        log_frame = ttk.LabelFrame(main_frame, text="处理日志", padding=5)
        log_frame.pack(fill=tk.BOTH, expand=True)

        log_container = ttk.Frame(log_frame)
        log_container.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(log_container)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.log_text = tk.Text(
            log_container, font=("Consolas", 10),
            yscrollcommand=scrollbar.set, wrap=tk.WORD,
            state=tk.DISABLED, bg="#1e1e1e", fg="#d4d4d4",
            insertbackground="white"
        )
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.log_text.yview)

        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=(5, 0))

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame, variable=self.progress_var, mode="determinate"
        )
        self.progress_bar.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=(0, 10))

        self.progress_label = ttk.Label(progress_frame, text="0%", width=8)
        self.progress_label.pack(side=tk.RIGHT)

    def _log(self, message, level="info"):
        self.log_text.config(state=tk.NORMAL)
        tag = level
        self.log_text.insert(tk.END, message + "\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update_idletasks()

    def _set_status(self, text):
        self.status_label.config(text=text)
        self.root.update_idletasks()

    def _browse_folder(self):
        folder = filedialog.askdirectory(title="选择B站缓存文件夹")
        if folder:
            self.folder_var.set(folder)

    def _on_preview(self):
        folder = self.folder_var.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showwarning("提示", "请先选择有效的文件夹")
            return
        entry_paths = find_entry_json_paths(folder)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self._log(f"文件夹: {folder}")
        self._log(f"找到 {len(entry_paths)} 个缓存视频条目", "highlight")
        for ep in entry_paths:
            entry_dir = os.path.dirname(ep)
            self._log(f"  - {entry_dir}")

    def _on_merge(self):
        folder = self.folder_var.get().strip()
        if not folder or not os.path.isdir(folder):
            messagebox.showwarning("提示", "请先选择有效的B站缓存文件夹")
            return

        ffmpeg_path = self.ffmpeg_var.get().strip() or "ffmpeg"
        output_dir = self.output_dir_var.get().strip() or None

        self.merge_btn.config(state=tk.DISABLED)
        self.preview_btn.config(state=tk.DISABLED)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.progress_label.config(text="0%")
        self._set_status("正在合并...")

        threading.Thread(
            target=self._do_merge, args=(folder, output_dir, ffmpeg_path),
            daemon=True
        ).start()

    def _do_merge(self, folder, output_dir, ffmpeg_path):
        self._log("=" * 50)
        self._log(f"缓存目录: {folder}")
        self._log(f"FFmpeg: {ffmpeg_path}")
        self._log("开始扫描并合并视频...")
        self._log("=" * 50)

        results, error = merge_all(folder, output_dir, ffmpeg_path)

        if error:
            self.root.after(0, lambda: self._log(f"错误: {error}", "error"))
            self.root.after(0, self._finish_merge)
            return

        total = len(results)
        for i, result in enumerate(results):
            self.root.after(0, lambda r=result: self._log_result(r))
            progress = int((i + 1) / total * 100)
            self.root.after(0, lambda p=progress: self.progress_var.set(p))
            self.root.after(0, lambda p=progress: self.progress_label.config(text=f"{p}%"))

        success_count = sum(1 for r in results if r["status"] == "success")
        skip_count = sum(1 for r in results if r["status"] == "skip")
        fail_count = sum(1 for r in results if r["status"] == "fail")

        self.root.after(0, lambda: self._log("=" * 50))
        self.root.after(0, lambda: self._log(
            f"处理完成: {success_count} 成功, {skip_count} 跳过, {fail_count} 失败",
            "highlight"
        ))
        self.root.after(0, self._finish_merge)

    def _log_result(self, result):
        if result["status"] == "success":
            self._log(f"✓ 合并成功: {result['name']}", "success")
            self._log(f"  输出路径: {result['path']}")
        elif result["status"] == "skip":
            self._log(f"○ 跳过: {result['name']} - {result['reason']}", "warning")
        elif result["status"] == "fail":
            self._log(f"✗ 失败: {result['name']} - {result['reason']}", "error")

    def _finish_merge(self):
        self.merge_btn.config(state=tk.NORMAL)
        self.preview_btn.config(state=tk.NORMAL)
        self._set_status("完成")


def main():
    root = tk.Tk()
    app = M4sMergerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
