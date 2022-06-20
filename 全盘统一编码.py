import os
from 通用函数 import get_file_path, del_all_empty_folder
from 函数.转格式函数 import convertFormat
from mutagen.mp4 import MP4, MP4Cover
import shutil
import sys
import datetime

dir = "G:\\209.244.191.4服务器备份\\ziyuan\\data\\test.backup\\dir_uploadify"

# have_cover = False

# 可接受的视频流格式。
vedioFormat = ["mp4", "mkv", "avi", "ts", "wmv", "ts", "rmvb", "3gp", "mov", "mpg"]


def addCover(filename, cover):
    audio = MP4(filename)
    data = open(cover, 'rb').read()
    covr = []
    if cover.endswith('png'):
        covr.append(MP4Cover(data, MP4Cover.FORMAT_PNG))
    else:
        covr.append(MP4Cover(data, MP4Cover.FORMAT_JPEG))
    audio.clear()
    audio['covr'] = covr
    audio.save()
    print(filename + " 内嵌图片：" + cover + "。")


tem = []
for parent,dirnames,filenames in os.walk(dir):
    for filename in filenames:
        tem.append(os.path.join(parent,filename))

# get_file_path(dir, tem, [], all_level=True)

files = []
for i in tem:
    for j in vedioFormat:
        if i.endswith(j):
            files.append(i)
            break

all_video_num = len(files)
count = 0
for i in files:
    count = count + 1
    time = datetime.datetime.now().strftime('%H:%M:%S')
    print("正在处理第" + str(count) + "/" + str(all_video_num) + "个视频：" + i + " " + time)
    input = i
    inputDir = os.path.split(input)[0]
    outputDir = os.path.join(inputDir, "output")
    output = os.path.join(outputDir,
                          str(os.path.split(input)[1][:-len(input.split(".")[-1])]) + "mp4")

    # 转编码
    video_type = os.path.splitext(i)[-1]
    result = convertFormat(i, silence=True)

    # 防止出现转换失败
    if os.path.exists(output):
        file_size = os.path.getsize(output)
        if file_size == 0:
            os.remove(output)
            result = convertFormat(i, silence=True, parameter='-max_muxing_queue_size 1024')

    print(result)

    # 有的视频格式正确，不用转，也就不用处理封面
    if os.path.exists(output):
        # 提取封面
        try:
            audio = MP4(i)
            cover = audio['covr'][0]
        except:
            cover = None
        if cover:
            with open(os.path.join(outputDir, "c.jpg"), 'wb') as f:
                f.write(cover)

            # 重新添加封面
            addCover(output, os.path.join(outputDir, "c.jpg"))

            # 删除封面
            os.remove(os.path.join(outputDir, "c.jpg"))

        # 删除源文件
        os.remove(i)

        # 将转编码后的视频放到源文件的位置
        i = os.path.splitext(i)[0] + ".mp4"
        shutil.move(output, i)
        os.rmdir(outputDir)
    else:
        # 如果编码正确，将文件重命名为mp4后缀。
        file_ex_name = os.path.splitext(i)[-1]
        if not file_ex_name == ".mp4":
            new = os.path.splitext(i)[0] + ".mp4"
            shutil.move(i, new)
            os.rmdir(outputDir)

del_all_empty_folder(dir)