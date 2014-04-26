patientfile = open("patientlist3.txt")
numberfile = open("patientlist2.txt")
patientlist = patientfile.read()
numberlist = numberfile.read()
patients = patientlist.split("\n")
numbers = numberlist.split("\n")


i = 0
f = file('namelist2.txt','a+')

while i < len(numbers):
	name = patients[i] + '_' + numbers[i] + '\n'
	f.write(name)
	i += 1
	
f.close()



