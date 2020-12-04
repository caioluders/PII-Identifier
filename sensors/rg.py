def rg_check(data) :

	maybe_rgs_parsed = [ r.replace(".","").replace("-","") for r in data ]

	true_rgs = []

	for r in maybe_rgs_parsed :
		r1 = list(map(int,list(r)))
		r4 = r1[:8]
		r2 = [ r4[rr]*(2+rr) for rr in range(len(r4)) ]
		d1 = 11-(sum(r2)%11)
		r4.append(d1)
		if r == ''.join(map(str,r4)) : true_rgs.append(r)

	return true_rgs
