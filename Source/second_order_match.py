import re
import regex
import types
from clean import filter_data

#变量列表
#变量提取
# def var_match(source,exp):
# 	reg_var = exp
# 	pattern = re.compile(reg_var,re.I)
# 	data = pattern.findall(source)
# 	var = clean(data)
# 	if(len(data)==1):
# 		list_var.add(data[0])
# 	return list_var


#select语句变量提取
def select_sql(content):

	res_Sel = {}
	column = []
	column_m  = []
	reg_sql_Sel = regex.regex_sql_SELECT_TableColumn
	pattern_Sel = re.compile(reg_sql_Sel,re.I|re.S)
	sel_data = pattern_Sel.findall(content)
	if(len(sel_data)==1):
		if(isinstance(sel_data[0],tuple)):
			table = str(filter_data(sel_data[0][0]))
			res_Sel['Table'] = table 
			columns = str(filter_data(sel_data[0][1]))
			columns = columns.replace('AND','-').replace('and','-')
			for c in columns.split("-"):
				c = c.strip()
				column.append(c)
		column_num = len(column)
		if column_num>1:
			# print("*"*50)
			# print(column)
			for col in column:
				p = re.compile(regex.regex_Select_Columns,re.I)
				col =  p.findall(col)
				for param in col:
					column_m.append(str(param).strip())
			if(len(column_m)>1):
				res_Sel['Column'] = column_m
				# print(res_Sel['Column'])
			# print("*"*50)
			# print("-"*80)
	return res_Sel


#Insert 语句变量提取
def insert_sql(content):
	res_In = {}
	cols = []
	values = []
	reg_sql_In = regex.regex_sql_INSERT_TableColumn
	pattern_In = re.compile(reg_sql_In,re.I)
	in_data = pattern_In.findall(content)
	if(len(in_data)==1):
		if(isinstance(in_data[0],tuple)):
			table = str(filter_data(in_data[0][0]))
			res_In['Table'] = table 

			columns = str(filter_data(in_data[0][1]))
			for column in columns.split(","):
				column = column.strip()
				cols.append(column.strip('`'))
			res_In['Column'] = cols

			value = str(filter_data(in_data[0][2]))
			for v in value.split(','):
				v = v.strip()
				values.append(v.strip('`'))
			res_In['Value'] = values
			# print(res_In['Value'])
	return res_In


#Update
def update_sql(content,RegExpression):
	res_Up = {}
	cols = []
	value = []
	column = []
	cell_list = []
	reg_sql_Up = RegExpression
	pattern_Up = re.compile(reg_sql_Up,re.I|re.S)
	up_data = pattern_Up.findall(content)
	if(len(up_data)==1):
		if(isinstance(up_data[0],tuple)):
			table = str(filter_data(up_data[0][0]))
			res_Up['Table'] = table

			part_data = str(filter_data(up_data[0][1]))

			equal_num = len(re.findall('=', part_data))
			if equal_num  == 1:
				c = str(filter_data(part_data.split('=')[0]))
				v = str(filter_data(part_data.split('=')[1]))

				value.append(v.strip())
				column.append(c.strip())
			if equal_num > 1:

				for cell in (part_data.split(',')): 
					cell = cell.strip()
					cell_list.append(cell)

				for cell_ in cell_list:
					col = filter_data(cell_.split('=')[0])
					column.append(col.strip())

					val = filter_data(cell_.split('=')[1])
					value.append(val.strip())

			else:
				pass

			res_Up['Column'] = column
			res_Up['Value'] = value
			
	return res_Up
	


