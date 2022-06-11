# coding=utf-8

import datetime
import os
import ffmpeg

str_video_path = ".\\RAW"
str_new_path = ".\\_OUTPUT"
map_old_new_path = {}
str_file_result = "./_OUTPUT/_result.txt"
str_file_mkdir_state = "./_OUTPUT/_mkdir_state.txt"

# 多文件夹复制
def mkdir_multi(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    else:
        return False

# 多文件夹的复制 以及 多绝对路径文件名的获取对应
def get_files_and_mkdir_mutil(video_path, new_path):
    list_file_path_name = []
    list_file_path = []
    # list_new_file_path_name = []
    list_new_file_path = []
    # 获取绝对路径的文件名 以及 多文件夹名
    for filepath,dirnames,filenames in os.walk(video_path):
        for filename in filenames:
            # 判断是否为MP4结尾
            if filename[-3:] == 'mp4' or filename[-3:] == 'MP4':
                list_file_path_name.append(os.path.join(filepath,filename))
        list_file_path.append(filepath)
    # 将最新文件夹路径字符串放到list_new_file_path
    for filepath in list_file_path:
        list_new_file_path.append(filepath.replace(video_path, new_path, 1))
    # 将最新文件名和视频文件名放到字典 map_old_new_path 做对应
    for filename in list_file_path_name:
        map_old_new_path[filename] = filename.replace(video_path, new_path, 1)
        # print(filename, filename.replace(video_path, new_path, 1))
    # 复制多文件夹到新的路径下
    if os.path.isfile(str_file_mkdir_state):
        os.remove(str_file_mkdir_state)
    file = open(str_file_mkdir_state, 'a+')
    for filepath in list_new_file_path:
        if mkdir_multi(filepath):
            file.writelines(filepath + "\t Success\n")
            # print(filepath, "S")
        else:
            file.writelines(filepath + "\t Failed\n")
            # print(filepath, "F")
    file.close()

# 时间格式处理
def get_ffmpeg_format_time(second):
    m, s = divmod(int(second), 60)
    h, m = divmod(m, 60)
    ft_end = '{:.2f}'.format(round(second%1, 2))
    # print(h, m, s, ft_end)
    str_time = str(h)+'-'+str(m)+'-'+str(s)
    time_format = datetime.datetime.strptime(str_time, '%H-%M-%S')
    # print(time_format)
    return str(time_format)[11:]+str(ft_end)[1:]
    # return strTimeLen

# system 命令执行
def do_system_cmd(cmd_crop, cmd_splicing):
    os.system('echo off')
    os.system(cmd_crop)
    os.system(cmd_splicing)

if __name__ == '__main__':
    # 获取文件绝对地址名 复制文件夹名
    get_files_and_mkdir_mutil(str_video_path, str_new_path)

    # videoList = os.listdir(str_video_path)
    # for file_name in videoList:
    #     if file_name[-3:] == 'mp4' or file_name[-3:] == 'MP4':
    #         map_old_new_path[str(str_video_path+file_name)] = str(str_new_path+file_name)
    # print(map_old_new_path)

    time_begin = float(ffmpeg.probe(str('./ADD/begin.mp4'))['format']['duration'])
    time_end = float(ffmpeg.probe(str('./ADD/end.mp4'))['format']['duration'])
    # print(time_begin, time_end)
    # str_time_begin = get_ffmpeg_format_time(time_begin)   # 开始时间格式处理
    # print(str_time_begin)

    if os.path.isfile(str_file_result):
        os.remove(str_file_result)

    # 先剪切视频，将视频直接压缩2500Kbps码率  之后转成ts格式，直接进行拼接
    for video_name in map_old_new_path.keys():
        timeVideo = float(ffmpeg.probe(video_name)['format']['duration'])
        # print(timeVideo)
        timeVideo = timeVideo - time_end
        # print(timeVideo)
        str_time_video = get_ffmpeg_format_time(timeVideo)
        # print(str_time_video)
        if os.path.isfile("./TMP.mp4"):
            os.remove('./TMP.mp4')
        str_cmd_crop = "ffmpeg.exe -ss 00:00:00.00  -i " + video_name +\
            " -vcodec copy -acodec copy -t " + str_time_video +" TMP.mp4 -y"
        # print(str_cmd_crop)
        os.system(str_cmd_crop)

        str_cmd_compress = "ffmpeg.exe -i .\\TMP.mp4 -b 2500K .\\compress_output.mp4 -y"
        os.system(str_cmd_compress)

        str_cmd_mp42ts = "ffmpeg.exe -i .\\compress_output.mp4 -c:v copy .\\compress_output.ts -y"
        os.system(str_cmd_mp42ts)

        str_cmd_concat = "ffmpeg.exe -i \"concat:compress_output.ts|.\\ADD\\end.ts\" -c copy " + map_old_new_path[video_name] + " -y"
        print(str_cmd_concat)
        os.system(str_cmd_concat)

        result = open(str_file_result, 'a+')
        new_video_size = int(int(ffmpeg.probe(map_old_new_path[video_name])['format']['size']) / 1024 / 1024)
        if new_video_size > 500 :
            result.writelines(map_old_new_path[video_name] + "\t SIZE:OverFlower 500M" + '\t Completed\n')
        else:
            result.writelines(map_old_new_path[video_name] + "\t SIZE:" + str(new_video_size) + 'M' + '\t Completed\n')
        result.close()












    # 问题：某些视频会出现 More than 1000 frames duplicated 导致剪切视频特别长
    # for video_name in map_old_new_path.keys():
    #     timeVideo = float(ffmpeg.probe(video_name)['format']['duration'])
    #     # print(timeVideo)
    #     timeVideo = timeVideo - time_end
    #     # print(timeVideo)
    #     str_time_video = get_ffmpeg_format_time(timeVideo)
    #     # print(str_time_video)
    #     if os.path.isfile("./TMP.mp4"):
    #         os.remove('./TMP.mp4')
    #     str_cmd_crop = "ffmpeg.exe -ss 00:00:00.00  -i " + video_name +\
    #         " -vcodec copy -acodec copy -t " + str_time_video +" TMP.mp4 -y"
    #     # print(str_cmd_crop)
    #     os.system(str_cmd_crop)
    #
    #     if int(int(ffmpeg.probe(video_name)['format']['bit_rate']) / 1000) >= 10000:
    #         str_cmd_compress = "ffmpeg.exe -i .\\TMP.mp4 -b 2500K .\\compree_output.mp4 -y"
    #         os.system(str_cmd_compress)
    #
    #         str_cmd_splicing = "ffmpeg.exe -i .\\compree_output.mp4 -i .\\ADD\\end.mp4 -filter_complex \"[0:0] [0:1] [1:0] [1:1] concat=n=2:v=1:a=1 [v] [a]\" -map \"[v]\" -map \"[a]\" -b 2500K " + map_old_new_path[video_name] + " -y"
    #         print(str_cmd_splicing)
    #         os.system(str_cmd_splicing)
    #
    #     else:
    #         str_cmd_splicing = "ffmpeg.exe -i .\\TMP.mp4 -i .\\ADD\\end.mp4 -filter_complex \"[0:0] [0:1] [1:0] [1:1] concat=n=2:v=1:a=1 [v] [a]\" -map \"[v]\" -map \"[a]\" -b 2500K " + map_old_new_path[video_name] + " -y"
    #         # print(str_cmd_splicing)
    #         os.system(str_cmd_splicing)
    #
    #     # do_system_cmd(str_cmd_crop,str_cmd_splicing)
    #
    #     result = open(str_file_result, 'a+')
    #     new_video_size = int(int(ffmpeg.probe(map_old_new_path[video_name])['format']['size']) / 1024 / 1024)
    #     if new_video_size > 500 :
    #         result.writelines(map_old_new_path[video_name] + "\t SIZE:OverFlower 500M" + '\t Completed\n')
    #     else:
    #         result.writelines(map_old_new_path[video_name] + "\t SIZE:" + str(new_video_size) + 'M' + '\t Completed\n')
    #
    #     result.close()













# for videoname in list_old_new_path.keys():
#         timeVideo = float(ffmpeg.probe(videoname)['format']['duration'])
#         # print(timeVideo)
#         timeVideo = timeVideo - time_end # -time_begin;
#         # print(timeVideo)
#         str_time_video = get_ffmpeg_format_time(timeVideo)
#         # print(str_time_video)
#         if os.path.isfile("./TMP.mp4"):
#             os.remove('./TMP.mp4')
#         str_cmd_crop = "ffmpeg.exe -ss 00:00:00.00  -i "+videoname+\
#             " -vcodec copy -acodec copy -t "+str_time_video+" TMP.mp4 -y"
#         # print(str_cmd_crop)
#         os.system(str_cmd_crop)
#
#         str_cmd_MP42TS = "ffmpeg.exe -i TMP.mp4 -c:v copy TMP.ts -y"
#         # print(str_cmd_MP42TS)
#         os.system(str_cmd_MP42TS)
#
#         str_cmd_splicing = "ffmpeg.exe -i \"concat:TMP.ts|.\ADD\end.ts\" -c copy output.ts -y"
#         # print(str_cmd_splicing)
#         os.system(str_cmd_splicing)
#
#         str_cmd_TS2MP4 = "ffmpeg.exe -y -i output.ts -c:v copy " + list_old_new_path[videoname]
#         # print(str_cmd_TS2MP4)
#         os.system(str_cmd_TS2MP4)
#
#         # do_system_cmd(str_cmd_crop,str_cmd_splicing)
#
#         result = open(sre_result, 'a+')
#         result.writelines(list_old_new_path[videoname]+'\t Completed\n')
#         result.close()


# for videoname in list_old_new_path.keys():
#         timeVideo = float(ffmpeg.probe(videoname)['format']['duration'])
#         # print(timeVideo)
#         timeVideo = timeVideo - time_end -time_begin;
#         # print(timeVideo)
#         str_time_video = get_ffmpeg_format_time(timeVideo)
#         print(str_time_video)
#         if os.path.isfile("./TMP.mp4"):
#             os.remove('./TMP.mp4')
#         str_cmd_crop = "ffmpeg.exe -ss "+str_time_begin+" -i "+videoname+\
#             " -vcodec copy -acodec copy -t "+str_time_video+" ./TMP.mp4 -y"
#         print(str_cmd_crop)
#
#         str_cmd_splicing = "ffmpeg.exe -y -i .\\ADD\\begin.mp4 -i .\\TMP.mp4 -i .\\ADD\\end.mp4 -filter_complex \"[0:0] [0:1] [1:0] [1:1] [2:0] [2:1] concat=n=3:v=1:a=1 [v] [a]\" -map \"[v]\" -map \"[a]\" "+list_old_new_path[videoname]
#         print(str_cmd_splicing)
#
#         do_system_cmd(str_cmd_crop,str_cmd_splicing)
#
#         result = open(sre_result, 'a+')
#         result.writelines(list_old_new_path[videoname]+'\t Completed\n')
#         result.close()





# if os.path.isfile('./tmp.txt'):
#    os.remove("./tmp.txt")
# file = open('./tmp.txt', 'a')
# str_content = "file .\\\ADD\\\\begin.mp4 \nfile .\\\TMP.mp4 \nfile .\\\ADD\\\\end.mp4"
# str_content = "file ./ADD/begin.mp4 \nfile ./TMP.mp4 \nfile ./ADD/end.mp4"
# file.write(str_content)

# str_cmd_splicing = "ffmpeg.exe -f concat -safe 0 -i tmp.txt -c copy "+list_old_new_path[videoname]
# print(str_cmd_splicing)

# do_system_cmd(str_cmd_crop, str_cmd_splicing)
# os.system('ipconfig')

# os.system("pause")
# run(str_cmd_splicing)


# "ffmpeg.exe -i .\\ADD\\begin.mp4 -i .\\TMP.mp4 -i .\\ADD\\end.mp4 -filter_complex '[0:0] [0:1] [1:0] [1:1] [2:0] [2:1] concat=n=3:v=1:a=1 [v] [a]' -map '[v]' -map '[a]' .\\_OUTPUT\\test.mp4 -y &"

# print(ffmpeg_exe+' -i '+listVideoPath[0])
# videoTime = os.system(ffmpeg_exe+' -i '+listVideoPath[0])
# videoTime = adb_shell(ffmpeg_exe+' -i '+listVideoPath[0])
# print(videoTime)


