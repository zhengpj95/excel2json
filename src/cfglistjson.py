""" 
导出 cfglist.json 文件
"""

import json
import os

# 导出文件名
fileName = 'cfglist.json'


def deal_cfglist_json(client_name: str, output_root: str) -> None:
    """ 导出cfglist.json 文件 """

    cfglistjson_dir = os.path.normpath(os.path.join(output_root + "/" + fileName))  # 导出路径

    if not os.path.exists(cfglistjson_dir) or os.path.getsize(cfglistjson_dir) == 0:
        # 第一次写入cfglist.json文件，或者文件为空的。w写入方式
        with open(cfglistjson_dir, 'w', encoding='utf-8') as outfile:
            ary = [client_name]  # json文件名数组
            json.dump(ary, outfile, indent=2, ensure_ascii=False)
    else:
        # cfglist.json文件存在
        newJsonAry = []
        isEmpty = os.path.getsize(cfglistjson_dir) == 0  # 判断文件大小，为0表示为空
        if isEmpty is True:
            print('cfglist.json文件是空的，有问题。请删除cfglist.json文件，重新导出')
            return
        with open(cfglistjson_dir, "r") as cfglistjson:
            # firstChar = cfglistjson.read(1) # 读取第一位字符判断，不存在就表示空文件，读取后记得要处理seek(0)
            # if not firstChar:
            #     print('cfglist.json文件是空的，有问题。请删除cfglist.json文件，重新导出')
            #     return
            # cfglistjson.seek(0) # 重置到文件头

            jsonAry: list = json.load(cfglistjson)  # 这里若是文件空的，读入就会有问题 待处理
            if client_name not in jsonAry:
                jsonAry.append(client_name)  # 导出的json未存在，则加入
                jsonAry.sort()  # 排序
                newJsonAry = jsonAry
        # 重新写入 （和上面一步整合）
        if newJsonAry and len(newJsonAry) > 0:
            with open(cfglistjson_dir, 'w') as cfglistjson:
                json.dump(newJsonAry, cfglistjson, indent=2, ensure_ascii=False)
