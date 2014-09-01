
pound = 1
penny = pound * 100
pennies = [200,100,50,20,10,5,2,1]

def count_combs(left, i, comb, add):
	# left : (int) how many pound were left
	# i = (int) count for iteration 
	# comb = (list of list) possible combinations for counting numbers
	# add = (list)

    if add:
        comb.append(add)
	# If add is not empty, execute this  

    if left == 0 or (i+1) == len(pennies):
        if (i+1) == len(pennies) and left > 0:
            comb.append( (left, pennies[i]) )
            i += 1
        while i < len(pennies):
            comb.append( (0, pennies[i]) )
            i += 1

        return 1
    cur = pennies[i]
    return sum(count_combs(left-x*cur, i+1, comb[:], (x,cur)) for x in range(0, int(left/cur)+1))

print count_combs(penny, 0, [], None)
