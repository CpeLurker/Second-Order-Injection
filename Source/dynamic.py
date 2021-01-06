#-*-coding:utf-8-*-
import re
import pymysql
import sql_conn
import types
import traceback
import final_res
import datetime
from color import end, red, green, yellow, info, good, warning, white, spc

def secheck(table,column,line,file_name):
	pds_data = []
	case_table = table
	case_column_list = column

	ans_list = del_repeat(case_column_list)
	my_line = line
	my_filename = str(file_name)

	try:
### tip
		print("%s%s Start dynamic detection By blind injection !%s"%(spc,white,end))
###连接数据库
		my_conn = sql_conn.mysql_connect()
		cursor = my_conn.cursor()
		cursor.execute("show tables")

 	### 丢弃已存在表
		for row in cursor.fetchall():
			if row[0] == case_table:
				cursor.execute("drop table "+case_table)
				my_conn.commit()

###创建表
	### SQL语句
	###创建数据库以及表	
		sql_create = "create table %s (id_sign int(3) primary key auto_increment not null);"%(case_table)
		cursor.execute(sql_create)

	### alter
		for create_column in asn_list:
			cursor.execute("alter table "+ case_table +" add column "+create_column+" varchar(50) not null default 'test_data';")


	### 载荷分片
		value1 = "test'/*"
		value2 = "*/ and sleep(2)--+"

	###数据入库
		sql_insert = "insert into "+case_table+" ("+ans_list[0]+","+ans_list[1]+") values (%s,%s)"
		cursor.execute(sql_insert)

	###脏数据出库
		sql_select = "select %s,%s from %s"%(ans_list[0],ans_list[1],case_table)
		cursor.execute(sql_select)
		params = cursor.fetchall()
		if len(params) > 0:
			for p in params:
				pds_data.append(p)

	### 载荷重组触发

		sql_tigger = "select * from "+"case_table"+" where "+ans_list[0]+" = "+"'"+pds_data[0][0]+"'"+" and "+ans_list[1]+" = "+"'"+pds_data[0][1]+"'"
		start_time = datetime.datetime.now()
		cursor.execute(sql_tigger)
		end_time = datetime.datetime.now()
		OK_time = (end_time - start_time).seconds
		print(OK_time)

	except:
		print("%s%s May be something went wrong!%s"%(warning,red,end))

	finally:
		cur.execute("""drop table """+case_table)
		my_conn.commit()

	if OK_time > 1.6:
		print ("%s%s There is a second-order injection after detection!%s"%(info,green,end))
		final_res.num_count()
		final_res.add_file_sql(my_filename,my_line)

	else:
		print ("%s%s There is no second-order injection after detection!%s"%(info,red,end))



#Insert插入动态检测
def incheck(table,column,line,file_name):
	pds_data = []
	case_table = table
	case_column_list = column

###数据清理
	ans_list = del_repeat(case_column_list)
	my_line = line
	my_filename = str(file_name)

	try:
	###Tips
		print("%s%s Start dynamic detection By comparing information !%s"%(spc,white,end))

	###连接数据库
		my_conn = sql_conn.mysql_connect()
		cursor = my_conn.cursor()

	 ###丢弃已存在表
		cursor.execute("show tables")
		for row in cursor.fetchall():
			if row[0] == case_table:
				cursor.execute("drop table "+case_table)
				my_conn.commit()
		cursor.execute("drop table temp")

