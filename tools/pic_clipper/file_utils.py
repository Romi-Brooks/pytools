import os
import math

class FileUtils:
    def __init__(self):
        pass
    
    def format_file_size(self, size_bytes):
        """
        格式化文件大小为易读格式
        
        Args:
            size_bytes: 文件大小（字节）
            
        Returns:
            str: 格式化后的文件大小
        """
        if size_bytes == 0:
            return "0 B"
        size_names = ["B", "KB", "MB", "GB", "TB"]
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"
    
    def get_image_files(self, directory):
        """
        获取目录中的所有图片文件
        
        Args:
            directory: 目录路径
            
        Returns:
            list: 图片文件路径列表
        """
        if not directory or not os.path.exists(directory):
            return []
        
        image_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif'))]
        return image_files
    
    def ensure_directory(self, directory):
        """
        确保目录存在
        
        Args:
            directory: 目录路径
        """
        if not os.path.exists(directory):
            os.makedirs(directory)
