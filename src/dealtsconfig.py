""" 
导出 config.ts 接口文件
"""

import os
import re

# 导出文件
tsconfigfilename = 'config.ts'


class TsconfigStruct:
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


def dealConfigTs(struct: TsconfigStruct) -> None:
    """ 导出 config.ts 文件 """
    clientName: str = struct.clientName
    dataObj: dict = struct.dataObj
    outputRoot: str = struct.outputRoot
    clientNameDef: str = struct.clientNameDef

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
            tsStr = tsStr + '\n\treadonly ' + data._name + ': ' + valType
            print(data._cs, data._type, data._name, data._def)
    tsStr = tsStr + '\n}'
    # print(tsStr)  
    # TODO (还需继续处理，新增的，字段有变化的)
    tsconfigDir = os.path.normpath(os.path.join(outputRoot + '/' + tsconfigfilename))
    with open(tsconfigDir, 'w', encoding='utf-8') as writefile:
        writefile.write(tsStr)
    print('export ' + tsconfigfilename +' successful!!!')

# TODO  测试，读取 config.ts 文件
def readCinfigTs()-> None:
    print('start to read config.ts file')
    fileroot = os.path.normpath(os.path.join(os.path.dirname(__file__), '../output/config.ts'))
    # regularexp = re.compile(r'interface')
    with open(fileroot, 'r', encoding = 'utf-8') as readfile:
        filestr = readfile.read().replace('\t','').replace('\n','').replace('*/', '*/\n').replace('/**','\n/**') # 每个interface单独一行
        print(filestr)
        # r'^interface [A-Za-z0-9]+ {[\n\s\S]+}[\n]+$'
        obj = re.findall(r'interface [A-Za-z0-9]+ \{.*\}$', filestr, re.M|re.I|re.DOTALL) 
        print('match list: ', obj, len(obj))

# TODO
if __name__ == '__main__':
    readCinfigTs()

