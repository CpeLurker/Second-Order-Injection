import re
import dynamic
import sql_conn
import second_order_match
from color import end, red, yellow, que, filepath
import regex
from relation import info,comment,order
enter1 = []
enter2 = []

'''
接近传统的二阶注入 Select and Update

'''

# 最接近传统二阶注入 分片插入 读取
def Direct_Insert_Sql(res_in,var_list,sql_string,repeatFlag,fpath,filename_path):
	# print("Select detect!!!")
	param_num = 0
	line = sql_string.strip()
	temp_value_list = []			#对于当前匹配的操作语句中变量的记录
	temp_column_list = []
	if res_in and var_list and ("Value" in res_in.keys()):
		for var in var_list:
			for value,column in zip(res_in['Value'],res_in['Column']):
				if var == value.strip("$"):
					param_num +=1
					#摘要 记录参数
					temp_value_list.append(value)
					temp_column_list.append(column)
		# length = len(temp_value_list)
		if param_num > 1:
			table = res_in['Table']
			print()
			print("param_num: ",param_num)
			print(line)
			print("table_name: ",table)
			print("column_name: ",temp_column_list)
			print("value_name: ",temp_value_list)
			print()
			for re_path in filename_path:
				with open(re_path, 'r+', errors="ignore") as re_file:
					equal_num = 0
					for re_line in re_file:
						res_sel =  second_order_match.select_sql(re_line)
						if res_sel  and table==res_sel['Table'] and'Column' in res_sel.keys() :
							for column in temp_column_list:
								for column_ in res_sel['Column']:
									if column_ == column:
										equal_num+=1
									else:
										continue
						else:
							continue
					if equal_num > 1 and repeatFlag :
						repeatFlag = 0
						print("%s%s There may exist second-order injection and construct payload detection...%s"%(que,yellow,end))
						print("%s "%(filepath),end = '')
						print(fpath)
						print(line)
						dynamic.secheck(table,temp_column_list,line,fpath)
					else:
						pass


									
										
										
										
										


#...更新时
def Direct_Update_Sql(res_up,var_list,sql_string,repeatFlag,fpath,filename_path):
	param_num = 0
	equal_num = 0
	line = sql_string.strip()
	temp_value_list = []
	temp_column_list = []
	if res_up and var_list and ("Column" in res_up.keys()):
		for var in var_list:
			for value,column in zip(res_up['Value'], res_up['Column']):
				if value.strip("$") == var:
					param_num += 1
					# 关注存在隐患的value 
					temp_value_list.append(value.strip())		
					temp_column_list.append(column.strip())
		# print(param_num)
		if param_num > 1:
			table = res_up['Table']
			value = temp_column_list
			column = temp_column_list
			print()
			print("param_num: ",param_num)
			print(line)
			print("table_name: ",table)

			print("column_name: ",temp_column_list)
			print("value_name: ",temp_value_list)
			print()

			for re_path in filename_path:
				with open(re_path, 'r+', errors="ignore") as re_file:
					for re_line in re_file:
						res_sel =  second_order_match.select_sql(re_line)
						if res_sel and  ("Column" in res_sel.keys()):
							if table == res_sel['Table']:
								for column in temp_column_list:
									for column_ in res_sel['Column']:
										if column == column_:
											equal_num += 1
										else:
											continue
							else:
								continue
					if equal_num > 1 and repeatFlag:
						repeatFlag = 0
						print("%s%s There may exist second-order injection and construct payload detection...%s"%(que,yellow,end))
						print("%s "%(filepath),end = '')
						print(fpath)
						print(line)
						dynamic.secheck(table,temp_column_list,line,fpath)
					else:
						pass
									
