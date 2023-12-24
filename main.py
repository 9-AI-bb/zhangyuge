import time
import zhangyuge
import fitz
from cnocr import CnOcr
import numpy as np
import pdfplumber
import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


# 使用cnocr的pdf转txt，可以处理绝大部分场景，但是速度慢，建议千万不要开多进程
def process_pdf2txt_ocr(file: bytes):
    ocr = CnOcr()
    content = ''
    # 只需要关心文件从什么变成什么
    # 打开pdf
    pdf = fitz.Document(stream=file, filetype='pdf')
    # 获取pdf页，将page内的像素数据直接转为txt
    for page in pdf:
        pix = page.get_pixmap()
        pix_arr = np.frombuffer(pix.samples, dtype='uint8').reshape(pix.h, pix.w, pix.n)
        ocr_result = ocr.ocr(pix_arr)
        for line in ocr_result:
            content += line['text'] + '\n'
    return content


def pdf2txt_ocr_rp_separate(file: bytes):
    ocr = CnOcr()
    content = ''
    page_list = []
    pdf = fitz.Document(stream=file, filetype='pdf')
    for page in pdf:
        pix = page.get_pixmap()
        reshape_ratio = int(pix.h / 1000)
        pix_arr = np.frombuffer(pix.samples, dtype='uint8').reshape(int(pix.h / reshape_ratio),
                                                                    int(pix.w / reshape_ratio),
                                                                    pix.n)
        page_list.append(pix_arr)
    for page in page_list:
        ocr_result = ocr.ocr(page, 2, box_score_thresh=0.7)
        for line in ocr_result:
            content += line['text'] + '\n'
    return content


# 使用pymupdf提取pdf文字，速度极快
def process_pdf2txt_pymupdf(file: bytes):
    content = ''
    pdf = fitz.Document(stream=file, filetype='pdf')
    time.sleep(2)
    for page in pdf:
        content += page.get_textpage().extractText() + '\n'
    return content


def process_pdf2txt_pdfplumber(file: bytes):
    content = ''
    pdf = pdfplumber.open(io.BytesIO(file))
    for page in pdf.pages:
        text = page.extract_text()
        content += text + '\n'
    return content


def process_pdf2txt_pdfminer(file: bytes):
    resource_manager = PDFResourceManager()
    output = io.StringIO()
    converter = TextConverter(resource_manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(resource_manager, converter)
    for page in PDFPage.get_pages(io.BytesIO(file)):
        interpreter.process_page(page)
    content = output.getvalue()
    return content


if __name__ == '__main__':
    start_time = time.time()
    print('开始执行')
    zhangyuge.processor_by_file(process_pdf2txt_pdfminer,
                                src_path='D:\Desktop\ice\code\python\zhangyuge\pdf\\',
                                src_suffix='.pdf',
                                dest_path='D:\Desktop\ice\code\python\zhangyuge\\txt\\',
                                dest_suffix='.txt',
                                processor_num=20)
    print(time.time() - start_time)
