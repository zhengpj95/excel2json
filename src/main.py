"""
bat脚本操作
"""

import sys
import os
from Utils import Utils
from excel2json import Excel2Json
from Utils import OUTPUT_ROOT


if __name__ == '__main__':
    # print(sys.argv)

    if sys.argv and len(sys.argv) > 2:
        # 拖拽单独excel表导出
        if sys.argv and len(sys.argv) > 1 and sys.argv[1]:
            xlsxUrl = os.path.join(sys.argv[1])
        if sys.argv and len(sys.argv) > 2 and sys.argv[2]:
            outputRoot = os.path.join(sys.argv[2])
        
        # 若导出路径不存在，创建
        if not os.path.exists(outputRoot):
            os.makedirs(outputRoot)

        # 开始处理excel表
        excel2Json = Excel2Json(xlsxUrl, outputRoot)
        excel2Json.readFile()

    else:
        # 运行所有的excel
        currentpath = os.path.abspath(__file__)
        dirname = os.path.dirname(currentpath)
        outputRoot = OUTPUT_ROOT

        # 若导出路径不存在，创建
        if not os.path.exists(outputRoot):
            os.makedirs(outputRoot)

        # 遍历处理所有的excel文件
        xlsxRoot = os.path.normpath(os.path.join(dirname, os.path.pardir, 'xlsx'))
        xlsxFils = Utils.readFileList(xlsxRoot)
        for file in xlsxFils:
            newUrl = os.path.normpath(os.path.join(xlsxRoot, file))
            excelJson = Excel2Json(newUrl, outputRoot)
            excelJson.readFile()

