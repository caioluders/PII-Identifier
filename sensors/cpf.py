def cpf_check(data) :
	
	maybe_cpfs_parsed = [ c.replace(".","").replace("-","") for c in data ]
	
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
