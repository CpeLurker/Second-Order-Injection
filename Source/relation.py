import re
info =  [r'.*user.*',r'.*member.*',r'.*resume.*']
comment = [r'.*user.*',r'.*member.*',r'.*article.*',r'.*comment.*',r'.*ms.*',r'.*message.*',r'.*liuyan.*']
order = [r'.*user.*',r'.*member.*',r'.*DELIVERY.*',r'.*addr.*',r'.*order.*']
table = 'article'
# for p in comment:
# 	print(p)
# 	m = re.match(p,table,re.I)
# 	mm = re.match(p,'liuyan',re.I)
# 	if mm:
# 		print(m,mm)