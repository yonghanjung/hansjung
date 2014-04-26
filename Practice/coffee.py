coffee = 10
while 1:
	money = int(raw_input("Input Money!"))
	if money == 300:
		print "Coffee"
		coffee = coffee -1
	elif money > 300:
		print "Change of %d" %(money - 300)
	else :
		print "Return money, No coffee"
		print "Left coffee is %d" %coffee
	if not coffee:
		print "No coffee at all, sorry"
		break
