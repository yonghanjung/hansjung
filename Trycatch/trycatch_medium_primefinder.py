import math
def is_prime(n):
    if n % 2 == 0 and n > 2:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

a = map(float,raw_input().split())
a1 = int(math.ceil(a[0]))
a2 = int(math.floor(a[1])) 

for i in range(a1,a2):
	if is_prime(i) == 1 : print i,
