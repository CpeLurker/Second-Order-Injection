import re

'''
数据处理
'''
#数据过滤
def filter_data(data):
	sp_character = '[\r\n\t\'"."" "]'			#过滤文本格式符及其他
	try:
		data = re.sub(sp_character, '', data)			#过滤空格
		new_data = data.strip()

		return new_data
	except:
		if isinstance(data, tuple):						#元组数据的处理
			# tuple to str
			data = ''.join(data)
			new_data = filter_data(data)
			
		return new_data