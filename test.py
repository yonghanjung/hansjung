from __future__ import print_function 
import random

trial = 10
days = 5
start = 100 
unit  = 1
daily = []
mean = 0.0
var = 1.0 

f = open ('myfile','w')
for i in range(0, trial):
	daily = []
	gostart = start
	gomean = mean 
	for j in range(0,days):
		prev_start = gostart 
		gostart += random.gauss(gomean, var) * unit 
		f.write("%f, " %gostart)
		diff = gostart - prev_start
		gomean = (mean + diff)/2

	f.write('\n')
f.close()
