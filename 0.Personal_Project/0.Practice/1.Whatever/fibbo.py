def fibbo(basic):
	basic.append(basic[len(basic)-1] + basic[len(basic)-2])
	return basic 

def main():
	basic = [1,1]
	inp = input()
	
	for i in range(0,inp):
		basic = fibbo(basic)
	basic = basic[0:len(basic)-2]
	print basic[len(basic)-1]

if __name__ == "__main__":
	main()