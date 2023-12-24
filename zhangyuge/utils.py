import os
from multiprocessing import Pool
from functools import partial
import json


# 用来分配线程，执行自定义函数
def thread_func(home_path: str, src_path: str, dest_path: str, suffix: str, func, processor_num: int):
    # 线程读取文件到队列，需要将队列内数据大小限制到总内存的一半再除以进程数
    # file_queue = queue.Queue()
    # 数据读取线程
    # def read_file_to_queue():
    #     for file_or_dir in os.listdir(home_path):
    #         # 读取文件到队列
    #         file_full_path = os.path.join(home_path, file_or_dir)
    #         if os.path.isfile(file_full_path):
    #             # todo:判断如果加入此文件后队列占用内存是否超出限制
    #             file_queue.put({file_full_path: open(file_full_path, 'rb')})
    #
    # # 数据处理线程
    # def process_file():
    #     while not file_queue.empty():
    #         # 获取文件数据
    #         file = file_queue.get()
    #         file_full_path = list(file.keys())[0]
    #         file_bytes = file.get(file_full_path)
    #         # 交给自定义函数处理
    #         result = func(file_bytes)
    #         # 保存
    #         save_result(result, src_path, file_full_path, dest_path, suffix)
    # def save_result(result: bytes, src_path: str, file_full_path: str, save_path: str, end_suffix: str):
    #     filename = os.path.basename(file_full_path)  # 文件原名
    #     base, ext = os.path.splitext(filename)  # 文件名和后缀
    #     if end_suffix == '.txt':
    #         with open(os.path.join(save_path, file_full_path[len(src_path):-len(ext)]) + end_suffix,
    #                   'w', encoding='utf-8') as result_file:
    #             result_file.write(result)
    #     elif end_suffix == '.json':
    #         with open(os.path.join(save_path, file_full_path[len(src_path):-len(ext)]) + end_suffix,
    #                   'w', encoding='utf-8') as result_file:
    #             json.dump(result, result_file)

    print('启动了一个进程，处理' + home_path)
    for file_or_dir in os.listdir(home_path):
        file_full_path = os.path.join(home_path, file_or_dir)
        if os.path.isfile(file_full_path):
            with open(file_full_path, 'rb') as file:
                file_bytes = file.read()
                result = func(file_bytes)
                save_result(result, src_path, file_full_path, dest_path, suffix)

    # read_thread = threading.Thread(target=read_file_to_queue())
    # process_thread = threading.Thread(target=process_file())


# 用来分配进程
def processor(func, src_path: str, dest_path: str, suffix: str = '.txt', processor_num: int = 2) -> None:
    print('进入多进程启动函数')
    home_path = []
    print('开始检索并创建文件夹')
    for home, _, _ in os.walk(src_path):
        home_path.append(home)
        target_path = os.path.join(dest_path, home[len(src_path):])
        if not os.path.exists(target_path):
            os.makedirs(target_path)

    partial_thread_func = partial(thread_func, src_path=src_path, dest_path=dest_path, suffix=suffix, func=func,
                                  processor_num=processor_num)
    print('准备启动多进程')
    with Pool(processes=processor_num) as pool:
        pool.map(partial_thread_func, home_path)


def processor_by_dir(func, src_path: str, dest_path: str, suffix: str = '.txt', processor_num: int = 2) -> None:
    # 以文件夹为单位分配进程
    processor(func, src_path, dest_path, suffix, processor_num)


def save_result(result: bytes, src_path: str, file_full_path: str, save_path: str, end_suffix: str):
    filename = os.path.basename(file_full_path)  # 文件原名
    base, ext = os.path.splitext(filename)  # 文件名和后缀
    # 创建存储所用的文件夹
    target_path = os.path.join(save_path, file_full_path[len(src_path):-len(filename)])
    print('存储在'+target_path)
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


# home_path: str, src_path: str, dest_path: str, suffix: str, func, processor_num: int
def process_func_by_file(file_full_path: str, src_path: str, dest_path: str, suffix: str, func, processor_num: int):
    # 打开文件交给函数处理
    with open(file_full_path, 'rb') as file:
        file_bytes = file.read()
        result = func(file_bytes)
    save_result(result, src_path, file_full_path, dest_path, suffix)
    pass


def processor_by_file(func, src_path: str,src_suffix:str, dest_path: str, dest_suffix: str = '.txt', processor_num: int = 2) -> None:
    # 以文件为单位分配进程
    with Pool(processes=processor_num) as pool:
        partial_process_func_by_file = partial(process_func_by_file, src_path=src_path, dest_path=dest_path,
                                               suffix=dest_suffix, func=func,
                                               processor_num=processor_num)
        # for home, _, files in os.walk(src_path):
        #     print('进入路径' + home)
        #     target_path = os.path.join(dest_path, home[len(src_path):])
        #     if not os.path.exists(target_path):
        #         os.makedirs(target_path)
        #     for file in files:
        #         file_full_path = os.path.join(home, file)
        #         pool.map(partial_process_func_by_file, [file_full_path])

        # 使用迭代器省内存
        pool.map(partial_process_func_by_file, iter_files(src_path,src_suffix))


def iter_files(src_path,src_suffix):
    """
    遍历目录及其所有子目录中的文件的迭代器函数
    :param src_path: 目录路径
    :return: 文件路径生成器
    """
    for home, _, files in os.walk(src_path):
        print('开始处理：'+home)
        for file in files:
            if not file.endswith(src_suffix):
                continue
            file_path = os.path.join(home, file)
            yield file_path
