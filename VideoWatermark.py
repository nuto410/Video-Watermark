# pip install moviepy

from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from PIL import Image
import shutil

if not shutil.which("ffmpeg"):
    print("FFmpeg 未安装，请先安装 FFmpeg 並添加到系統環境變量")
    exit()

# 加載視頻文件
# video = VideoFileClip("video.mp4")
video = VideoFileClip("video.mkv")

# 視頻文件 長寬
Vwidth, Vheight = video.size

# 加載圖片文件
image = ImageClip("image.png")

# 使用PIL調整圖片大小
scale_factor = 0.5  # 圖片占視頻的比例(0.5=50%)
new_width = int(Vwidth * scale_factor)
new_height = int(Vheight * scale_factor)
image = image.resize((new_width, new_height))

image = image.set_duration(5)  # 圖片持續時間(秒)
image = image.set_position(("center", "center"))  # 圖片位置
image = image.set_start(10)  # 圖片插入時間

# 合成視頻
final_video = CompositeVideoClip([video, image])

# 保存新視頻
# final_video.write_videofile("output_video.mp4", codec="libx264", fps=24)
final_video.write_videofile("output_video.mkv", codec="libx264", fps=24)
