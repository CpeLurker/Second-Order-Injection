import re
import regex
import second_order_match
import Review


varlist = set()
list_var = set()

#变量提取 进行粗粒度提取
def var_match(content):
	reg_var = regex.regex_var
	p = re.compile(reg_var,re.I)
	data = p.findall(content)
	if(len(data)==1) and (len(data[0])==3):

		if data[0][0]:
			e_data = data[0][0]
			varlist.add(clean_data(e_data).strip("$"))
		if data[0][1]:
			ex_data = data[0][1]
			varlist.add(clean_data(ex_data).strip("$"))
		if data[0][2]:
			exi_data = data[0][2]
			varlist.add(clean_data(exi_data).strip("$"))
		# list_var = var_review(varlist)
	else:
		pass
	
	return varlist

#结合审计的变量规律特征 对系统生成变量进行进一步过滤 对携带敏感词的变量进一步过滤
def var_review(vlist):
	review_list = Review.review_list_var
	var_list_ = set()
	for var in vlist:
		flag = True
		length =  len(review_list)
		while length > 0:
			if(var.find(review_list[length-1])!=-1):
				flag = False
				break
			length = length-1
		if flag==True:
			var_list_.add(var)
			
	return var_list_

#获取读取出库的的数据
def select_Column_Table(content,regex):
	res_Column_Table = {}
	columns = []
	pattern = re.compile(regex,re.I)
	data = pattern.findall(content)
	if(len(data)==1):
		if(isinstance(data[0],tuple)):
			column = str(second_order_match.filter_data(data[0][0]))
			if column != "*":
				column = column.replace('AND','-').replace('and','-')
				for c in column.split("-"):
					c = c.strip()
					columns.append(c)
				res_Column_Table['column'] = columns
			else:
				res_Column_Table['column'] = column
			table = str(second_order_match.filter_data(data[0][1]))
			res_Column_Table['table'] = table
	return res_Column_Table






#数据清洗
def clean_data(data):
	#一般地考虑str格式
	#空白字符
	data = str(data).strip()
	if(len(data)>16 or len(data)<2):
		data = ''
	if data.isalpha():
		data = data
	else:
		data = ''
	return data

	#列表数据处理
def format_data(data):
	p_table = re.compile(format_table_regex)				#表
	p_column = re.compile(format_column_regex)				#列
	p_var = re.compile(format_var_regex)					#变量
	h_table_data = p_table.findall(data)
	h_column_data = p_column.findall(data)
	h_var_data = p_column.findall(data)
	h_data = [h_table_data,h_column_data,h_var_data]
	return h_data


def li_handle(the_list):
	li_handled_data = []
	for ue in the_list:
        #判断数据类型是不是列表
		if isinstance(ue, list):
			li_handle(ue)					
		else:
			li_handled_data.append(ue)
	return li_handled_data