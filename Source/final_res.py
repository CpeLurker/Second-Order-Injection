# -*-coding:utf-8 -*-
import sys
import os
import re
import types

from color import end, red, green, yellow, good, warning,spc

res_num = 0
res_list = set()

#计数函数
def num_count():
###漏洞数
	global res_num 
	res_num += 1

def add_file_sql(filename,sql_string):
	res_filename = filename
	res_sql_string = sql_string
	res = "FilePath: "+res_filename +"\n"+ "injectSql: " + res_sql_string
	res_list.add(res)

#文件结果打印
def res_print():
	with open('result.txt', 'w', errors='ignores') as f:
		f.write("Final result as following!"+'\n')
		f.write('='*100+'\n')
		f.write('There are ')
		f.write(str(len(res_list)))
		f.write(" inject point have been found!"+'\n')
		for res in res_list:
			f.write(res+'\n')
		f.write('='*100+'\n')

	print("%sFinal result as following!"%(spc))
	print ('\n\n\n'+"%s=%s"%(yellow,end)*100+'\n')
	print ("%sThere are %s"%(red,end), end = ''),
	print ("%s"%(green), end = '')
	print (str(len(res_list)), end = '')
	print ("%s"%(end), end = '')
	print ("%s inject point have been found!%s"%(red,end))

	for res in res_list:
		print ("%s%s"%(good,end))
		print ("%s"%(green)+res+"%s"%(end))
	
	print ("%s=%s"%(yellow,end)*100)