""" 
导出 config.ts 接口文件
"""

import os

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
            tsStr = tsStr + '\n\treadonly ' + data._name + ': ' + valType
            # print(data._cs, data._type, data._name)
    tsStr = tsStr + '\n}'
    # print(tsStr)  
    # TODO (还需继续处理，新增的，字段有变化的)
    tsconfigDir = os.path.normpath(
        os.path.join(outputRoot + '/' + tsconfigfilename))
    with open(tsconfigDir, 'w', encoding='utf-8') as writefile:
        writefile.write(tsStr)
    print('export ' + tsconfigfilename +' successful!!!')
