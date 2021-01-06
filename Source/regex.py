'''
生成特征库
'''
import re
import random
# regex_var = "\$(.*)\s*=\s*.*POST\[.*\].*;"
regex_var = "\$(.*)\s*=\s*.*trim.*|\$(.*)\s*=\s*.*addslashes.*|\$(.*)\s*=\s*.*stripslashes.*"
regex_Select_Columns = "(.*)=\S*|(.*)"
regex_sql_SELECT = "(select.*from.*where.*);"
regex_sql_SELECT_TableColumn = "select .* from\s*(.*)\s*where\s*(.*)"
regex_sql_SELECT_Column_Table = "select (.*) from (.*) where\s*.*"
# regex_sql_INSERT 
regex_sql_INSERT_TableColumn = "insert into (.*) \((.*)\) values \((.*)\)"
regex_sql_INSERT_TableColumn2 = "insert into (.*)\s*\((.*)\)\s*values\s*\((.*)\)"
regex_sql_UPDATE_TableColumn = "update (.*) set (.*) where .*"
regex_SELECT1 = "select\S(?P<table>.*)\S\s*->\s*from.*[(](?P<column>.*?)[)]*\s*->where\S(?P<attr1>.*)\S\s*->where\S(?P<attr2>.*)\S;" #捕捉模式
regex_SELECT2 = "select\S(?P<table>.*)\S\s*->\s*from.*[(](?P<column>.*?)[)]*\s*->where\S(?P<attr1>.*);"
regex_sel_param1 = "select\S(?P<table>.*)\S\s*->\s*from.*[(](?P<column>.*?)[)]*\s*->where\S*=(?P<value1>.*)\S\s*->where\S*=(?P<value2>.*)\S;"


# p = re.compile(regex_sql_UPDATE_TableColumn, re.I)
# sql = "update usertext set username = 'a' , address = 'b' where 1=1"
# f = p.findall(sql)
# print(f)

ans_list = ['name','pwd']
value1 = "test'/*"
value2 = "*/,%s=user()-- -"%('pwd')
sql =  "UPDATE info set"+" name" + "=" +"'"+value1+"'"+ "," +"pwd" + "=" +"'"+value2+"'"
print(sql)

