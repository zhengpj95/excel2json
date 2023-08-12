
import tkinter
from Utils import Utils
from os import path

# 创建主窗口
root = tkinter.Tk()

root.title('导表工具')
root.geometry('800x500+200+200')
root.minsize(800, 500)
root.maxsize(1100, 600)

# 所有的xlsx文件
xlsxRoot = path.join(path.dirname(__file__), '../xlsx')
files = Utils.readFileList(xlsxRoot)

# 创建列表
listbox = tkinter.Listbox(root, font=("微软雅黑", 12), height=20)
listbox.pack(fill='both', padx=20)
for i,file in enumerate(files):
    listbox.insert(i, file)


# 按钮
onekeyBtn = tkinter.Button(root, text='导出所有', width=20, font=(None,15))
onekeyBtn.pack(side='right')

singleBtn = tkinter.Button(root, text='导出选中', width=20, font=(None,15))
singleBtn.pack(side='left')

# 显示窗口
root.mainloop()
