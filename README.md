# excel2json

## excel表配置说明

1. 工作表sheet以 **#** 开头，则表示此工作表不处理
2. 表的第1，2行，第1列到第5列，说明导出文件的相关信息，目前仅仅支持json文件的导出，也就是客户端文件的导出。如果服务端也是用json，则导出json文件即可。前面的列数将作为key存在，如果是n个key，则前面n列为key。
3. 表的第4-7行，描述导出的每列数据信息
    1. 第4行，是描述说明
    2. 第5行，是导出列的名称
    3. 第6行，导出数据类型，目前支持 number, string, array, object
    4. 第7行，是否导出客户端和服务端字段，SC。
    5. 这4行列表的后面不能有多余的说明，否则也将其作为要导出的列处理。下面的行数可以添加多余说明
4. 1，7行是固定的格式，不能多也不能少。1-2行的列数也是固定的，不可有多余，4-7行的列数根据实际情况处理，不固定；但不能有多余的非导出的说明

目前支持拖动 xlsx 文件到 build.bat 中进行导出。暂不支持点击 build.bat 导出xlsx所在目录下的全部xlsx。

## 导出文件说明

1. `output/cfglist.json` 文件，是所有都导出的json文件名集合
2. `output/config.ts` 文件，是导出的json文件的接口声明文件，便于游戏内使用

## python语法

os.path.exists(path) 如果路径 path 存在，返回 True；如果路径 path 不存在或损坏，返回 False。

os.path.getsize(path) 返回文件大小，如果文件不存在就返回错误

`__file__` 文件路径

`__dir__` 目录路径

os.path.join(path1[, path2[, ...]])	把目录和文件名合成一个路径

os.path.normcase(path) 转换path的大小写和斜杠

os.path.normpath(path)	规范path字符串形式

sorted(dict.keys())  字典key排序

enumerate(dict.keys()) 字典key的序号遍历方式  for i,v in enumerate() i就是序号从0开始，v就是key值

## TODO

- 新增有修改的才一键操作功能（导出选中，导出变化，导出所有）