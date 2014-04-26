howmany = input()
sol = []

for i in range(0,howmany):
	comeon = raw_input()
	firstpart = comeon[0]
	secondpart = comeon[1]
	if len(comeon)-1 > 1:
		for j in range(0,(len(comeon))):
			if (2*j + 3) <= len(comeon):
				firstpart += comeon[2*j+2]
				secondpart += comeon[2*j + 3]
		sol.append(firstpart,secondpart)

print firstpart+secondpart