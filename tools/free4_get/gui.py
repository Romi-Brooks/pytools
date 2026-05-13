import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from tools.free4_get.fetcher import fetch_latest, search, get_download_links


class Free4GetGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("free4.xyz 内容获取工具")
        self.root.geometry("700x600")
        self.root.minsize(600, 500)
        self.current_results = []

        self._center_window()
        self._build_ui()

    def _center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - 700) // 2
        y = (screen_height - 600) // 2
        self.root.geometry(f"700x600+{x}+{y}")

    def _build_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(top_frame, text="获取最新内容", command=self._on_fetch_latest).pack(side=tk.LEFT, padx=(0, 10))

        ttk.Label(top_frame, text="关键词:").pack(side=tk.LEFT, padx=(10, 2))
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(top_frame, textvariable=self.search_var, width=25)
        search_entry.pack(side=tk.LEFT, padx=(0, 5))
        search_entry.bind("<Return>", lambda e: self._on_search())
        ttk.Button(top_frame, text="搜索", command=self._on_search).pack(side=tk.LEFT)

        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0, 5))
        self.status_label = ttk.Label(info_frame, text="就绪")
        self.status_label.pack(side=tk.LEFT)
        self.progress_label = ttk.Label(info_frame, text="")
        self.progress_label.pack(side=tk.RIGHT)

        result_frame = ttk.LabelFrame(main_frame, text="搜索结果", padding=5)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        listbox_frame = ttk.Frame(result_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.result_listbox = tk.Listbox(
            listbox_frame, yscrollcommand=scrollbar.set,
            font=("微软雅黑", 10), selectbackground="#0078D7"
        )
        self.result_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.result_listbox.yview)
        self.result_listbox.bind("<<ListboxSelect>>", self._on_select_result)

        detail_frame = ttk.LabelFrame(main_frame, text="下载链接", padding=5)
        detail_frame.pack(fill=tk.X, pady=(0, 5))

        self.detail_text = tk.Text(detail_frame, height=5, font=("微软雅黑", 9), wrap=tk.WORD)
        self.detail_text.pack(fill=tk.BOTH, expand=True)

        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X)
        ttk.Button(bottom_frame, text="清空结果", command=self._clear_results).pack(side=tk.LEFT)

    def _set_status(self, text):
        self.status_label.config(text=text)
        self.root.update_idletasks()

    def _on_fetch_latest(self):
        self.current_results = []
        self.result_listbox.delete(0, tk.END)
        self.detail_text.delete(1.0, tk.END)
        self._set_status("正在获取最新内容...")
        threading.Thread(target=self._do_fetch_latest, daemon=True).start()

    def _do_fetch_latest(self):
        try:
            results, total = fetch_latest()
            self.root.after(0, lambda: self._display_results(results, total, "最新"))
        except Exception as e:
            self.root.after(0, lambda: self._set_status(f"获取失败: {str(e)}"))

    def _on_search(self):
        keyword = self.search_var.get().strip()
        if not keyword:
            messagebox.showwarning("提示", "请输入搜索关键词")
            return
        self.current_results = []
        self.result_listbox.delete(0, tk.END)
        self.detail_text.delete(1.0, tk.END)
        self._set_status(f"正在搜索: {keyword}")
        threading.Thread(target=self._do_search, args=(keyword,), daemon=True).start()

    def _do_search(self, keyword):
        try:
            results, total = search(keyword)
            self.root.after(0, lambda: self._display_results(results, total, "搜索"))
        except Exception as e:
            self.root.after(0, lambda: self._set_status(f"搜索失败: {str(e)}"))

    def _display_results(self, results, total, source):
        self.current_results = results
        self.result_listbox.delete(0, tk.END)
        if not results:
            self.result_listbox.insert(tk.END, "未找到结果")
            self._set_status("未找到结果")
            return
        for i, item in enumerate(results):
            display_text = f"{i+1}. {item['title']}"
            self.result_listbox.insert(tk.END, display_text)
        self._set_status(f"{source}: 共 {total} 个结果，显示前 {len(results)} 个")

    def _on_select_result(self, event):
        selection = self.result_listbox.curselection()
        if not selection or not self.current_results:
            return
        index = selection[0]
        if index >= len(self.current_results):
            return
        item = self.current_results[index]
        self.detail_text.delete(1.0, tk.END)
        self.detail_text.insert(tk.END, f"标题: {item['title']}\n")
        self.detail_text.insert(tk.END, f"链接: {item['url']}\n")
        self.detail_text.insert(tk.END, "\n正在获取下载链接...")
        threading.Thread(target=self._do_get_links, args=(index, item["url"]), daemon=True).start()

    def _do_get_links(self, index, url):
        try:
            links = get_download_links(url)
            self.root.after(0, lambda: self._display_links(index, links))
        except Exception as e:
            self.root.after(0, lambda: self._display_links_error(str(e)))

    def _display_links(self, index, links):
        self.detail_text.delete(1.0, tk.END)
        item = self.current_results[index]
        self.detail_text.insert(tk.END, f"标题: {item['title']}\n")
        self.detail_text.insert(tk.END, f"链接: {item['url']}\n\n")
        if links:
            for name, link in links.items():
                self.detail_text.insert(tk.END, f"{name}: {link}\n")
        else:
            self.detail_text.insert(tk.END, "未找到下载链接\n")

    def _display_links_error(self, error):
        self.detail_text.insert(tk.END, f"获取下载链接失败: {error}\n")

    def _clear_results(self):
        self.current_results = []
        self.result_listbox.delete(0, tk.END)
        self.detail_text.delete(1.0, tk.END)
        self._set_status("就绪")


def main():
    root = tk.Tk()
    app = Free4GetGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
