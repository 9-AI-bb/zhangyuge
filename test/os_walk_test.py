import os

for home, dirs, files in os.walk('D:\Desktop\ice\code\python\zhangyuge\pdf'):
    for file in files:
        print(os.path.join(home, file))
