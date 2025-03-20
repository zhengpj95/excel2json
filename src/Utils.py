import os
from os import path

# 常量定义，xlsx文件夹路径
XLSX_ROOT = path.normpath(path.join(path.dirname(__file__), '../xlsx'))
# 常量定义，output文件夹路径
OUTPUT_ROOT = path.normpath(path.join(path.dirname(__file__), "../output"))
# 常量定义，output/client，客户端导出json路径
CLIENT_ROOT = path.normpath(path.join(OUTPUT_ROOT, './client'))
# 常量定义，output/server，服务端导出lua路径
SERVER_ROOT = path.normpath(path.join(OUTPUT_ROOT, './server'))


class Utils:

    @staticmethod
    def readFileList(dir_path: str, extname: str = 'xlsx', filter_str: str = "00") -> list:
        """ 读取dir下的所有文件扩展名==extname的文件 """
        if not path.exists(dir_path):
            print('路径错误：' + dir_path)
            return
        files = os.listdir(dir_path)
        rst: list = []
        for file in files:
            firstChar = path.splitext(file)[0][0]
            if firstChar == '~' or file.startswith(filter_str):  # 过滤打开中的文件
                continue
            text_name = path.splitext(file)[-1][1:]
            if text_name == extname:
                rst.append(file)
        return rst
