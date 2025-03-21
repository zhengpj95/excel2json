""" 
可视化操作界面
"""

import tkinter
from os import path

from Utils import Utils
from Utils import XLSX_ROOT, OUTPUT_ROOT
from excel2json import Excel2Json

# 创建主窗口
win = tkinter.Tk()

win.title('导表工具')
win.geometry('800x500+200+200')
win.minsize(800, 500)
win.maxsize(1100, 600)

# 所有的xlsx文件
xlsxRoot = XLSX_ROOT
files = Utils.read_file_list(xlsxRoot)
# 导出路径
outputRoot = OUTPUT_ROOT

# 创建列表
listbox = tkinter.Listbox(win, font=("微软雅黑", 12), height=20)
listbox.pack(fill='both', padx=20)
for i, file in enumerate(files):
    listbox.insert(i, file)
listbox.selection_set(0)
listbox.activate(0)  # 让第一项成为焦点（可选）
listbox.focus_set()  # 让 Listbox 获取焦点（可选）


# 导出所有
def export_all_func():
    print('** print selected: All')
    for file in files:
        filePath = path.normpath(path.join(xlsxRoot, file))
        excel2Json = Excel2Json(filePath, outputRoot)
        excel2Json.read_file()


onekeyBtn = tkinter.Button(win, text='导出所有', width=20, font=(None, 15), command=export_all_func)
onekeyBtn.pack(side='right')


# 选中导出
def export_select_func():
    selectItem = listbox.curselection()
    if not selectItem:
        print('** select error, please select one item!!!')
        return
    txt = listbox.get(selectItem)  # 选中的内容
    selectItemPath = path.normpath(path.join(xlsxRoot, txt))
    print('** print selected: ', selectItemPath)
    excel2Json = Excel2Json(selectItemPath, outputRoot)
    excel2Json.read_file()


singleBtn = tkinter.Button(win, text='导出选中', width=20, font=(None, 15), command=export_select_func)
singleBtn.pack(side='left')

# 显示窗口
win.mainloop()
