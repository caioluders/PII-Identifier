import re, unidecode
from operator import itemgetter

def calculate_distance(data,x,keywords) :
	results = []

	for k in keywords :
		i_x = data.find(x)
		relevant_data = unidecode.unidecode(data[:i_x].lower())
		i_k = relevant_data.find(k)

		if i_k < 0 : continue

		i_k += len(k)
		percent_distance = 100-((i_x-i_k)*100 / len(data))
		results.append( [ x, k , percent_distance ] )

	return sorted(results, key=itemgetter(2))	

def cpf_check(data) :
	cpf_re = re.compile(r"\d{11}|\d{3}\.\d{3}\.\d{3}-\d{2}")	
	
	maybe_cpfs = re.findall(cpf_re,data)
	maybe_cpfs_parsed = [ c.replace(".","").replace("-","") for c in maybe_cpfs ]
	
	true_cpfs = []

	for c in maybe_cpfs_parsed :
		c1 = list(map(int,list(c)))
		c4 = c1[:9]
		c2 = [ c4[cc]*(10-cc) for cc in range(len(c4)) ]
		d1 = 11-(sum(c2)%11)
		c4.append(d1)
		c3 = [ c4[cc]*(11-cc) for cc in range(len(c4)) ]
		d2 = 11-(sum(c3)%11)
		c4.append(d2)
		if c == ''.join(map(str,c4)) : true_cpfs.append(c) 
	
	return true_cpfs


def rg_check(data) :
	rg_re = re.compile(r"\d{9}|\d{2}\.\d{3}\.\d{3}-\d{1}")

	maybe_rgs = re.findall(rg_re,data) 
	maybe_rgs_parsed = [ r.replace(".","").replace("-","") for r in maybe_rgs ]

	true_rgs = []

	for r in maybe_rgs_parsed :
		r1 = list(map(int,list(r)))
		r4 = r1[:8]
		r2 = [ r4[rr]*(2+rr) for rr in range(len(r4)) ]
		d1 = 11-(sum(r2)%11)
		r4.append(d1)
		if r == ''.join(map(str,r4)) : true_rgs.append(r)

	return true_rgs

def birthday_check(data) :

	date_re = re.compile(r"(\d{2}(\.|-|\/)\d{2}(\.|-|\/)(\d{4}|\d{2}))")
	keywords = ["birthday","aniversario","Data de nascimento"]

	dates_list = re.findall(date_re,data)
	dates = []

	for d in dates_list :
		dates.append( calculate_distance(data,d[0],keywords)  )

	return dates

def fullname_check(data) :
		
	fullname_re = re.compile(r"[A-Z]\w+\s[A-Z]\w+")
	keywords = ["name","nome"]

	names_lists = re.findall(fullname_re,data)
	names = []

	for n in names_lists :
		names.append( calculate_distance(data,n,keywords) )	

	return names
			
