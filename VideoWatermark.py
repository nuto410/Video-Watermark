# pip install moviepy
from moviepy import editor

from moviepy.editor import VideoFileClip, TextClip, ImageClip, CompositeVideoClip
from PIL import Image
import shutil
import os

# 设置 ImageMagick 路径
import moviepy.config as mpy_config
mpy_config.IMAGEMAGICK_BINARY = r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"

if not shutil.which("ffmpeg"):
    print("FFmpeg 未安装，请先安装 FFmpeg 並添加到系統環境變量。\n該軟體用於處理視頻文件。\n可使用指令ffmpeg -version確認是否安裝。")
    exit()

if not shutil.which("magick"):
    print("ImageMagick 未安裝，請先安裝 ImageMagick 並添加到系統環境變量。\n該軟體用於處理圖片文件。\n可使用指令magick -version確認是否安裝。")
    exit()

# 加載視頻文件
video = VideoFileClip("video.mp4")
# video = VideoFileClip("video.mkv")

# 視頻文件 長寬
Vwidth, Vheight = video.size

#  圖片浮水印       ############################################################################################################

# 加載圖片文件
# image = ImageClip("image.jpg")
image = ImageClip("image.png")
# image = VideoFileClip("image.gif")

# 圖片 長寬
Iwidth, Iheight = image.size

# 使用PIL調整圖片大小(比例調整圖片大小)
scale_factor = 0.3  # 0.5=50%
Iwidth = int(Iwidth * scale_factor)
Iheight = int(Iheight * scale_factor)
image = image.resize((Iwidth, Iheight))
print("調整後圖片尺寸:", image.size)

if Iwidth > Vwidth or Iheight > Vheight:
    print(Iwidth, Vwidth, Iheight, Vheight)
    print("圖片尺寸大於視頻尺寸，請調整圖片尺寸")
    exit()

image = image.set_duration(10)  # 圖片持續時間(秒)
image = image.set_position(("center", "center"))  # 圖片位置
# set_position options
# ("left", "top")  # 左上 ("center", "top"))  # 上中 ("right", "top")  # 右上 ("left", "center")  # 左中 ("center", "center")  # 中心 ("right", "center")  # 右中 ("left", "bottom")  # 左下 ("center", "bottom")  # 下中 ("right", "bottom")  # 右下
image = image.set_start(5)  # 圖片插入時間


#  圖片浮水印       ############################################################################################################

# 文字浮水印       #############################################################################################################
# import matplotlib.font_manager as fm

# # 獲取系統中所有的字體文件
# fonts = fm.findSystemFonts(fontpaths=None, fontext='ttf')

# # 印出所有字體文件位置
# for font in fonts:
#     print(font)

# # 創建文字浮水印
# text = "Your Watermark Text"  # 要顯示的浮水印文字
# font_size = 50  # 字體大小

# # 創建 TextClip 物件
# text_clip = TextClip(text, fontsize=font_size, color='white', font="Arial", stroke_width=2, stroke_color='black')

# # 設定文字的持續時間（與視頻長度一致）
# text_clip = text_clip.set_duration(video.duration)

# # 設定文字的位置（可以選擇 "center", "top", "bottom" 等）
# text_clip = text_clip.set_position(("center", "bottom"))  # 範例：底部居中

# 文字均勻覆蓋影片
# 設定每個文字片段的內容和屬性
text = "Text"
font_size = 30
text_clip = TextClip(text, fontsize=font_size, color='white', font="Arial", stroke_width=2, stroke_color='black')

# 獲取視頻的寬度和高度
Vwidth, Vheight = video.size

# 计算每个文字片段的宽度和高度
text_width, text_height = text_clip.size

# 设置每列和每行的数量（可以根据需要调整）
cols = 10  # 设置列数
rows = 6   # 设置行数

# 计算每列之间的间隔，确保文字不会重叠
x_gap = (Vwidth - (cols * text_width)) / (cols + 1)
y_gap = (Vheight - (rows * text_height)) / (rows + 1)

# 创建并定位多个文字片段，均匀分布
text_clips = []
for row in range(rows):
    for col in range(cols):
        # 计算每个文字的位置，考虑文字宽度和高度
        x = (col + 1) * x_gap + col * text_width  # 文字的水平位置
        y = (row + 1) * y_gap + row * text_height  # 文字的垂直位置

        # 创建并设置每个文字片段的位置
        # text_clip_instance = text_clip_instance.rotate(rotation_angle) #文字旋轉
        text_clip_instance = text_clip.set_position((x, y)).set_start(0).set_duration(video.duration)
        text_clips.append(text_clip_instance)

# 創建跑馬燈文字
# text = "This is a scrolling watermark text"  # 要顯示的文字
# font_size = 50  # 字體大小
# text_clip = TextClip(text, fontsize=font_size, color='white', font="Arial", stroke_width=2, stroke_color='black')

# # 設定文字的持續時間（與視頻長度一致）
# text_clip = text_clip.set_duration(video.duration)

# # 計算文字寬度，並設置文字從右側滾動到左側
# text_width = text_clip.size[0]
# text_clip = text_clip.set_position(lambda t: (Vwidth - (t * (Vwidth + text_width) / video.duration), Vheight - font_size - 10))


# 文字浮水印       #############################################################################################################



# # 將文字疊加到視頻上
# final_video = CompositeVideoClip([video, text_clip])
# 將文字均勻分布到視頻上
final_video = CompositeVideoClip([video, image] + text_clips)
# # 將圖片疊加到視頻上
# final_video = CompositeVideoClip([video, image])
# 將文字和圖片疊加到視頻上
# final_video = CompositeVideoClip([video, text_clip, image])

# 保存新視頻
final_video.write_videofile("output_video.mp4", codec="libx264", fps=24)
# final_video.write_videofile("output_video.mkv", codec="libx264", fps=24)
