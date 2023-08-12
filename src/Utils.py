
import os
from os import path

class Utils:

    def readFileList(dir: str, extname: str = 'xlsx') -> list:
        """ 读取dir下的所有文件扩展名==extname的文件 """
        if not path.exists(dir):
            print('路径错误：' + dir)
            return
        files = os.listdir(dir)
        rst: list = []
        for file in files:
            textname = path.splitext(file)[-1][1:]
            if textname == extname:
                rst.append(file)
        return rst

# 测试
# rst: list = Utils.readFileList(path.join(path.dirname(__file__) , '../xlsx'))
# print(rst)