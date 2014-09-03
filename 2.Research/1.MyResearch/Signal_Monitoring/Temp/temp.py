# -*- coding: utf-8 -*-

from Test.GMM import read_csv
from Test.GMM import build_matrix
from Test.GMM import decompose_train_test
from sklearn.decomposition import KernelPCA

filename1 = 'HE.csv'
filename2 = 'MI.csv'

A = read_csv(filename1, filename2)

HE_data = A[0]
MI_data = A[1]

for idx in HE_data:
    print idx, HE_data[idx]

print "\n \n"

#for idx in MI_data:
#    print idx, MI_data[idx]


A = build_matrix(A)

print "\n \n"



for idx in range(len(A[1])):
    print A[1][idx]

print "\n \n"

for idx in A[1][:10]:
    print idx

#for idx in range(len(A[3])):
#    print A[3][idx]




'''
#KPCA 누적 설명력 계산

HE_MI_train_test  = decompose_train_test(24,150,A)

HET =  HE_MI_train_test[0]
kpca = KernelPCA(n_components=2)
kpca.fit(HET)

print kpca.lambdas_  , len(kpca.lambdas_)
print  "\n"

kpca = KernelPCA(n_components=len(HET))
kpca.fit(HET)
print kpca.lambdas_, len(kpca.lambdas_)


A = sum(kpca.lambdas_)
print "\n"
B = [x/A for x in kpca.lambdas_]
print B
print "\n"

mysum = 0
myiter = 0
for idx in B:
    mysum += idx
    myiter += 1
    print myiter,mysum
'''