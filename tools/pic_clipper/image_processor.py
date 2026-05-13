from PIL import Image
import os

class ImageProcessor:
    def __init__(self):
        pass
    
    def load_image(self, path):
        """
        加载图片
        
        Args:
            path: 图片路径
            
        Returns:
            tuple: (original_image, current_image)
        """
        try:
            original_image = Image.open(path).convert("RGB")  # 统一格式，避免透明通道问题
            current_image = original_image.copy()
            return original_image, current_image
        except Exception as e:
            print(f"加载图片错误: {e}")
            return None, None
    
    def scale_image(self, original_image, base_scale, factor, min_scale, max_scale):
        """
        缩放图片
        
        Args:
            original_image: 原始图片
            base_scale: 当前缩放比例
            factor: 缩放因子
            min_scale: 最小缩放比例
            max_scale: 最大缩放比例
            
        Returns:
            tuple: (scaled_image, new_scale)
        """
        if not original_image:
            return None, base_scale
        
        # 计算新的累计缩放因子
        new_scale = base_scale * factor
        # 限制缩放边界
        if new_scale < min_scale or new_scale > max_scale:
            print(f"缩放限制：已达{min_scale}x~{max_scale}x边界")
            return None, base_scale
        
        # 基于原始图片计算缩放后尺寸
        orig_w, orig_h = original_image.size
        new_w = int(orig_w * new_scale)
        new_h = int(orig_h * new_scale)
        
        # 缩放图片
        scaled_image = original_image.resize((new_w, new_h), Image.LANCZOS)
        
        return scaled_image, new_scale
    
    def crop_image(self, image, crop_box, image_x, image_y, scale):
        """
        裁剪图片
        
        Args:
            image: 要裁剪的图片
            crop_box: 裁剪框坐标 (x1, y1, x2, y2)
            image_x: 图片在画布上的x坐标
            image_y: 图片在画布上的y坐标
            scale: 画布缩放比例
            
        Returns:
            Image: 裁剪后的图片
        """
        if not image or not crop_box:
            return None
        
        x1, y1, x2, y2 = crop_box
        # 转换为当前缩放后图片的实际坐标（边界校验）
        orig_x1 = max(0, int((x1 - image_x) / scale))
        orig_y1 = max(0, int((y1 - image_y) / scale))
        orig_x2 = min(image.width, int((x2 - image_x) / scale))
        orig_y2 = min(image.height, int((y2 - image_y) / scale))
        
        if orig_x2 <= orig_x1 or orig_y2 <= orig_y1:
            print("无效的裁剪区域，请重新选择")
            return None
        
        # 裁剪图片
        cropped_img = image.crop((orig_x1, orig_y1, orig_x2, orig_y2))
        return cropped_img
    
    def save_image(self, image, output_dir, image_path, base_scale, crop_box, image_x, image_y, scale):
        """
        保存裁剪后的图片
        
        Args:
            image: 裁剪后的图片
            output_dir: 输出目录
            image_path: 原始图片路径
            base_scale: 缩放比例
            crop_box: 裁剪框坐标
            image_x: 图片在画布上的x坐标
            image_y: 图片在画布上的y坐标
            scale: 画布缩放比例
            
        Returns:
            str: 保存的文件路径
        """
        if not image:
            return None
        
        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # 计算裁剪坐标
        x1, y1, x2, y2 = crop_box
        orig_x1 = max(0, int((x1 - image_x) / scale))
        orig_y1 = max(0, int((y1 - image_y) / scale))
        
        # 生成文件名
        if image_path:
            base_name = os.path.basename(image_path)
            name, ext = os.path.splitext(base_name)
        else:
            name, ext = "cut", ".png"
        
        output_path = os.path.join(output_dir, f"{name}_scale{round(base_scale,2)}_cut_{orig_x1}_{orig_y1}{ext}")
        
        # 高质量保存
        image.save(output_path, quality=100, optimize=True)
        print(f"裁剪图片保存至: {output_path}")
        return output_path
