""" 
导出 config.ts 接口文件
"""

import os
import re
import json
from Utils import OUTPUT_ROOT

# 导出文件名
configFileName = 'config.ts'
# 隐射文件名
tmpFileName = "configtmp.json"
# 缓存文件目录
tmpFileRoot = os.path.normpath(os.path.join(os.path.dirname(__file__), '../tmp/'))
# 隐射文件路径
tmpFilePath = os.path.normpath(os.path.join(tmpFileRoot, tmpFileName))

class ConfigInterfaceStruct:
    """ 导出config.ts文件的信息 """

    # 表名
    def clientName(self):
        pass

    # 表名描述
    def clientNameDef(self):
        pass

    # 字段结构体
    def dataObj(self):
        pass

    # 导出路径
    def outputRoot(self):
        pass


def dealConfigTs(struct: ConfigInterfaceStruct) -> None:
    """ 导出 config.ts 文件 """
    if not struct:
        return

    clientName: str = struct.clientName
    dataObj: dict = struct.dataObj
    outputRoot: str = struct.outputRoot
    clientNameDef: str = struct.clientNameDef

    # 写入config.ts的内容
    tsStr = '/** '+clientNameDef+' */\n' 
    tsStr = tsStr + 'interface ' + clientName.replace('.json', '') + ' {'
    for idx in range(0, len(dataObj)):
        data: dict = dataObj[idx]
        if 'C' in data._cs or 'c' in data._cs:
            valType = data._type
            if data._type == 'array':
                valType = 'any[]'
            elif data._type == 'object':
                valType = 'any'
            tsStr = tsStr + '\n\t/** ' + data._def + ' */'
            tsStr = tsStr + '\n\treadonly ' + data._name + ': ' + valType + ';'
            # print(data._cs, data._type, data._name, data._def)
    tsStr = tsStr + '\n}'

    tmpObj = readTmpJson()
    tmpObj[clientName] = tsStr # 写入缓存json文件

    writeTmpJson(tmpObj)

    newtsStr: str = '/** 本文件为导表工具导出，不可手动修改 */\n\n'
    for key in sorted(tmpObj):
        newtsStr = newtsStr + tmpObj[key] + '\n\n'
    # print(newtsStr)  

    tsconfigDir = os.path.normpath(os.path.join(outputRoot + '/' + configFileName)) # 导出路径
    with open(tsconfigDir, 'w', encoding='utf-8') as writefile:
        writefile.write(newtsStr)
    # print('write ' + configFileName +' successful!!!')


def readTmpJson() -> dict:
    """ 读取一份本地缓存文件，所有的导出到config.ts的json文件，都映射一个key-vale，方便下回写入 """
    if not os.path.exists(tmpFileRoot):
        os.mkdir(tmpFileRoot)

    if not os.path.exists(tmpFilePath):
        return {}
    with open(tmpFilePath, 'r', encoding='utf-8') as readfile:
        jsonobj = json.load(readfile)
        return jsonobj


def writeTmpJson(obj: dict) -> None:
    """ 写入缓存文件 """
    with open(tmpFilePath, 'w', encoding='utf-8') as writefile:
        json.dump(obj, writefile, indent=2,ensure_ascii=False)


# TODO  测试，读取 config.ts 文件
def readCinfigTs() -> None:
    print('start to read config.ts file')
    fileroot = os.path.normpath(os.path.join(OUTPUT_ROOT, './config.ts'))
    # regularexp = re.compile(r'interface')
    with open(fileroot, 'r', encoding = 'utf-8') as readfile:
        filestr = readfile.read()
        # print(filestr)
        
        # # r'^interface [A-Za-z0-9]+ {[\n\s\S]+}[\n]+$'
        # obj = re.findall(r'interface [A-Za-z0-9]+ {$', filestr, re.M|re.I|re.DOTALL) 
        # obj = re.findall(r'[a-zA-z0-9]{0,}[\u4e00-\u9fa5]{0,}[a-zA-z0-9]{0,}', filestr)
        # print('match list: ', obj, len(obj))

        newfilestr = re.sub(r'/\*\*.{0,}\*/', '', filestr) # 清除所有的/***/注释  中文[\u4e00-\u9fa5]
        newfilestr = newfilestr.replace('\n', '').replace('\t','') # 清除所有的换行符和制表符
        newfilestr = newfilestr.replace('}interface','}\ninterface') # 每个interface一行
        print(newfilestr)
        # print(re.split(r'}', newfilestr), len(re.split(r'}', newfilestr))) # 以}切割
        # obj = re.findall(r'interface [A-Za-z0-9]+ {.{1,}}', newfilestr)
        # print(obj, len(obj))

# TODO
if __name__ == '__main__':
    # readCinfigTs()
    obj = readTmpJson()
    print(obj)

