inp = input()

a = []
a.append(1)
a.append(1)

for i in range(0,inp+5):
	a.append(a[i] + a[i+1]) 

print a[inp-1]
