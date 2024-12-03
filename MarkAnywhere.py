import os
import random
from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
import shutil

# 檢查是否已安裝FFmpeg
if not shutil.which("ffmpeg"):
    print("FFmpeg 未安裝，請先安裝 FFmpeg 並添加到系統環境變量。\n該軟體用於處理影片文件。\n可使用指令 ffmpeg -version 確認是否安裝。")
    exit()

# 加載影片文件
video = VideoFileClip("video.mp4")
# video = VideoFileClip("video.mkv")

# 影片文件 長寬
Vwidth, Vheight = video.size

# 從 "watermarks" 資料夾中讀取圖片
watermark_folder = "watermarks"  # 設定圖片資料夾路徑
image_files = [f for f in os.listdir(watermark_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]  # 只選擇圖片文件

# 檢查資料夾內是否有圖片
if not image_files:
    print("水印資料夾中沒有圖片，請確保 'watermarks' 資料夾內有圖片。")
    exit()

# 設定圖片的縮放比例
scale_factor = 0.1  # 0.1=10% 的縮放比例
image_duration = 0.5  # 每個水印出現的時間長度（秒）
num_watermarks = 20  # 要添加的水印數量

# 檢查圖片是否有超過影片的尺寸，並過濾掉不符合的圖片
valid_images = []

for image_file in image_files:
    image_path = os.path.join(watermark_folder, image_file)
    image = ImageClip(image_path).set_duration(image_duration)  # 確保每個圖片初始持續時間為 image_duration
    Iwidth, Iheight = image.size

    # 使用PIL調整圖片大小(比例調整圖片大小)
    Iwidth = int(Iwidth * scale_factor)
    Iheight = int(Iheight * scale_factor)

    # 如果圖片尺寸大於影片尺寸，則過濾掉這張圖片
    if Iwidth <= Vwidth and Iheight <= Vheight:
        valid_images.append(image.resize((Iwidth, Iheight)))  # 預先縮放圖片
    else:
        print(f"圖片 {image_file} 尺寸大於影片尺寸，將不會使用此圖片作為水印。")

# 檢查是否有有效的水印圖片
if not valid_images:
    print("所有圖片尺寸均大於影片尺寸，請調整圖片尺寸。")
    exit()

# 計算所有不重疊的水印時間段
watermarks = []
used_times = []  # 記錄已使用的時間段，防止重疊

# 設定最大嘗試次數，防止無限循環
max_attempts = 100
attempts = 0

# 添加水印
for _ in range(num_watermarks):
    if attempts >= max_attempts:
        print("達到最大嘗試次數，跳過生成新的水印。")
        break

    # 隨機選擇一個不重疊的時間段
    start_time = random.uniform(0, video.duration - image_duration)  # 隨機選擇出現時間
    overlap = False
    for (start, duration) in used_times:
        if (start_time < start + duration) and (start_time + image_duration > start):
            overlap = True
            break

    if overlap:
        attempts += 1
        continue  # 如果有重疊，跳過當前嘗試並繼續嘗試下一個時間段

    used_times.append((start_time, image_duration))  # 記錄當前時間段

    # 隨機選擇水印圖片
    selected_image = random.choice(valid_images)  # 從有效圖片列表中隨機選擇

    # 設置水印的透明度（範圍 0.0 到 1.0，1.0 為完全不透明）
    opacity = 0.6  # 設置為60%的透明度
    watermark = selected_image.set_opacity(opacity)  # 設置透明度

    # 隨機選擇位置 (允許超出畫面)
    x_pos = random.randint(-selected_image.w, Vwidth)  # 橫向位置（允許部分超出左側）
    y_pos = random.randint(-selected_image.h, Vheight)  # 縱向位置（允許部分超出上方）

    watermark = watermark.set_start(start_time)  # 設置水印的出現時間
    watermark = watermark.set_duration(image_duration)  # 設置水印的持續時間
    watermark = watermark.set_position((x_pos, y_pos))  # 設置水印的位置
    watermarks.append(watermark)

# 確保每次只有一個水印顯示
final_video = CompositeVideoClip([video] + watermarks)

# 保存新影片
final_video.write_videofile("markanywhere_video.mp4", codec="libx264", fps=24)
# final_video.write_videofile("markanywhere_video.mkv", codec="libx264", fps=24)
