import os
import time
from multiprocessing import Pool
import fitz
import numpy as np
from cnocr import CnOcr
from functools import partial


def get_path_list(src_path, dest_path):
    home_list = []
    for home, _, _ in os.walk(src_path):
        home_list.append(home)
        target_path = os.path.join(dest_path, home[len(src_path):])
        if not os.path.exists(target_path):
            print(target_path)
            os.makedirs(target_path)
    return home_list


def process_book(home_path, src_path, dest_path):
    print('开始处理' + home_path)
    ocr = CnOcr()
    for file_or_dir in os.listdir(home_path):
        file_full_path = os.path.join(home_path, file_or_dir)
        if os.path.isfile(file_full_path):
            content = ''
            # pymupdf打开文件
            pdf = fitz.Document(file_full_path)
            print(file_full_path + '成功打开')
            # 转为像素bytes
            pdf_all_page_pix_arr = []
            for page in pdf:
                pix = page.get_pixmap()
                pix_arr = np.frombuffer(pix.samples, dtype='uint8').reshape(pix.h, pix.w, pix.n)
                ocr_result = ocr.ocr(pix_arr)
                for line in ocr_result:
                    content += line['text'] + '\n'
            with open(os.path.join(dest_path, home_path[len(src_path):]) + file_or_dir[:-4] + '.txt', 'w',
                      encoding='utf-8') as file:
                file.write(content)


def main(src_path, dest_path):
    path_list = get_path_list(src_path, dest_path)
    print(path_list)
    partial_process_book = partial(process_book, src_path=src_path, dest_path=dest_path)
    with Pool(2) as pool:
        pool.map(partial_process_book, path_list)


if __name__ == '__main__':
    start_time = time.time()
    SRC_PATH = 'D:\Desktop\ice\code\python\zhangyuge\pdf'  # 替换为你的目录路径
    DEST_PATH = 'D:\Desktop\ice\code\python\zhangyuge\\txt'
    main(SRC_PATH, DEST_PATH)
    print(time.time() - start_time)
