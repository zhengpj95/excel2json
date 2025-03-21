""" 
把 excel 导出 json | lua
"""

import json
import os
import time

from openpyxl import load_workbook
from openpyxl.worksheet import worksheet

import cfglistjson
import configts
import json2lua
import sheetindex
import str2list


class SheetStruct:
    """ 表的导出信息 """

    def __init__(self):
        self.server_name = None  # 服务端导出文件名称
        self.client_name = None  # 客户端导出文件名称
        self.key_count = None  # key的数量
        self.special_type = None  # 特殊的格式
        self.sheet_title = None  # sheet名称
        self.xlsx_title = None  # xlsx名称


class DataStruct:
    """ 导出数据的结构体信息 """

    def __init__(self):
        self.name = None  # 字段名
        self.type = None  # 类型 (number, string, array, object)
        self.cs = None  # 导出字段（S服务端C客户端）
        self.definition = None  # 字段名注释


class Excel2Json:
    xlsl_url = ''
    # 配表信息定义的行数
    struct_row = [4, 5, 6, 7]
    # 配表真实数据要导出的列数，每行的后面可能有些说明，但是是不用导出，所以需要记录要导出的真实列数，也就是structRow行的真实列数
    struct_col_len = 0
    # 配表真实数据开始的行数
    start_row = 8
    sheet: worksheet.Worksheet = None
    # 表头结构体
    sheet_struct: SheetStruct = None
    # 导出路径
    output_root: str = ''

    def __init__(self, xlsx_url: str, output_root: str) -> None:
        self.xlsl_url = xlsx_url
        self.output_root = output_root  # 导出路径

    def read_file(self) -> None:
        xlsxTitle = self.get_xlsx_title()
        print('===== 开始处理表：', xlsxTitle, " =====")
        wb = load_workbook(filename=self.xlsl_url)
        # print(wb.sheetnames)
        # print(wb.worksheets)
        for sheet in wb.worksheets:
            # title中以#开头的表示不导出
            if sheet.title[0] == '#':
                continue
            self.sheet = sheet
            if not self.get_sheet_struct():
                continue
            self.deal_single_sheet()
        self.sheet = None
        self.xlsl_url = ''
        self.sheet_struct = None
        print('===== 结束处理', xlsxTitle, " =====\n")

    def get_xlsx_title(self) -> str:
        """ 获取xlsx文件名称 """
        basename = os.path.basename(self.xlsl_url).replace('.xlsx', '')
        return basename

    def get_sheet_struct(self) -> SheetStruct:
        """ 获取当个sheet导出文件的名称以及key数量 """
        serverName = self.sheet.cell(row=1, column=2).value
        clientName = self.sheet.cell(row=1, column=5).value
        keyCount = self.sheet.cell(row=2, column=2).value
        specialType = self.sheet.cell(row=2, column=5).value
        if not (serverName or clientName):
            return None
        struct = SheetStruct()
        struct.server_name = serverName
        struct.client_name = clientName
        struct.key_count = keyCount
        struct.special_type = specialType == 1
        struct.sheet_title = self.sheet.title
        struct.xlsx_title = self.get_xlsx_title()
        self.sheet_struct = struct
        return struct

    def get_row_value(self, row: int) -> list:
        """ 获取某行的数据 """
        columns = self.sheet.max_column
        rowData = []
        for i in range(1, columns + 1):
            cellValue = self.sheet.cell(row=row, column=i).value
            # 单元格填0是需要导出的
            if cellValue is None:
                break
            rowData.append(cellValue)
        return rowData

    def get_data_struct(self) -> dict:
        """ 导出数据的结构体信息 """
        row4 = self.get_row_value(self.struct_row[0])
        row5 = self.get_row_value(self.struct_row[1])
        row6 = self.get_row_value(self.struct_row[2])
        row7 = self.get_row_value(self.struct_row[3])
        dataDict: dict = {}
        self.struct_col_len = len(row5)
        for i in range(0, len(row5)):
            struct = DataStruct()
            struct.name = row5[i]
            struct.type = row6[i]
            struct.cs = row7[i].upper()
            struct.definition = row4[i]
            dataDict[i] = struct
        return dataDict

    def deal_single_sheet(self) -> None:
        """ 处理单张sheet """
        if not self.sheet_struct:
            return
        # print(sheet.max_row, sheet.max_column)
        # print('start to deal sheet: ', self.sheet.title)

        if self.sheet_struct.special_type:
            self.deal_special_reach_row_data()
        else:
            self.deal_each_row_data()
        sheetindex.deal_sheet_index_file(self.sheet_struct.xlsx_title, self.sheet_struct.sheet_title,
                                         self.sheet_struct.client_name)

    def deal_special_reach_row_data(self) -> None:
        """ 处理特殊的导出格式，竖状 """
        dataStruct = self.get_data_struct()
        if not dataStruct:
            return

        totalJson = {}
        for row in range(self.start_row, self.sheet.max_row + 1):
            rowData: DataStruct = self.get_row_value(row)
            if len(rowData) == 0 or rowData[0] is None or 'C' not in rowData[2]:
                break

            totalJson[rowData[0]] = eachRowJson = {}
            col0: DataStruct = dataStruct[0]  # key
            eachRowJson[col0.name] = rowData[0]
            col3: DataStruct = dataStruct[3]  # value

            if rowData[1] == 'array':
                eachRowJson[col3.name] = str2list.str_to_list(rowData[3])
            elif rowData[1] == 'object':
                eachRowJson[col3.name] = json.loads(rowData[3])
            else:
                eachRowJson[col3.name] = rowData[3]

        self.deal_json_data(totalJson)

    def deal_each_row_data(self) -> None:
        """ 读取每行配置，处理导出数据 """
        dataStruct = self.get_data_struct()
        if not dataStruct:
            return

        # 判断是否有客户端或服务端字段
        haveClient = False
        haveServer = False
        for idx in range(0, len(dataStruct)):
            if haveClient is True and haveServer is True:
                break
            if 'C' in dataStruct[idx].cs and haveClient is False:
                haveClient = True
            if 'S' in dataStruct[idx].cs and haveServer is False:
                haveServer = True

        totalKey = self.sheet_struct.key_count  # 表中配置的key数量
        maxRow = self.sheet.max_row

        totalJson = {}
        luaJson = {}  # 先生成临时json，再转化为lua
        for row in range(self.start_row, maxRow + 1):
            rowData = self.get_row_value(row)
            if len(rowData) == 0 or rowData[0] is None:
                break

            eachRowJson = totalJson
            eachLuaJson = luaJson
            for key in range(0, totalKey):
                if not eachRowJson.get(rowData[key]):
                    eachRowJson[rowData[key]] = {}
                    eachLuaJson[rowData[key]] = {}
                eachRowJson = eachRowJson.get(rowData[key])
                eachLuaJson = eachLuaJson.get(rowData[key])

            for col in range(0, self.struct_col_len):
                colStruct: DataStruct = dataStruct[col]
                if 'C' in colStruct.cs:
                    if colStruct.type == 'array':
                        eachRowJson[colStruct.name] = str2list.str_to_list(
                            rowData[col])
                    elif colStruct.type == 'object':
                        eachRowJson[colStruct.name] = json.loads(rowData[col])
                    else:
                        eachRowJson[colStruct.name] = rowData[col]
                if 'S' in colStruct.cs:
                    if colStruct.type == 'array':
                        eachLuaJson[colStruct.name] = str2list.str_to_list(
                            rowData[col])
                    elif colStruct.type == 'object':
                        eachLuaJson[colStruct.name] = json.loads(rowData[col])
                    else:
                        eachLuaJson[colStruct.name] = rowData[col]

        if haveClient:
            self.deal_json_data(totalJson)
        # else:
        #     print('\t\t【{0}】不需要导出json'.format(self.sheet.title))

        if haveServer:
            self.deal_lua_data(luaJson)
        # else:
        #     print("\t\t【{0}】不需要导出lua".format(self.sheet.title))

    def deal_json_data(self, obj: dict) -> None:
        """ 导出json数据 """
        struct = self.sheet_struct
        if not struct.client_name:
            # print(self.xlslUrl + ' --- 客户端配置名为空 -- 不导出json')
            return

        with open(self.output_root + "/" + struct.client_name, "w", encoding='utf-8') as outfile:
            json.dump(obj, outfile, indent=2, ensure_ascii=False)
            # outfile.write(json.dumps(obj, indent=4, ensure_ascii=True))

        self.deal_cfglist_json(struct.client_name)
        self.deal_config_ts(struct.client_name)

    def deal_lua_data(self, obj: dict) -> None:
        """ 导出lua数据 """
        struct = self.sheet_struct
        if not struct.server_name:
            # print(self.xlslUrl + ' --- 服务端配置名为空 -- 不导出lua')
            return

            # lua说明
        urlList = self.xlsl_url.split(os.sep)  # 获取路径中的xlsx文件名
        luaStr = "-- {0}\n-- {1}\n".format(urlList[-1], struct.server_name)
        luaStr += "-- %s\n\n" % time.strftime(
            "%Y-%m-%d %H:%M:%S", time.localtime())
        luaStr += "return"
        # json转化为lua
        wf = open(self.output_root + "/" + struct.server_name, 'w', 1, 'utf-8')
        wf.write(luaStr + json2lua.dic_to_lua_str(obj))
        wf.close()

    def deal_cfglist_json(self, client_name: str) -> None:
        """ 处理 cfglist.json 文件 """
        # print('start to export cfglist.json file')
        cfglistjson.deal_cfglist_json(client_name, self.output_root)
        # print('write cfglist.json successful!!!')

    def deal_config_ts(self, client_name: str) -> None:
        """ 导出config.d.ts文件 待处理 """
        # print('start to export config.ts file')
        dataDict: dict = self.get_data_struct()  # 传入结构体
        struct = configts.ConfigInterfaceStruct(client_name, self.sheet.title, dataDict, self.output_root)
        configts.deal_config_ts(struct)
