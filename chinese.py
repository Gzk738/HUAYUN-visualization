#-*-coding:utf-8-*-
#文件名: zh.py
def set_zh():
    from pylab import mpl
    mpl.rcParams['font.sans-serif'] = ['默认字体的名称'] # 指定默认字体
    mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

#Mac OSX系统中，字体的名称在fontbook这个APP里找