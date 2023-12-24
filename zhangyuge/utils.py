import os
from multiprocessing import Pool
from functools import partial
import json


def save_result(result: bytes, src_path: str, file_full_path: str, save_path: str, end_suffix: str):
    filename = os.path.basename(file_full_path)  # 文件原名
    base, ext = os.path.splitext(filename)  # 文件名和后缀
    # 创建存储所用的文件夹
    target_path = os.path.join(save_path, file_full_path[len(src_path):-len(filename)])
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    if end_suffix == '.txt':
        with open(os.path.join(save_path, file_full_path[len(src_path):-len(ext)]) + end_suffix,
                  'w', encoding='utf-8') as result_file:
            result_file.write(result)
    elif end_suffix == '.json':
        with open(os.path.join(save_path, file_full_path[len(src_path):-len(ext)]) + end_suffix,
                  'w', encoding='utf-8') as result_file:
            json.dump(result, result_file)
    print(file_full_path + '处理完成')


# home_path: str, src_path: str, dest_path: str, suffix: str, func, processor_num: int
def process_func_by_file(file_full_path: str,
                         src_path: str,
                         dest_path: str,
                         suffix: str,
                         func,
                         processor_num: int):
    # 打开文件交给函数处理
    with open(file_full_path, 'rb') as file:
        file_bytes = file.read()
        result = func(file_bytes)
    save_result(result, src_path, file_full_path, dest_path, suffix)
    pass


def processor_by_file(func,
                      src_path: str,
                      src_suffix: str,
                      dest_path: str,
                      dest_suffix: str = '.txt',
                      processor_num: int = 2) -> None:
    # 以文件为单位分配进程
    with Pool(processes=processor_num) as pool:
        partial_process_func_by_file = partial(process_func_by_file, src_path=src_path, dest_path=dest_path,
                                               suffix=dest_suffix, func=func,
                                               processor_num=processor_num)
        # 使用生成迭代器省内存
        pool.map(partial_process_func_by_file, iter_files(src_path, src_suffix))


def iter_files(src_path, src_suffix):
    """
    遍历目录及其所有子目录中的文件的迭代器函数
    :param src_path: 目录路径
    :param src_suffix: 原文件后缀
    :return: 文件路径生成器
    """
    for home, _, files in os.walk(src_path):
        for file in files:
            if not file.endswith(src_suffix):
                continue
            file_path = os.path.join(home, file)
            yield file_path
