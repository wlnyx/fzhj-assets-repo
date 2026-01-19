import os
from PIL import Image # 需要安装: pip install Pillow

# 配置
source_folder = 'original/weapon'      # 原图文件夹名
target_folder = 'compressed/weapon'    # 压缩图文件夹名
quality_val = 80                # 压缩质量 (1-100)，80通常肉眼看不出区别

# 确保目标文件夹存在
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

print(f"开始从 {source_folder} 压缩到 {target_folder} ...")

for filename in os.listdir(source_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        img_path = os.path.join(source_folder, filename)
        save_path = os.path.join(target_folder, filename)
        
        try:
            with Image.open(img_path) as img:
                # 如果是PNG，保持RGBA格式以保留透明度
                if filename.lower().endswith('.png'):
                    # PNG 压缩通常通过 quantize 或保存时的 optimize 参数
                    # 这里使用简单的 optimize 模式
                    img.save(save_path, optimize=True, quality=quality_val)
                else:
                    # JPG/WEBP 直接压缩
                    img.save(save_path, quality=quality_val)
            print(f"已处理: {filename}")
        except Exception as e:
            print(f"出错: {filename}, 原因: {e}")

print("全部完成！")