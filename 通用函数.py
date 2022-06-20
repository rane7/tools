import os
import requests


def del_all_empty_folder(path):
    dir = []
    get_file_path(path, [], dir, True)
    dir=dir[::-1]
    for i in dir:
        if not os.listdir(i):
            os.rmdir(i)



def get_file_path(root_path, file_list, dir_list, all_level=False):
    # 获取该目录下所有的文件名称和目录名称
    dir_or_files = os.listdir(root_path)
    for dir_file in dir_or_files:
        # 获取目录或者文件的路径
        dir_file_path = os.path.join(root_path, dir_file)
        # 判断该路径为文件还是路径
        if os.path.isdir(dir_file_path):
            dir_list.append(dir_file_path)
            # 递归获取所有文件和目录的路径
            if all_level:
                get_file_path(dir_file_path, file_list, dir_list, True)
        else:
            file_list.append(dir_file_path)

def getProxy():
    content = requests.get("http://219.244.171.32:5010/get/").json()
    ip = content["proxy"]
    # proxy = {'http': 'http://' + ip}
    return "http://" + ip