# insert + update
def Direct_Insert_Sql_Up(res_in,var_list,sql_string,repeatFlag,fpath,filename_path):
	param_num = 0
	equal_num = 0
	string = sql_string.strip()
	column_list = var_list
	temp_column_list = []
	columns = []
	if res_in and var_list and "Column" in res_in.keys():
		for column in res_in['Column']:
			for re_column in column_list:
				if column==re_column:		
					param_num += 1				#确认是会被读取写入的列
					temp_column_list.append(column)	
		# print("___:",column_list)	
		# print("________:",temp_column_list)
		if param_num >1:
			table = res_in['Table']
			print()
			print("param_num: ",param_num)
			print(string)
			print("table_name: ",table)
			print("column_name: ",temp_column_list)
			# print("value_name: ",temp_value_list)
			print()
			global enter1
			global enter2
			for re_path in filename_path:
				if r"admin" in re_path  or r"install" in re_path:
					continue
				with open(re_path,'r+',errors="ignore") as re_file:
					for re_line in re_file:
						res_up = second_order_match.update_sql(re_line,regex.regex_sql_UPDATE_TableColumn)
						if res_up and ("Column" in res_up.keys()):
							if table == res_up['Table']:
								for column in temp_column_list:
									for column_ in res_up['Column']:
										if column == column_:
											equal_num += 1
						# print("equal_num:",equal_num)
					if equal_num > 1 and repeatFlag:
						repeatFlag = 0
						print("equal_num:",equal_num)
						print("%s%s There may exist second-order injection and construct payload detection...%s"%(que,yellow,end))
						print("%s "%(filepath),end = '')
						print(fpath)					
						print(string)	
							# sql_conn.mysql_connect()
						dynamic.upcheck(table,temp_column_list,string,fpath)				
					else:
						pass					





'''
间接分片重组
INSERT + INSERT
INSERT + SELECT

UPDATE + SELECT
UPDATE + INSERT
'''

# INSERT+INSERT
def Indirect_Insert_Sql_In(res_in,var_list,sql_string,repeatFlag,fpath,filename_path,mode):
	MODE = mode
	param_num = 0
	line = sql_string.strip()
	column_list = var_list
	temp_column_list = []
	columns = []
	if res_in and var_list and "Column" in res_in.keys():
		for column in res_in['Column']:
			for re_column in column_list:
				if column==re_column:		
					param_num += 1				#确认是会被读取写入的列
					temp_column_list.append(column)		
				
		if param_num >1:
			table = res_in['Table']
			tableA = table_judge(table)
			print()
			print("param_num: ",param_num)
			print(line)
			print("table_name: ",table)
			print("column_name: ",temp_column_list)
			# print("value_name: ",temp_value_list)
			print()
			global enter1
			global enter2
			for re_path in filename_path:
				if r"admin" in re_path  or r"install" in re_path:
					continue
				with open(re_path,'r+',errors="ignore") as re_file:
					for re_line in re_file:
						string = re_line.replace("{$table}","phpcms_").strip()
						re_res_in = second_order_match.insert_sql(string)
						if re_res_in and "Column" in re_res_in.keys():
							for column in temp_column_list:
								if column in re_res_in['Column']:
									if string != sql_string:
										tableB = table_judge(re_res_in['Table'])
										if repeatFlag == 1 and  (tableA!=tableB) and r"admin" not in fpath and r"install" not in fpath:
											if (findItem(enter1,enter2,string.strip(),sql_string.strip())):
												continue
											else:
												if (MODE == 1):				#精准检测模式
													table1 = tableA
													table2 = tableB
													print("%s%s The Strict detection mode %s"%(que,yellow,end))
													print("%s%s There may logically related tables:%s"%(que,yellow,end))
													print("Table:",table1,table2) 
													for p in info:
														label =  re.match(p,table1,re.I)
														if label:
															for p_ in info:
																label_ = re.match(p_,table2,re.I)
																if label_:
																	print("Table:",table1)
																	print("Table:",table2)
																	enter1.append(string)
																	enter2.append(line)
																	print("There may exist second-order injection and construct payload detection...")
																	dynamic.incheck(table,temp_column_list,line,fpath)
																else:
																	continue
														else:
															continue
													for p in comment:
														label =  re.match(p,table1,re.I)
														if label:
															for p_ in comment:
																label_ = re.match(p_,table2,re.I)
																if label_:
																	print("Table:",table1)
																	print("Table:",table2)
																	enter1.append(string)
																	enter2.append(line)
																	print("There may exist second-order injection and construct payload detection...")
																	dynamic.incheck(table,temp_column_list,line,fpath)
																else:
																	continue
														else:
															continue
												else:
													enter1.append(string)
													enter2.append(line)
													repeatFlag = 0
													print("%s%s There may exist second-order injection and construct payload detection...%s"%(que,yellow,end))
													print("%s "%(filepath),end = '')
													print(fpath)
													print(line)
													print(string)
													# sql_conn.mysql_connect()
													dynamic.incheck(table,temp_column_list,line,fpath)
										else:
											pass
									else:
										pass
								else:
									continue
							else:
								continue

