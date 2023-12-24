# zhangyuge
##一个简易的多进程批量文件处理python包（学习用）

只需要传入处理方法，待处理的文件路径，期望处理后得到的数据存储位置，和他们的后缀名，就可以以多进程的方式运行

##使用方法：

1.先自定义一个文件处理方法def file_process(file)，file类型是bytes，在其中编写转换过程，最后返回一个数据

2.from zhangyuge import processor_by_file，导入需要的方法函数

3.传入需要的参数：processor_by_file(func,src_path,src_suffix,dest_paath,dest_suffix,processor_num)

4.运行程序


##processor_by_file参数说明：

func：自定义函数

src_path：原文件路径

src_suffix：原文件后缀名

dest_paath：处理后文件存储路径

dest_suffix：处理后文件后缀

processor_num：进程数量（默认为2）

