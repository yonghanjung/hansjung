def listsum (numbers):
	if not numbers:
		return 0
	else:
		(f, rest) = numbers
		return f+listsum(rest)

mylist  = (1,(2,(3, None)))
total = listsum(mylist)

print total