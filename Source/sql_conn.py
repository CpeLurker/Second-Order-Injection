import pymysql
import datetime
from color import end, warning, red

'''
user:root
pwd:root
数据库：case


'''
#创建连接
def mysql_connect():
	user='root'
	password = 'root'
	db = 'case'
	try:
		conn = pymysql.connect(user=user, password=password, database=db, charset='utf8')
	except:
		print("%s%s Unable to connect mysql!%s"%(warning,red,end))
	return conn
	# value1 = "test'/*"
	# value2 = "*/,%s=user() where 1=1 and sleep(2)-- -"%('pwd')
	# set_sql = "UPDATE info set"+" name" + "=" +"'"+value1+"'"+ "," +"pwd" + "=" +"'"+value2+"'"
	# try:
	# 	with conn.cursor() as cursor:
	# 		#sql = 'INSERT INTO info (name,pwd) values(%s, %s)'
	# 		#cursor.execute(sql,(value1,value2));
	# 		start_time = datetime.datetime.now()
	# 		cursor.execute(set_sql)
	# 	conn.commit()
	# 	end_time = datetime.datetime.now()
	# 	OK_time = (end_time - start_time).seconds
	# 	print(OK_time)
	# finally:
	# 	conn.close()
	
	# if OK_time > 1.6:
	# 	print ("There is a second-order injection after detection!")
		

# mysql_connect()