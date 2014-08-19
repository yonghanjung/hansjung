howmany = input()
sol = []
solunit = []

for trial in range(0,howmany):
	a = raw_input()
	b = a.split()
	num_a = float(b[0])

	if b[1] == 'kg':
		sol.append(round(num_a*2.2046,4))
		solunit.append('lb')
	elif b[1] == 'lb':
		sol.append(num_a*0.4536)
		solunit.append('kg')
	elif b[1] == 'g':
		sol.append(num_a*3.7854)
		solunit.append('l')
	elif b[1] == 'l':
		sol.append(round(num_a*0.2642+0.00005,4))
		solunit.append('g')

	## converting 

for i in range(0, howmany):
	print sol[i],solunit[i]
