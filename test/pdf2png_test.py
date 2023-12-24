import fitz

pdf = fitz.Document('D:\Desktop\ice\code\python\zhangyuge\pdf\世界科技全景百卷书（93）机器人技术.pdf')

# page = pdf.pages(11)
page = pdf.load_page(0)
pix = page.get_pixmap()
print(pix)


