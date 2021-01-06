#-*-coding:utf-8-*-
import re
import sys,getopt
# import tempfile
import regex
import time
import datetime
import traceback
import types
import Review
import ListFile
import final_res
import var_maintain
import static_analysis
import second_order_match
from color import spc, end, warning, red


'''
Python3
匹配符合条件的变量var
匹配符合条件的sql语句
Author:Lyc
'''
#regex_var = re.compile("([$].*);", re.I)		#变量 忽略大小写进行匹配

filename_path = []
list_var = set()
varlist = set()
list_sql = []
origin_sql = []
res_select = {}
sql_ = []
MODE = 0 #默认宽松检测模式
# path = sys.argv[1]
# INJECT_MODE = sys.argv[2]
argv = sys.argv[1:]

# path = r'E:\PHPStudy\phpStudy20161103\WWW\Demo'


# 扫描入口函数 , 传入 文件路径列表

def start_scan():
	print(path)
	filename_path = ListFile.ListFile(path)

	varlist = set()
	list_var = set()
	for fpath in filename_path:
		with open(fpath, 'r+', errors='ignore') as file_content:
			for line in file_content:
				varlist = var_maintain.var_match(line)

	list_var = var_maintain.var_review(varlist)
	print(list_var)

	for fpath in filename_path:
		with open(fpath, 'r+', errors='ignore') as resource:
			for line in resource:
				line = line.replace("{$table}","phpcms_").strip()

				flag = 1
				res_in = second_order_match.insert_sql(line)
				res_up = second_order_match.update_sql(line,regex.regex_sql_UPDATE_TableColumn)
				
			#直接分片重组
				static_analysis.Direct_Insert_Sql(res_in,list_var,line,flag,fpath,filename_path)
				static_analysis.Direct_Update_Sql(res_up,list_var,line,flag,fpath,filename_path)
				static_analysis.Direct_Insert_Sql_Up(res_in,list_var,line,flag,fpath,filename_path)

			#间接分片重组
				static_analysis.Indirect_Insert_Sql_In(res_in,list_var,line,flag,fpath,filename_path,MODE)
				static_analysis.Indirect_Update_Sql_In(res_up,list_var,line,flag,fpath,filename_path,MODE)

def Insert():
	print('The INJECTION Mode is INJECT_MODE')
	filename_path = ListFile.ListFile(path)

	varlist = set()
	list_var = set()
	for fpath in filename_path:
		with open(fpath, 'r+', errors='ignore') as file_content:
			for line in file_content:
				varlist = var_maintain.var_match(line)

	list_var = var_maintain.var_review(varlist)
	print(list_var)

	for fpath in filename_path:
		with open(fpath, 'r+', errors='ignore') as resource:
			for line in resource:
				line = line.replace("{$table}","phpcms_").strip()
				flag = 1
				res_in = second_order_match.insert_sql(line)
				# res_up = second_order_match.update_sql(line,regex.regex_sql_UPDATE_TableColumn)
				
			#INSERT
				static_analysis.Direct_Insert_Sql(res_in,list_var,line,flag,fpath,filename_path)
				static_analysis.Direct_Insert_Sql_Up(res_in,list_var,line,flag,fpath,filename_path)
				static_analysis.Indirect_Insert_Sql_In(res_in,list_var,line,flag,fpath,filename_path,MODE)
				
def Update():
	print('The INJECTION Mode is Update_MODE')
	filename_path = ListFile.ListFile(path)

	varlist = set()
	list_var = set()
	for fpath in filename_path:
		with open(fpath, 'r+', errors='ignore') as file_content:
			for line in file_content:
				varlist = var_maintain.var_match(line)

	list_var = var_maintain.var_review(varlist)
	print(list_var)

	for fpath in filename_path:
		with open(fpath, 'r+', errors='ignore') as resource:
			for line in resource:
				line = line.replace("{$table}","phpcms_").strip()
				flag = 1
				# res_in = second_order_match.insert_sql(line)
				res_up = second_order_match.update_sql(line,regex.regex_sql_UPDATE_TableColumn)
				
			#UPDATE
				static_analysis.Direct_Update_Sql(res_up,list_var,line,flag,fpath,filename_path)
				
				static_analysis.Indirect_Update_Sql_In(res_up,list_var,line,flag,fpath,filename_path,MODE)
def start(mode):
	currenttim = datetime.datetime.now()
	starttime = time.time()
	print("%s "%(spc),currenttim)
	print()
	
	# filename_path = ListFile.ListFile(path)
	if mode == "Insert":
		Insert()
	elif mode == "Update":
		Update()
	else:
		start_scan()

	final_res.res_print()

	endtime = time.time()
	costtime = endtime - starttime
	print ("The total time is ", end= '')
	print(costtime, end = '')
	print("s")




if __name__ == '__main__':
	# sys.stderr=tempfile.TemporaryFile()
	try:
		choice_mode = 'Default'

		try:
			opts, args = getopt.getopt(argv,"p:m:",["path=","mode="])
		except getopt.GetoptError:
			print("%s%s May be something went wrong!%s"%(warning,red,end))
		for opt, arg in opts:
			if opt in ("-p","--path"):
				path = arg
			elif opt in ("-m","--mode"):
				choice_mode = arg
		# print(choice_mode)
		
		start(choice_mode)

	except:
		traceback.print_exc()
		print("%s%s May be something went wrong!%s"%(warning,red,end))


	




