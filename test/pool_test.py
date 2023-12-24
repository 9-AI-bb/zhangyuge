import os
import multiprocessing
import time
from functools import partial


# 定义处理函数，用于计算文件长度
def process_file(file_path):
    time.sleep(0.1)
    count = 0
    for file in os.listdir(file_path):
        if os.path.isfile(file):
            count += 1
    return count

    # 主程序


def main(directory):
    directories=[]
    # 获取目录下的所有子目录，形成目录列表
    for home,_,_ in os.walk(directory):
        directories.append(home)
    # 创建进程池
    with multiprocessing.Pool(processes=20) as pool:
        # 对目录中的文件进行处理，并返回文件内容（这里返回文件长度）
        results = pool.map(process_file, [d for d in directories])

    return results


# 测试主程序
if __name__ == "__main__":
    start_time = time.time()
    directory_path = "D:\Desktop\ice"  # 替换为你的目录路径
    results = main(directory_path)
    print(results)
    print(time.time() - start_time)