###创建数据库及表
	### sql操作语句
		sql_create_temp = "create table temp (col1 varchar(50) NOT NULL default 'test_data',col2 varchar(50) default 'test_data')"
		sql_create = "create table %s (id_sign int(3) primary key auto_increment not null);"%(case_table)
		#sql_alter = "alter table "+ case_table +" add column %s varchar(50) not null default 'test_data';"

		sql_insert = "insert into "+case_table+" ("+ans_list[0]+","+ans_list[1]+") values (%s,%s)"
		sql_select = "select "+ans_list[0]+","+ans_list[1]+" from %s limit 1"%(case_table)

	### 载荷分片
		value1 = "test'/*"
		value2 = "*/,(select user()))-- "

	###创建
		cursor.execute(sql_create_temp)
		cursor.execute(sql_create)
		for create_column in ans_list:
			cursor.execute("alter table "+ case_table +" add column "+create_column+" varchar(50) not null default 'test_data';")
		
		cursor.execute(sql_insert,(value1,value2))
	###模拟数据出库
		cursor.execute(sql_select)
		params = cursor.fetchall()
		if len(params) > 0:
			for p in params:
				pds_data.append(p)
		# print(pds_data)
	###载荷重组触发
		sql_tigger = "insert into temp (col1,col2) values ("+"'"+pds_data[0][0]+"'"+","+"'"+pds_data[0][1]+"'"+")"
		# print(sql_insert_temp)
	###插入另一张表
		cursor.execute(sql_tigger)
		cursor.execute("select col2 from temp limit 1")
		res = cursor.fetchall()

		cursor.execute("select user()")
		user = cursor.fetchall()
		# print("_______use",user)
		if res==user:
			print ("%s%s There is a second-order injection after detection!%s"%(info,green,end))
			final_res.num_count()
			final_res.add_file_sql(my_filename,my_line)
		else:
			print ("%s%s There is no second-order injection after detection!%s"%(info,red,end))

###错误数据
	except:
		print("%s%s May be something went wrong!%s"%(warning,red,end))
	finally:
		my_conn.commit()

#Update更新动态检测
def upcheck(table,column,line,file_name):
### 存储数据
	pds_data = []
	case_table = table
	case_column_list = column


###数据清理
	ans_list = del_repeat(case_column_list)
	my_line = line
	my_filename = str(file_name)

	try:
	###Tips
		print("%s%s Start dynamic detection By blind injection!%s"%(spc,white,end))

	###连接数据库
		my_conn = sql_conn.mysql_connect()
		cur = my_conn.cursor()  
		cur.execute("show tables")
		for row in cur.fetchall():
			if row[0] == case_table:
				cur.execute("drop table "+case_table)
				my_conn.commit()
	
	###创建表
		sql_create = "create table %s (id_sign int(3) primary key auto_increment not null);"%(case_table)
		sql_alter = "alter table "+ case_table +" add column %s varchar(20) not null default 'test_data'"
		cur.execute(sql_create)
		# print (case_table)
		# print(sql_alter)
		for create_column in ans_list:
			cur.execute("alter table "+ case_table +" add column "+create_column+" varchar(50) not null default 'test_data';")

		sql_insert = "insert into "+case_table+" ("+ans_list[0]+","+ans_list[1]+") values (%s,%s)"
		sql_select = "select %s,%s from %s"%(ans_list[0],ans_list[1],case_table)

	###构造载荷片段
		#pay_value = "123' and sleep(2)-- -"
		value1 = "test'/*"
		value2 = "*/,%s=user() where 1=1 and sleep(2)-- -"%(ans_list[1])
		cur.execute(sql_insert,(value1,value2))
		cur.execute(sql_select)
		params = cur.fetchall()
		# print(params,type(params[0]))
		if len(params)>0:
			for p in params:
				pds_data.append(p)

		# print(value2)
		# sql_up = "UPDATE "+case_table+ " set "+ans_list[0]+" = %s"+","+ans_list[1]+" = %s"+" WHERE 1=1"
		# print(sql_up)

	###载荷重组触发
		sql_tigger = "UPDATE " + case_table+ " set "+ans_list[0]+ " = "+ "'"+pds_data[0][0]+"'"+"," + ans_list[1]+" = "+"'"+pds_data[0][1]+"'"+" WHERE 1=1"
		start_time = datetime.datetime.now()
		cur.execute(sql_tigger)
		my_conn.commit()
		end_time = datetime.datetime.now()
		OK_time = (end_time - start_time).seconds
		# print("TIME COST:", end = '')
		# print(OK_time,end = '')
		# print("s")

	except:
		traceback.print_exc()
		print("%s%s May be something went wrong!%s"%(warning,red,end))

	finally:
		cur.execute("""drop table """+case_table)
		my_conn.commit()


	if OK_time > 1.6:
		print ("%s%s There is a second-order injection after detection!%s"%(info,green,end))
		final_res.num_count()
		final_res.add_file_sql(my_filename,my_line)

	else:
		print ("%s%s There is no second-order injection after detection!%s"%(info,red,end))

		





def del_repeat(list1):
	list2 = []
	list1.reverse()
	for i in list1:
		if i not in list2:
			list2.append(i)
	list2.reverse()
	return list2