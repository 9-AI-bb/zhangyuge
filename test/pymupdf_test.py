import fitz
pdf = fitz.Document('../pdf/3/世界科技全景百卷书（93）机器人技术.pdf')
print(pdf.pages(0))
