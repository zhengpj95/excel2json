""" 
导出 config.ts 接口文件
"""
import json
import os
import re

from Utils import OUTPUT_ROOT

# 导出文件名
configFileName = 'config.ts'
configNameFileName = "config-name.ts"
configNameFilePath = os.path.normpath(os.path.join(os.path.dirname(__file__), '../xlsx/', configNameFileName))
# 隐射文件名
tmpFileName = "00config_ts_tmp.txt"
# 缓存文件目录
tmpFileRoot = os.path.normpath(os.path.join(os.path.dirname(__file__), '../xlsx/'))
# 隐射文件路径
tmpFilePath = os.path.normpath(os.path.join(tmpFileRoot, tmpFileName))


class ConfigInterfaceStruct:
    """ 导出config.ts文件的信息 """

    def __init__(self, client_name: str, client_name_def: str, data_obj: dict, output_root: str):
        self.client_name = client_name  # 表名
        self.client_name_def = client_name_def  # 表名描述
        self.data_obj = data_obj  # 字段结构体
        self.output_root = output_root  # 导出路径


def deal_config_ts(struct: ConfigInterfaceStruct) -> None:
    """ 导出 config.ts 文件 """
    if not struct:
        return

    clientName: str = struct.client_name
    dataObj: dict = struct.data_obj
    outputRoot: str = struct.output_root
    clientNameDef: str = struct.client_name_def
    print("  ", clientName, outputRoot, clientNameDef)

    # 写入config.ts的内容
    tsStr = '/** ' + clientNameDef + ' */\n'
    tsStr = tsStr + 'export interface ' + clientName.replace('.json', '') + ' {'
    for idx in range(0, len(dataObj)):
        data = dataObj[idx]  # DataStruct
        if 'C' in data.cs or 'c' in data.cs:
            valType = data.type
            if data.type == 'array':
                valType = 'any[]'
            elif data.type == "number[]":
                valType = 'number[]'
            elif data.type == "string[]":
                valType = 'string[]'
            elif data.type == 'number[][]':
                valType = 'number[][]'
            elif data.type == 'string[][]':
                valType = 'string[][]'
            elif data.type == 'object':
                valType = 'Record<string | number, any>'
            tsStr = tsStr + '\n  /** ' + data.definition + ' */'
            tsStr = tsStr + '\n  readonly ' + data.name + ': ' + valType + ';'
            # print(data.cs, data.type, data.name, data.definition)
    tsStr = tsStr + '\n}'

    tmpObj = read_tmp_json()
    tmpObj[clientName] = tsStr  # 写入缓存json文件

    write_tmp_json(tmpObj)

    newtsStr: str = '/** 本文件为导表工具导出，不可手动修改 */\n'  # config.ts
    configNameTsStr: str = '/** 本文件为导表工具导出，不可手动修改 */\n\nexport const enum ConfigName {\n'  # config-name.ts
    for key in sorted(tmpObj):
        newtsStr = newtsStr + '\n' + tmpObj[key] + '\n'
        tsKey = key.replace(".json", "")
        configNameTsStr = configNameTsStr + "  " + tsKey + ' = "' + tsKey + '",\n'

    configNameTsStr = configNameTsStr + "}\n"

    tsconfigDir = os.path.normpath(os.path.join(outputRoot + '/' + configFileName))  # 导出路径
    with open(tsconfigDir, 'w', encoding='utf-8', newline='\n') as writefile:
        writefile.write(newtsStr)
    # print('write ' + configFileName +' successful!!!')
    tsconfigNameDir = os.path.normpath(os.path.join(outputRoot + "/" + configNameFileName))
    with open(tsconfigNameDir, 'w', encoding='utf-8', newline='\n') as writefile:
        writefile.write(configNameTsStr)


def read_tmp_json() -> dict:
    """ 读取一份本地缓存文件，所有的导出到config.ts的json文件，都映射一个key-vale，方便下回写入 """
    if not os.path.exists(tmpFileRoot):
        os.mkdir(tmpFileRoot)

    if not os.path.exists(tmpFilePath):
        return {}
    with open(tmpFilePath, 'r', encoding='utf-8') as readfile:
        jsonobj = json.load(readfile)
        return jsonobj


def write_tmp_json(obj_dict: dict) -> None:
    """ 写入缓存文件 """
    with open(tmpFilePath, 'w', encoding='utf-8', newline='\n') as writefile:
        json.dump(obj_dict, writefile, indent=2, ensure_ascii=False)


# TODO  测试，读取 config.ts 文件
def read_config_ts() -> None:
    print('start to read config.ts file')
    file_root = os.path.normpath(os.path.join(OUTPUT_ROOT, './config.ts'))
    # regularexp = re.compile(r'interface')
    with open(file_root, 'r', encoding='utf-8') as readfile:
        file_str = readfile.read()
        # print(filestr)

        # # r'^interface [A-Za-z0-9]+ {[\n\s\S]+}[\n]+$'
        # obj = re.findall(r'interface [A-Za-z0-9]+ {$', filestr, re.M|re.I|re.DOTALL)
        # obj = re.findall(r'[a-zA-z0-9]{0,}[\u4e00-\u9fa5]{0,}[a-zA-z0-9]{0,}', filestr)
        # print('match list: ', obj, len(obj))

        newfilestr = re.sub(r'/\*\*.{0,}\*/', '', file_str)  # 清除所有的/***/注释  中文[\u4e00-\u9fa5]
        newfilestr = newfilestr.replace('\n', '').replace('\t', '')  # 清除所有的换行符和制表符
        newfilestr = newfilestr.replace('}interface', '}\ninterface')  # 每个interface一行
        print(newfilestr)
        # print(re.split(r'}', newfilestr), len(re.split(r'}', newfilestr))) # 以}切割
        # obj = re.findall(r'interface [A-Za-z0-9]+ {.{1,}}', newfilestr)
        # print(obj, len(obj))


# TODO
if __name__ == '__main__':
    # readCinfigTs()
    obj = read_tmp_json()
    print(obj)
