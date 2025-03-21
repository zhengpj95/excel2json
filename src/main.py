"""
bat脚本操作
"""

import os
import sys

from Utils import OUTPUT_ROOT, XLSX_ROOT
from Utils import Utils
from excel2json import Excel2Json

if __name__ == '__main__':
    # print(sys.argv)

    if sys.argv and len(sys.argv) > 2:
        """ 拖拽单独excel表导出 """
        if sys.argv and len(sys.argv) > 1 and sys.argv[1]:
            xlsx_url = os.path.join(sys.argv[1])
        if sys.argv and len(sys.argv) > 2 and sys.argv[2]:
            output_root = os.path.join(sys.argv[2])

        # 若导出路径不存在，创建
        if not os.path.exists(output_root):
            os.makedirs(output_root)

        # 开始处理excel表
        excel2Json = Excel2Json(xlsx_url, output_root)
        excel2Json.read_file()

    else:
        """ 运行所有的excel """
        output_root = OUTPUT_ROOT

        # 若导出路径不存在，创建
        if not os.path.exists(output_root):
            os.makedirs(output_root)

        # 遍历处理所有的excel文件
        xlsx_root = XLSX_ROOT
        xlsx_files = Utils.read_file_list(xlsx_root)
        for file in xlsx_files:
            newUrl = os.path.normpath(os.path.join(xlsx_root, file))
            excelJson = Excel2Json(newUrl, output_root)
            excelJson.read_file()
