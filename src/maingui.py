""" 
可视化操作界面
"""

import tkinter
from Utils import Utils
from os import path
from excel2json import Excel2Json
from Utils import XLSX_ROOT, OUTPUT_ROOT

# 创建主窗口
win = tkinter.Tk()

win.title('导表工具')
win.geometry('800x500+200+200')
win.minsize(800, 500)
win.maxsize(1100, 600)

# 所有的xlsx文件
xlsxRoot = XLSX_ROOT
files = Utils.readFileList(xlsxRoot)
# 导出路径
outputRoot = OUTPUT_ROOT

# 创建列表
listbox = tkinter.Listbox(win, font=("微软雅黑", 12), height=20)
listbox.pack(fill='both', padx=20)
for i,file in enumerate(files):
    listbox.insert(i, file)


# 导出所有
def exportAllFunc():
    print('print all')
    for file in files:
        filePath = path.normpath(path.join(xlsxRoot, file))
        excel2Json = Excel2Json(filePath, outputRoot)
        excel2Json.readFile()

onekeyBtn = tkinter.Button(win, text='导出所有', width=20, font=(None,15), command=exportAllFunc)
onekeyBtn.pack(side='right')

# 选中导出
def exportSelectFunc():
    selectItem = listbox.curselection()
    if not selectItem:
        print('select error, please select one item!!!')
        return
    txt = listbox.get(selectItem) #选中的内容
    selectItemPath = path.normpath(path.join(xlsxRoot, txt))
    print('print selected: ', selectItemPath)
    excel2Json = Excel2Json(selectItemPath, outputRoot)
    excel2Json.readFile()

singleBtn = tkinter.Button(win, text='导出选中', width=20, font=(None,15), command=exportSelectFunc)
singleBtn.pack(side='left')

# 显示窗口
win.mainloop()
