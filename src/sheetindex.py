""" 
json到excel的关联
"""

from os import path

from Utils import XLSX_ROOT

# 文件名
fileName = "00sheet_index.txt"
# 文件路径
filePath = path.normpath(path.join(XLSX_ROOT, fileName))


def deal_sheet_index_file(xlsx_title: str, sheet_title: str, json_name: str) -> None:
    """ 写入 00sheet_index.txt，建立xlsx和其下sheet的映射关系 """
    # print('11111 dealSheetIndexFile---', xlsx_title, sheet_title, json_name, filePath)
    flagStr = xlsx_title + ' = ' + sheet_title + '[' + json_name + ']'
    if not path.exists(filePath) or path.getsize(filePath) == 0:
        with open(filePath, 'w', encoding='utf-8', newline='\n') as writefile:
            writefile.write(flagStr)
        return

    obj = read_sheet_index_file()
    if not obj.get(xlsx_title):
        obj[xlsx_title] = {}
        obj[xlsx_title][sheet_title] = sheet_title + '[' + json_name + ']'
    else:
        xlsx_obj: dict = obj.get(xlsx_title)
        if not xlsx_obj.get(sheet_title):
            xlsx_obj[sheet_title] = sheet_title + "[" + json_name + "]"

    # print(111, obj)
    rewriteStr = ''
    for key in sorted(obj.keys()):  # xlsx名字遍历
        singleXlsxStr = key + ' = '
        subObj: dict = obj.get(key)  # sheet字典
        subObjKeys = subObj.keys()  # sheet名字数组
        for i, sheet_key in enumerate(sorted(subObjKeys)):  # sheet名字遍历，i就是序号，从0开始
            # print(i, sheet_key)
            if len(subObjKeys) - 1 == i:
                singleXlsxStr += subObj.get(sheet_key)
            else:
                singleXlsxStr += subObj.get(sheet_key) + ' | '
        if rewriteStr == '':
            rewriteStr = singleXlsxStr
        else:
            rewriteStr = rewriteStr + '\n' + singleXlsxStr
    # print("rewriteStr: ", rewriteStr)
    with open(filePath, 'w', encoding='utf-8', newline='\n') as writefile:
        writefile.write(rewriteStr + "\n")


def read_sheet_index_file() -> dict:
    """ xlsx字典 读取 00sheet_index.txt，缓存为dict """
    with open(filePath, 'r', encoding='utf-8') as readfile:
        lineList = readfile.readlines()

    obj: dict = {}
    for line in lineList:
        ary: list = line.split(' = ')  # 拆分，ary[0]就是xlsx名称，ary[1]就是其下所有的sheet拼接的字符串
        xlsxName = ary[0]  # xlsx名称
        obj[xlsxName] = {}
        ary1 = ary[1].replace('\n', '').split(' | ')  # 拆分，每个元素就是一个sheet
        for item in ary1:
            if item == '' or item is None:
                continue
            sheetName = item.split('[')[0]  # sheet名称
            obj[xlsxName][sheetName] = item
    # print(11111, obj)
    return obj
