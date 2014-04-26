howmany = input()
xsol = []
ysol = []

for trial in range(0,howmany):
	x = []
	y = []
	for points in range(0,3):
		adr = map(int,raw_input().split())
		x.append(adr[0])
		y.append(adr[1])
	if x.count(x[0]) is 2:
		if x.count(x[1]) is 2:
			xsol.append(x[2])
		else:
			xsol.append(x[1])
	else:
		xsol.append(x[0])

	if y.count(y[0]) is 2:
		if y.count(y[1]) is 2:
			ysol.append(y[2])
		else:
			ysol.append(y[1])
	else:
		ysol.append(x[0])

for trial in range(0,howmany):
	print xsol[trial],ysol[trial]