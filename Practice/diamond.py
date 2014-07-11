def diamond(th, leng):
	# Initialize array 
	# peak mid 
	# Calculate how many 
	arr = [" "] * leng
	mid = leng / 2 + 1 
	if th <= mid :
		k = th
	else : 
		k = mid - (th - mid) 		
	howmany = 2*k - 1
	arr[mid-howmany/2: mid+howmany/2] = "*" * howmany

	arr.reverse()
	arr.pop()
	arr.reverse()
	return arr

def main():
	inp = input()
	for i in range(0,inp):
		output = diamond(i+1, inp)
		print ''.join(map(str, output))

if __name__ == '__main__':
	main()