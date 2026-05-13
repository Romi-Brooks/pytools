import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import os
import sys

# 导入自定义模块
from image_processor import ImageProcessor
from file_utils import FileUtils

class ImageCutter:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Clipper")
        self.root.geometry("1200x800")
        
        # 初始化处理器
        self.image_processor = ImageProcessor()
        self.file_utils = FileUtils()
        
        # 设置默认切割尺寸
        self.crop_width = 512
        self.crop_height = 512
        
        # 图像相关变量
        self.image = None          # 当前显示的图像（PIL对象，可能被缩放）
        self.original_image = None # 保存原始图像备份（用于缩放计算，避免失真）
        self.tk_image = None       # 画布显示的tk图像对象
        self.image_path = None
        self.image_directory = None
        
        # 输出目录
        self.output_directory = "output"
        
        # 鼠标位置和裁剪框
        self.mouse_x = 0
        self.mouse_y = 0
        self.crop_box = None
        
        # 拖动相关变量
        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        # 确认按钮
        self.confirm_btn = None
        self.cancel_btn = None
        
        # 图片导航
        self.image_files = []
        self.current_image_index = -1
        
        # 缩放相关【核心优化】
        self.base_scale = 1.0      # 累计缩放因子（核心：基于原始图的总缩放比例）
        self.scale_step = {0.5: 0.5, 1.5: 1.5}  # 缩放步长
        self.min_scale = 0.2       # 最小缩放比例（防止缩放过小）
        self.max_scale = 5.0       # 最大缩放比例（防止缩放过⼤）
        
        # 创建UI
        self.create_widgets()
    
    def create_widgets(self):
        # 菜单栏
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="打开图片", command=self.open_image)
        filemenu.add_command(label="打开目录", command=self.open_directory)
        filemenu.add_separator()
        filemenu.add_command(label="退出", command=self.root.quit)
        menubar.add_cascade(label="文件", menu=filemenu)
        self.root.config(menu=menubar)
        
        # 主框架
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 左侧控制面板
        control_frame = tk.Frame(main_frame, width=300, bg="#f0f0f0")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # 输入输出设置
        io_frame = tk.LabelFrame(control_frame, text="输入输出", padx=10, pady=10)
        io_frame.pack(fill=tk.X, padx=10, pady=10)
        
        open_image_btn = tk.Button(io_frame, text="打开图片", command=self.open_image)
        open_image_btn.pack(fill=tk.X, pady=2)
        open_dir_btn = tk.Button(io_frame, text="打开目录", command=self.open_directory)
        open_dir_btn.pack(fill=tk.X, pady=2)
        
        # 输出目录设置
        output_frame = tk.Frame(io_frame)
        output_frame.pack(fill=tk.X, pady=5)
        tk.Label(output_frame, text="输出目录:").pack(side=tk.LEFT)
        self.output_var = tk.StringVar(value=self.output_directory)
        output_entry = tk.Entry(output_frame, textvariable=self.output_var, width=20)
        output_entry.pack(side=tk.LEFT, padx=5)
        browse_output_btn = tk.Button(output_frame, text="浏览", command=self.browse_output_directory)
        browse_output_btn.pack(side=tk.LEFT, padx=5)
        
        # 切割尺寸设置
        size_frame = tk.LabelFrame(control_frame, text="切割尺寸", padx=10, pady=10)
        size_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 尺寸模式选择
        mode_frame = tk.Frame(size_frame)
        mode_frame.pack(fill=tk.X, pady=5)
        self.size_mode = tk.StringVar(value="fixed")
        tk.Radiobutton(mode_frame, text="固定大小", variable=self.size_mode, value="fixed").pack(side=tk.LEFT, padx=10)
        tk.Radiobutton(mode_frame, text="自定义大小", variable=self.size_mode, value="custom").pack(side=tk.LEFT, padx=10)
        
        # 自定义尺寸
        custom_frame = tk.Frame(size_frame)
        custom_frame.pack(fill=tk.X, pady=5)
        tk.Label(custom_frame, text="宽度:").pack(side=tk.LEFT)
        self.width_var = tk.StringVar(value="512")
        width_entry = tk.Entry(custom_frame, textvariable=self.width_var, width=10)
        width_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(custom_frame, text="高度:").pack(side=tk.LEFT, padx=10)
        self.height_var = tk.StringVar(value="512")
        height_entry = tk.Entry(custom_frame, textvariable=self.height_var, width=10)
        height_entry.pack(side=tk.LEFT, padx=5)
        apply_btn = tk.Button(custom_frame, text="应用", command=self.apply_custom_size)
        apply_btn.pack(side=tk.LEFT, padx=5)
        
        # 常用尺寸快捷按钮
        quick_frame = tk.Frame(size_frame)
        quick_frame.pack(fill=tk.X, pady=5)
        tk.Label(quick_frame, text="常用尺寸:").pack(side=tk.LEFT)
        quick_sizes = [(512, 512), (768, 768), (1024, 1024), (768, 512), (512, 768)]
        for w, h in quick_sizes:
            btn = tk.Button(quick_frame, text=f"{w}x{h}", command=lambda w=w, h=h: self.set_size(w, h))
            btn.pack(side=tk.LEFT, padx=2)
        
        # 图片信息显示区域
        info_frame = tk.LabelFrame(control_frame, text="图片信息", padx=10, pady=10)
        info_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 原始分辨率+当前缩放后分辨率
        res_frame = tk.Frame(info_frame)
        res_frame.pack(fill=tk.X, pady=2)
        tk.Label(res_frame, text="分辨率:", width=8, anchor=tk.W).pack(side=tk.LEFT)
        self.resolution_var = tk.StringVar(value="-- x --")
        tk.Label(res_frame, textvariable=self.resolution_var, anchor=tk.W).pack(side=tk.LEFT)
        
        # 累计缩放比例显示【新增】
        scale_frame = tk.Frame(info_frame)
        scale_frame.pack(fill=tk.X, pady=2)
        tk.Label(scale_frame, text="当前缩放:", width=8, anchor=tk.W).pack(side=tk.LEFT)
        self.current_scale_var = tk.StringVar(value="1.0x")
        tk.Label(scale_frame, textvariable=self.current_scale_var, fg="#0066cc", anchor=tk.W).pack(side=tk.LEFT)
        
        # 文件大小显示
        size_frame = tk.Frame(info_frame)
        size_frame.pack(fill=tk.X, pady=2)
        tk.Label(size_frame, text="文件大小:", width=8, anchor=tk.W).pack(side=tk.LEFT)
        self.file_size_var = tk.StringVar(value="--")
        tk.Label(size_frame, textvariable=self.file_size_var, anchor=tk.W).pack(side=tk.LEFT)
        
        # 图片缩放控制区域【优化】
        scale_ctrl_frame = tk.LabelFrame(control_frame, text="图片缩放（累计）", padx=10, pady=10)
        scale_ctrl_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 缩放按钮+边界提示
        scale_btn_frame = tk.Frame(scale_ctrl_frame)
        scale_btn_frame.pack(fill=tk.X, pady=5)
        scale_0_5_btn = tk.Button(scale_btn_frame, text="缩小0.5x", command=lambda: self.scale_image(0.5))
        scale_0_5_btn.pack(side=tk.LEFT, padx=5)
        scale_1_5_btn = tk.Button(scale_btn_frame, text="放大1.5x", command=lambda: self.scale_image(1.5))
        scale_1_5_btn.pack(side=tk.LEFT, padx=5)
        restore_btn = tk.Button(scale_btn_frame, text="恢复原始尺寸", command=self.restore_original_image)
        restore_btn.pack(side=tk.LEFT, padx=5)
        
        # 缩放边界提示
        tip_label = tk.Label(scale_ctrl_frame, text=f"缩放范围：{self.min_scale}x ~ {self.max_scale}x", 
                             font=("Arial", 9), fg="#666666")
        tip_label.pack(anchor=tk.W, pady=2)
        
        # 操作提示
        hint_frame = tk.Frame(control_frame)
        hint_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(hint_frame, text="操作提示:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        tk.Label(hint_frame, text="1. 拖动鼠标选择切割区域", font=("Arial", 10)).pack(anchor=tk.W)
        tk.Label(hint_frame, text="2. 点击√保存，点击×重新选择", font=("Arial", 10)).pack(anchor=tk.W)
        tk.Label(hint_frame, text="3. 缩放按钮可累计，多次点击叠加比例", font=("Arial", 10)).pack(anchor=tk.W)
        tk.Label(hint_frame, text="4. 缩放后裁剪，结果为缩放后实际尺寸", font=("Arial", 10)).pack(anchor=tk.W)
        
        # 右侧区域（图像+导航）
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 图像显示区域（优化渲染）
        self.canvas_frame = tk.Frame(right_frame)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.canvas_frame, bg="#e0e0e0")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 导航按钮区域
        nav_frame = tk.Frame(right_frame, width=60, bg="#f0f0f0")
        nav_frame.pack(side=tk.RIGHT, fill=tk.Y)
        nav_inner_frame = tk.Frame(nav_frame, bg="#f0f0f0")
        nav_inner_frame.pack(expand=True, pady=20)
        self.prev_btn = tk.Button(nav_inner_frame, text="上一张", command=self.prev_image, state=tk.DISABLED, width=8)
        self.prev_btn.pack(pady=5)
        self.next_btn = tk.Button(nav_inner_frame, text="下一张", command=self.next_image, state=tk.DISABLED, width=8)
        self.next_btn.pack(pady=5)
        
        # 绑定鼠标事件
        self.canvas.bind("<Button-1>", self.on_mouse_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)
    
    def update_image_info(self):
        """更新图片信息（新增缩放比例、缩放后分辨率）"""
        if self.image and self.original_image and self.image_path:
            # 原始分辨率 + 当前缩放后分辨率
            orig_w, orig_h = self.original_image.size
            curr_w, curr_h = self.image.size
            self.resolution_var.set(f"原始{orig_w}x{orig_h} | 当前{curr_w}x{curr_h}")
            # 累计缩放比例（保留2位小数）
            self.current_scale_var.set(f"{round(self.base_scale, 2)}x")
            # 文件大小
            if os.path.exists(self.image_path):
                file_size = os.path.getsize(self.image_path)
                self.file_size_var.set(self.file_utils.format_file_size(file_size))
            else:
                self.file_size_var.set("内存中")
        else:
            self.resolution_var.set("-- x --")
            self.current_scale_var.set("1.0x")
            self.file_size_var.set("--")
    
    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"), ("All files", "*")]
        )
        if file_path:
            self.image_path = file_path
            self.image_directory = None
            self.load_image(file_path)
    
    def open_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.image_directory = directory
            self.image_files = self.file_utils.get_image_files(directory)
            if self.image_files:
                self.current_image_index = 0
                self.image_path = self.image_files[self.current_image_index]
                self.load_image(self.image_path)
                self.prev_btn.config(state=tk.DISABLED)
                self.next_btn.config(state=tk.NORMAL if len(self.image_files) > 1 else tk.DISABLED)
    
    def load_image(self, path):
        try:
            self.original_image, self.image = self.image_processor.load_image(path)
            if self.original_image and self.image:
                self.base_scale = 1.0  # 重置累计缩放因子
                self.update_canvas(quick_render=True)  # 快速渲染
                self.update_image_info()
                # 清除裁剪相关状态
                self.canvas.delete("crop_box", "crop_overlay", "resolution_info")
                self.remove_confirm_buttons()
                self.crop_box = None
        except Exception as e:
            print(f"加载图片错误: {e}")
    
    def restore_original_image(self):
        """恢复原始尺寸（重置累计缩放因子）"""
        if self.original_image:
            self.base_scale = 1.0
            self.image = self.original_image.copy()
            self.update_canvas(quick_render=True)
            self.update_image_info()
            # 清除裁剪相关状态
            self.canvas.delete("crop_box", "crop_overlay", "resolution_info")
            self.remove_confirm_buttons()
            self.crop_box = None
            print("已恢复原始图片尺寸")
    
    def scale_image(self, factor):
        """【核心优化】累计缩放图片，快速渲染"""
        if not self.original_image:
            return
        
        # 缩放图片
        scaled_image, new_scale = self.image_processor.scale_image(
            self.original_image, self.base_scale, factor, self.min_scale, self.max_scale
        )
        
        if scaled_image:
            self.image = scaled_image
            self.base_scale = new_scale  # 更新累计缩放因子
            self.update_canvas(quick_render=True)  # 快速渲染到画布
            self.update_image_info()  # 更新缩放信息
            
            # 清除裁剪相关状态（缩放后重新选框）
            self.canvas.delete("crop_box", "crop_overlay", "resolution_info")
            self.remove_confirm_buttons()
            self.crop_box = None
            print(f"图片缩放至{round(new_scale, 2)}x（累计）")
    
    def update_canvas(self, quick_render=False):
        """【优化渲染】快速更新画布，减少延迟"""
        if not self.image:
            return
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        if canvas_width == 1 or canvas_height == 1:
            self.root.after(50, self.update_canvas, quick_render)  # 缩短延迟，快速重试
            return
        
        img_w, img_h = self.image.size
        # 计算适配画布的缩放比例（最大1.0，避免超出画布）
        fit_scale = min(canvas_width / img_w, canvas_height / img_h, 1.0)
        fit_w = int(img_w * fit_scale)
        fit_h = int(img_h * fit_scale)
        
        # 快速渲染：直接缩放为画布适配尺寸，减少内存占用
        render_img = self.image.resize((fit_w, fit_h), Image.LANCZOS if not quick_render else Image.BILINEAR)
        self.tk_image = ImageTk.PhotoImage(render_img)
        
        # 清空画布并绘制（单步操作，减少画布刷新次数）
        self.canvas.delete("all")
        self.canvas.create_image(canvas_width//2, canvas_height//2, image=self.tk_image, anchor=tk.CENTER)
        
        # 保存画布渲染参数（用于裁剪坐标转换）
        self.scale = fit_scale
        self.image_x = (canvas_width - fit_w) // 2
        self.image_y = (canvas_height - fit_h) // 2
        self.image_display_size = (fit_w, fit_h)
    
    def set_size(self, width, height):
        self.size_mode.set("fixed")
        self.crop_width = width
        self.crop_height = height
        self.width_var.set(str(width))
        self.height_var.set(str(height))
        self.canvas.delete("crop_box", "crop_overlay", "resolution_info")
        self.remove_confirm_buttons()
        self.crop_box = None
    
    def apply_custom_size(self):
        try:
            width = int(self.width_var.get())
            height = int(self.height_var.get())
            if width > 0 and height > 0:
                self.size_mode.set("fixed")
                self.crop_width = width
                self.crop_height = height
                self.canvas.delete("crop_box", "crop_overlay", "resolution_info")
                self.remove_confirm_buttons()
                self.crop_box = None
        except ValueError:
            pass
    
    def browse_output_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_directory = directory
            self.output_var.set(directory)
    
    def on_mouse_press(self, event):
        if self.confirm_btn or self.cancel_btn:
            if self.crop_box:
                self.remove_confirm_buttons()
            else:
                return
        self.is_dragging = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.canvas.delete("crop_box", "crop_overlay", "resolution_info")
        self.remove_confirm_buttons()
        self.crop_box = None
    
    def on_mouse_drag(self, event):
        # 初始化变量，避免UnboundLocalError
        x1 = y1 = x2 = y2 = 0
        if self.is_dragging:
            self.canvas.delete("crop_box", "crop_overlay", "resolution_info")
            if self.size_mode.get() == "fixed":
                if hasattr(self, 'crop_width') and hasattr(self, 'scale'):
                    display_w = int(self.crop_width * self.scale)
                    display_h = int(self.crop_height * self.scale)
                    # 鼠标为中心绘制固定尺寸框
                    x1 = event.x - display_w // 2
                    y1 = event.y - display_h // 2
                    x2 = x1 + display_w
                    y2 = y1 + display_h
                    # 限制在图片范围内
                    if hasattr(self, 'image_x'):
                        img_x, img_y = self.image_x, self.image_y
                        img_w, img_h = self.image_display_size
                        x1 = max(img_x, x1)
                        y1 = max(img_y, y1)
                        x2 = min(img_x + img_w, x2)
                        y2 = min(img_y + img_h, y2)
                        # 重新校准中心，保证尺寸不变
                        center_x, center_y = (x1+x2)//2, (y1+y2)//2
                        x1, y1 = center_x - display_w//2, center_y - display_h//2
                        x2, y2 = x1+display_w, y1+display_h
            else:
                # 自定义尺寸框
                x1 = min(self.drag_start_x, event.x)
                y1 = min(self.drag_start_y, event.y)
                x2 = max(self.drag_start_x, event.x)
                y2 = max(self.drag_start_y, event.y)
                # 限制在图片范围内
                if hasattr(self, 'image_x'):
                    img_x, img_y = self.image_x, self.image_y
                    img_w, img_h = self.image_display_size
                    x1 = max(img_x, x1)
                    y1 = max(img_y, y1)
                    x2 = min(img_x + img_w, x2)
                    y2 = min(img_y + img_h, y2)
            
            # 绘制裁剪框和遮罩
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="red", width=2, tags="crop_box")
            if hasattr(self, 'image_x'):
                img_x, img_y = self.image_x, self.image_y
                img_w, img_h = self.image_display_size
                self.canvas.create_rectangle(img_x, img_y, x1, img_y+img_h, fill="gray", stipple="gray50", tags="crop_overlay")
                self.canvas.create_rectangle(x2, img_y, img_x+img_w, img_y+img_h, fill="gray", stipple="gray50", tags="crop_overlay")
                self.canvas.create_rectangle(x1, img_y, x2, y1, fill="gray", stipple="gray50", tags="crop_overlay")
                self.canvas.create_rectangle(x1, y2, x2, img_y+img_h, fill="gray", stipple="gray50", tags="crop_overlay")
            
            # 显示裁剪分辨率
            if self.size_mode.get() == "fixed":
                res_text = f"{self.crop_width}x{self.crop_height}"
            else:
                if hasattr(self, 'scale'):
                    orig_w = max(1, int((x2-x1)/self.scale))
                    orig_h = max(1, int((y2-y1)/self.scale))
                    res_text = f"{orig_w}x{orig_h}"
                else:
                    res_text = ""
            if res_text:
                self.canvas.create_text(x2-10, y1-10, text=res_text, font=("Arial", 10), fill="red", tags="resolution_info")
            self.crop_box = (x1, y1, x2, y2)
    
    def on_mouse_release(self, event):
        self.is_dragging = False
        if self.crop_box:
            self.show_confirm_buttons()
    
    def show_confirm_buttons(self):
        self.remove_confirm_buttons()
        x1, y1, x2, y2 = self.crop_box
        # 绘制确认/取消按钮
        self.confirm_btn = self.canvas.create_text(x2+15, y2+15, text="√", font=("Arial", 12, "bold"), fill="green", tags="confirm_btn")
        self.canvas.tag_bind(self.confirm_btn, "<Button-1>", self.confirm_crop)
        self.cancel_btn = self.canvas.create_text(x2+35, y2+15, text="×", font=("Arial", 12, "bold"), fill="red", tags="cancel_btn")
        self.canvas.tag_bind(self.cancel_btn, "<Button-1>", self.cancel_crop)
    
    def remove_confirm_buttons(self):
        self.canvas.delete("confirm_btn", "cancel_btn")
        self.confirm_btn = None
        self.cancel_btn = None
    
    def confirm_crop(self, event):
        self.cut_current_area()
        self.canvas.delete("crop_box", "crop_overlay", "resolution_info")
        self.remove_confirm_buttons()
        self.crop_box = None
    
    def cancel_crop(self, event):
        self.canvas.delete("crop_box", "crop_overlay", "resolution_info")
        self.remove_confirm_buttons()
        self.crop_box = None
    
    def prev_image(self):
        if self.image_files and self.current_image_index > 0:
            self.current_image_index -= 1
            self.image_path = self.image_files[self.current_image_index]
            self.load_image(self.image_path)
            self.prev_btn.config(state=tk.DISABLED if self.current_image_index == 0 else tk.NORMAL)
            self.next_btn.config(state=tk.NORMAL)
    
    def next_image(self):
        if self.image_files and self.current_image_index < len(self.image_files) - 1:
            self.current_image_index += 1
            self.image_path = self.image_files[self.current_image_index]
            self.load_image(self.image_path)
            self.prev_btn.config(state=tk.NORMAL)
            self.next_btn.config(state=tk.DISABLED if self.current_image_index == len(self.image_files)-1 else tk.NORMAL)
    
    def cut_current_area(self):
        """裁剪当前选中区域，保存为缩放后实际尺寸"""
        if not self.image or not self.crop_box:
            return
        
        # 裁剪图片
        cropped_img = self.image_processor.crop_image(
            self.image, self.crop_box, self.image_x, self.image_y, self.scale
        )
        
        if cropped_img:
            # 保存图片
            self.image_processor.save_image(
                cropped_img, self.output_directory, self.image_path, 
                self.base_scale, self.crop_box, self.image_x, self.image_y, self.scale
            )

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageCutter(root)
    root.mainloop()
