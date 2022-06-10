import datetime
import os
import ffmpeg

strVideoPath = '.\\RAW\\'
str_new_path = '.\\_OUTPUT\\'
list_old_new_path = {}
sre_result = "./_OUTPUT/_result.txt"

# def adb_shell(cmd):
#     result = os.popen(cmd).readlines()
#     print(result)
#     return result



def get_ffmpeg_format_time(second):
    m, s = divmod(int(second), 60)
    h, m = divmod(m, 60)
    ft_end = '{:.2f}'.format(round(second%1, 2))
    # print(h, m, s, ft_end)
    str_time = str(h)+'-'+str(m)+'-'+str(s)
    time_format = datetime.datetime.strptime(str_time, '%H-%M-%S')
    # print(time_format)
    strTimeLen = str(time_format)[11:]+str(ft_end)[1:]
    return strTimeLen

def do_system_cmd(str_cmd_crop, str_cmd_splicing):
    os.system('echo off')
    os.system(str_cmd_crop)
    os.system(str_cmd_splicing)


if __name__ == '__main__':

    videoList = os.listdir(strVideoPath)
    for file_name in videoList:
        if file_name[-3:] == 'mp4' or file_name[-3:] == 'MP4':
            list_old_new_path[str(strVideoPath+file_name)] = str(str_new_path+file_name)
    # print(list_old_new_path)

    time_begin = float(ffmpeg.probe(str('./ADD/begin.mp4'))['format']['duration'])
    time_end = float(ffmpeg.probe(str('./ADD/end.mp4'))['format']['duration'])
    # print(time_begin, time_end)
    str_time_begin = get_ffmpeg_format_time(time_begin)
    # print(str_time_begin)

    if os.path.isfile(sre_result):
        os.remove(sre_result)

for videoname in list_old_new_path.keys():
        timeVideo = float(ffmpeg.probe(videoname)['format']['duration'])
        # print(timeVideo)
        timeVideo = timeVideo - time_end # -time_begin;
        # print(timeVideo)
        str_time_video = get_ffmpeg_format_time(timeVideo)
        # print(str_time_video)
        if os.path.isfile("./TMP.mp4"):
            os.remove('./TMP.mp4')
        str_cmd_crop = "ffmpeg.exe -ss 00:00:00.00  -i "+videoname+\
            " -vcodec copy -acodec copy -t "+str_time_video+" TMP.mp4 -y"
        # print(str_cmd_crop)
        os.system(str_cmd_crop)

        str_cmd_MP42TS = "ffmpeg.exe -i TMP.mp4 -c:v copy TMP.ts -y"
        # print(str_cmd_MP42TS)
        os.system(str_cmd_MP42TS)

        str_cmd_splicing = "ffmpeg.exe -i \"concat:TMP.ts|.\ADD\end.ts\" -c copy output.ts -y"
        # print(str_cmd_splicing)
        os.system(str_cmd_splicing)

        str_cmd_TS2MP4 = "ffmpeg.exe -y -i output.ts -c:v copy " + list_old_new_path[videoname]
        # print(str_cmd_TS2MP4)
        os.system(str_cmd_TS2MP4)

        # do_system_cmd(str_cmd_crop,str_cmd_splicing)

        result = open(sre_result, 'a+')
        result.writelines(list_old_new_path[videoname]+'\t Completed\n')
        result.close()

'''
for videoname in list_old_new_path.keys():
        timeVideo = float(ffmpeg.probe(videoname)['format']['duration'])
        # print(timeVideo)
        timeVideo = timeVideo - time_end -time_begin;
        # print(timeVideo)
        str_time_video = get_ffmpeg_format_time(timeVideo)
        print(str_time_video)
        if os.path.isfile("./TMP.mp4"):
            os.remove('./TMP.mp4')
        str_cmd_crop = "ffmpeg.exe -ss "+str_time_begin+" -i "+videoname+\
            " -vcodec copy -acodec copy -t "+str_time_video+" ./TMP.mp4 -y"
        print(str_cmd_crop)

        str_cmd_splicing = "ffmpeg.exe -y -i .\\ADD\\begin.mp4 -i .\\TMP.mp4 -i .\\ADD\\end.mp4 -filter_complex \"[0:0] [0:1] [1:0] [1:1] [2:0] [2:1] concat=n=3:v=1:a=1 [v] [a]\" -map \"[v]\" -map \"[a]\" "+list_old_new_path[videoname]
        print(str_cmd_splicing)

        do_system_cmd(str_cmd_crop,str_cmd_splicing)

        result = open(sre_result, 'a+')
        result.writelines(list_old_new_path[videoname]+'\t Completed\n')
        result.close()
'''


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



