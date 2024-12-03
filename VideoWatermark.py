# pip install moviepy

from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip
from PIL import Image
import shutil

if not shutil.which("ffmpeg"):
    print("FFmpeg 未安装，请先安装 FFmpeg 並添加到系統環境變量")
    exit()

# 加載視頻文件
video = VideoFileClip("video.mp4")
# video = VideoFileClip("video.mkv")

# 視頻文件 長寬
Vwidth, Vheight = video.size

# 加載圖片文件
image = ImageClip("image.png")

# 圖片 長寬
Iwidth, Iheight = image.size

# 使用PIL調整圖片大小(比例調整圖片大小)
scale_factor = 0.1  # 0.5=50%
Iwidth = int(Iwidth * scale_factor)
Iheight = int(Iheight * scale_factor)
image = image.resize((Iwidth, Iheight))
print("調整後圖片尺寸:", image.size)

if Iwidth > Vwidth or Iheight > Vheight:
    print(Iwidth, Vwidth, Iheight, Vheight)
    print("圖片尺寸大於視頻尺寸，請調整圖片尺寸")
    exit()

image = image.set_duration(3)  # 圖片持續時間(秒)
image = image.set_position(("center", "center"))  # 圖片位置
# set_position options
# ("left", "top")  # 左上 ("center", "top"))  # 上中 ("right", "top")  # 右上 ("left", "center")  # 左中 ("center", "center")  # 中心 ("right", "center")  # 右中 ("left", "bottom")  # 左下 ("center", "bottom")  # 下中 ("right", "bottom")  # 右下
image = image.set_start(5)  # 圖片插入時間

# 合成視頻
final_video = CompositeVideoClip([video, image])

# 保存新視頻
final_video.write_videofile("output_video.mp4", codec="libx264", fps=24)
# final_video.write_videofile("output_video.mkv", codec="libx264", fps=24)