#INSERT + Select
def Indirect_Update_Sql_In(res_in,var_list,sql_string,repeatFlag,fpath,filename_path,mode):
	MODE = mode
	param_num = 0
	line = sql_string.strip()
	column_list = var_list
	temp_column_list = []
	columns = []
	if res_in and var_list and "Column" in res_in.keys():
		for column in res_in['Column']:
			for re_column in column_list:
				if column==re_column:		
					param_num += 1				#确认是会被读取写入的列
					temp_column_list.append(column)		
				
		if param_num >1:
			table = res_in['Table']
			tableA = table_judge(table)
			print()
			print("param_num: ",param_num)
			print(line)
			print("table_name: ",table)
			print("column_name: ",temp_column_list)
			# print("value_name: ",temp_value_list)
			print()
			global enter1
			global enter2
			for re_path in filename_path:
				if r"admin" in re_path  or r"install" in re_path:
					continue
				with open(re_path,'r+',errors="ignore") as re_file:
					for re_line in re_file:
						string = re_line.replace("{$table}","phpcms_").strip()
						re_res_up = second_order_match.update_sql(string,regex.regex_sql_UPDATE_TableColumn)
						if re_res_up and "Column" in re_res_up.keys():
							for column in temp_column_list:
								if column in re_res_up['Column']:
									if string != sql_string:
										tableB = table_judge(re_res_up['Table'])
										if repeatFlag == 1 and  (tableA!=tableB) and r"admin" not in fpath and r"install" not in fpath:
											if (findItem(enter1,enter2,string.strip(),sql_string.strip())):
												continue
											else:
												if (MODE == 1):				#精准检测模式
													table1 = tableA
													table2 = tableB
													print("%s%s The Strict detection mode %s"%(que,yellow,end))
													print("%s%s There may logically related tables:%s"%(que,yellow,end))
													print("Table:",table1,table2) 
													for p in info:
														label =  re.match(p,table1,re.I)
														if label:
															for p_ in info:
																label_ = re.match(p_,table2,re.I)
																if label_:
																	print("Table:",table1)
																	print("Table:",table2)
																	enter1.append(string)
																	enter2.append(line)
																	print("There may exist second-order injection and construct payload detection...")
																	dynamic.incheck(table,temp_column_list,line,fpath)
																else:
																	continue
														else:
															continue
													for p in comment:
														label =  re.match(p,table1,re.I)
														if label:
															for p_ in comment:
																label_ = re.match(p_,table2,re.I)
																if label_:
																	print("Table:",table1)
																	print("Table:",table2)
																	enter1.append(string)
																	enter2.append(line)
																	print("There may exist second-order injection and construct payload detection...")
																	dynamic.incheck(table,temp_column_list,line,fpath)
																else:
																	continue
														else:
															continue
												else:
													enter1.append(string)
													enter2.append(line)
													repeatFlag = 0
													print("%s%s There may exist second-order injection and construct payload detection...%s"%(que,yellow,end))
													print("%s "%(filepath),end = '')
													print(fpath)
													print(line)
													print(string)
													# sql_conn.mysql_connect()
													dynamic.incheck(table,temp_column_list,line,fpath)
										else:
											pass
									else:
										pass
								else:
									continue
							else:
								continue


									
												
										




#判断元素是否在列表中
def findItem(list1,list2,item1,item2):
	if (item1 in list1) and (item2 in list2):
		return True
	elif (item2 in list1) and (item1 in list2):
		return True
	else:
		return False

#判断表名是否重复
def table_judge(table_name):
	List = table_name.split('_')
	name = List[len(List)-1]
	return name
