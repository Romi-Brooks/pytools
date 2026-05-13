# PyTools - 自用 Python 小工具集

基于 Python 3.x + tkinter 构建的桌面小工具集合，提供统一的 GUI 启动入口。

## 项目结构

```
pytools/
├── main_gui.py                  # 主入口 - 统一启动所有工具
├── requirements.txt             # Python 依赖
├── LICENSE
└── tools/
    ├── pic_clipper/             # 图像预处理切分工具
    ├── sovits_tts/              # GPT-SoVITS 语音合成客户端
    ├── m4s_merger/              # B站缓存视频合并工具
    └── free4_get/               # free4.xyz 内容获取工具
```

## 环境准备

### Python 环境
确保已安装 Python 3.8+。

### 安装依赖
```bash
pip install -r requirements.txt
```

### 外部依赖
- **FFmpeg**：m4s_merger 工具需要 FFmpeg 用于视频合并，请确保 `ffmpeg` 命令可在命令行中访问
- **GPT-SoVITS**：sovits_tts 工具需要本地运行 GPT-SoVITS API 服务（默认端口 9880）

## 快速开始

```bash
python main_gui.py
```

启动主界面后点击对应按钮即可打开各工具。

## 工具说明

### 1. 图像预处理切分工具 (pic_clipper)
对图片进行固定尺寸或自定义尺寸切割，支持：
- 固定尺寸切割（以鼠标为中心拖动裁剪框）
- 自定义尺寸切割（自由拖动选择区域）
- 常用尺寸快捷按钮（512x512, 768x768, 1024x1024, 768x512, 512x768）
- 累计缩放功能（0.2x ~ 5.0x）
- 批量处理目录内所有图片
- 裁剪框带灰色遮罩和分辨率标注

### 2. GPT-SoVITS API 调用 (sovits_tts)
GPT-SoVITS 语音合成客户端，支持：
- 文本转语音合成
- 参考音频与参考文本设置
- GPT 模型 / SoVITS 模型切换
- 推理参数调节（采样步数、top_k、top_p、温度、语速等）
- 文本分段合成
- 并行推理与音频超采样
- 合成进度实时显示 + 音频播放

### 3. B站缓存视频合并 (m4s_merger)
将 Bilibili 客户端缓存的 `audio.m4s` + `video.m4s` 无损合并为 mp4，支持：
- 自动遍历缓存目录查找 `entry.json`
- 解析视频标题与分P信息
- 自动创建 output 输出目录
- 防重复命名（自动添加时间戳）
- 支持自定义 FFmpeg 路径

### 4. free4.xyz 内容获取 (free4_get)
从 free4.xyz 网站获取最新内容或搜索内容，支持：
- 获取网站最新内容
- 关键词搜索
- 查看下载链接（KatFile / RapidGator / NitroFlare）

## License

MIT
