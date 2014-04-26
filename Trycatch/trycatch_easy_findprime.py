import math
def is_prime(n):
    if n % 2 == 0 and n > 2: 
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

num = 0
for i in range(2,100):
	if is_prime(i) == 1:
		print i,
		num += 1
		if num % 5 == 0:
			print ""  
