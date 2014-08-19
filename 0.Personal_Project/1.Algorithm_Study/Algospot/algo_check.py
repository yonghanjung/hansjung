import itertools 

howmany = input()
resp = []

def convert(inp):
	if inp == 'one':
		return 1
	elif inp == 'two':
		return 2
	elif inp == 'three':
		return 3
	elif inp == 'four':
		return 4
	elif inp == 'five':
		return 5
	elif inp == 'six':
		return 6
	elif inp == 'seven':
		return 7
	elif inp == 'eight':
		return 8
	elif inp == 'nine':
		return 9
	elif inp == 'zero':
		return 0

def compute(x,y,op):
	if op == '+':
		return x+y
	elif op == '*':
		return x*y
	elif op == '/':
		return x/y
	elif op == '-':
		return x-y 

def reader(x):
        1836
        2/302
        2/2 (100%)
        0/2 (0%)
        5
        2 (40%)

        채점 결과 분포
        문제 해결 진행 상황


	if x == 1:
		return 'one'
	elif x == 2:
		return 'two'
	elif x == 3:
		return 'three'
	elif x == 4:
		return 'four'
	elif x == 5:
		return 'five'
	elif x == 6:
		return 'six'
	elif x == 7:
		return 'seven'
	elif x == 8:
		return 'eight'
	elif x == 9:
		return 'nine'
	elif x == 0:
		return 'zero'

def solutionpool(word):
	pool = list(itertools.permutations(word))
	sol = []
	for i in range(0,len(pool)):
		sol.append(''.join(pool[i]))
	return sol

for trial in range(0,howmany):
	equ = raw_input()
	fac = equ.split()
	a = convert(fac[0])
	b = convert(fac[2])
	ans = compute(a,b,fac[1])
	answer = reader(ans)
	solpool = solutionpool(fac[4])
	mark = 0
	for i in range(0,len(solpool)):
		if answer == solpool[i]:
			mark  = 1
			break
		else:
			mark = 0
	if mark == 1:
		resp.append("Yes")
	else: 
		resp.append("No")

for i in range(0,len(resp)):
	print ''.join(resp[i])