""" 
json到excel的关联
"""

from os import path
from Utils import XLSX_ROOT

# 文件名
fileName = "00sheet_index.txt"
# 文件路径
filePath = path.normpath(path.join(XLSX_ROOT, fileName))

def dealSheetIndexFile(xlsxTitle: str, sheetTitle: str, jsonName: str) -> None:
    """ 写入 00sheet_index.txt，建立xlsx和其下sheet的映射关系 """
    # print('dealSheetIndexFile---', xlsxTitle, sheetTitle,  jsonName, filePath)
    flagStr = xlsxTitle + ' = ' + sheetTitle + '[' + jsonName + ']'
    if not path.exists(filePath) or path.getsize(filePath) == 0:
        with open(filePath, 'w', encoding='utf-8') as writefile:
            writefile.write(flagStr)
        return
    
    obj = readSheetIndexFile()
    if not obj.get(xlsxTitle):
        obj[xlsxTitle] = {}
        obj[xlsxTitle][sheetTitle] = sheetTitle + '[' + jsonName + ']'

    # print(111, obj)
    rewriteStr = ''
    for key in sorted(obj.keys()):  # xlsx名字遍历
        singleXlsxStr = key + ' = '
        subObj: dict = obj.get(key) # sheet字典
        subObjKeys = subObj.keys()  # sheet名字数组
        for i,sheetkey in enumerate(sorted(subObjKeys)): # sheet名字遍历，i就是序号，从0开始
            # print(i, sheetkey)
            if len(subObjKeys) - 1 == i: 
                singleXlsxStr += subObj.get(sheetkey)
            else :
                singleXlsxStr += subObj.get(sheetkey) + ' | '
        if rewriteStr == '':
            rewriteStr = singleXlsxStr
        else:
            rewriteStr = rewriteStr + '\n' + singleXlsxStr
    # print(rewriteStr)
    with open(filePath, 'w', encoding='utf-8') as writefile:
        writefile.write(rewriteStr)


def readSheetIndexFile() -> dict:
    """ xlsx字典 读取 00sheet_index.txt，缓存为dict """
    lineList: list = []
    with open(filePath, 'r', encoding='utf-8') as readfile:
        lineList = readfile.readlines()

    obj: dict = {}
    for line in lineList:
        ary: list = line.split(' = ') # 拆分，ary[0]就是xlsx名称，ary[1]就是其下所有的sheet拼接的字符串
        xlsxName = ary[0] # xlsx名称
        obj[xlsxName] = {}
        ary1 = ary[1].replace('\n', '').split(' | ') # 拆分，每个元素就是一个sheet
        for item in ary1:
            if item == '' or item == None:
                continue
            sheetName = item.split('[')[0] # sheet名称
            obj[xlsxName][sheetName] = item
    # print(obj)
    return obj
