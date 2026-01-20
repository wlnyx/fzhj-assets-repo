import os
from PIL import Image

# ================= 配置区域 =================
source_folder = 'original/weapon'      # 原图文件夹
target_folder = 'compressed/weapon'    # 输出文件夹

# 1. 强力尺寸限制 (单位: 像素)
# 如果图片宽或高超过这个值，会等比例缩小。
# 网页用作图标建议设为 256 或 128。如果不缩放请设为 None
MAX_SIZE = 128 

# 2. JPG 压缩质量 (1-100)
# 之前的 80 比较保守，网页用建议 60-70
JPG_QUALITY = 65

# 3. PNG 颜色压缩 (True/False)
# 开启后会将 PNG 转为 256 色 (8-bit)，体积剧减，但极少数半透明渐变可能会有波纹
PNG_QUANTIZE = True 
# ===========================================

if not os.path.exists(target_folder):
    os.makedirs(target_folder)

print(f"🚀 开始强力压缩...")
print(f"配置: 最大尺寸={MAX_SIZE}px, PNG转256色={PNG_QUANTIZE}, JPG质量={JPG_QUALITY}")

count = 0
saved_size = 0

for filename in os.listdir(source_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
        img_path = os.path.join(source_folder, filename)
        save_path = os.path.join(target_folder, filename)
        
        try:
            with Image.open(img_path) as img:
                # --- 步骤 1: 缩小尺寸 (Resize) ---
                if MAX_SIZE:
                    # 如果宽高任意一边超过限制，就等比例缩小
                    if img.width > MAX_SIZE or img.height > MAX_SIZE:
                        img.thumbnail((MAX_SIZE, MAX_SIZE), Image.Resampling.LANCZOS)

                # --- 步骤 2: 保存与压缩 ---
                if filename.lower().endswith('.png'):
                    if PNG_QUANTIZE:
                        # 核心黑科技：转为 P 模式 (Palette, 256色)
                        # method=2 (FastOctree) 通常对透明图片支持较好
                        # dither=Image.FLOYDSTEINBERG 开启抖动让颜色过渡自然
                        img = img.convert('P', palette=Image.ADAPTIVE, colors=256)
                    
                    img.save(save_path, optimize=True)
                
                else:
                    # 处理 JPG / WebP
                    if img.mode == 'RGBA':
                        img = img.convert('RGB') # JPG 不支持透明
                    img.save(save_path, quality=JPG_QUALITY, optimize=True)
                
                # 计算节省了多少空间
                org_size = os.path.getsize(img_path)
                new_size = os.path.getsize(save_path)
                saved_size += (org_size - new_size)
                count += 1
                
        except Exception as e:
            print(f"❌ 出错: {filename}, 原因: {e}")

# 转换单位显示
saved_mb = saved_size / 1024 / 1024
print(f"\n✅ 全部完成！共处理 {count} 张图片。")
print(f"🎉 累计节省空间: {saved_mb:.2f} MB")