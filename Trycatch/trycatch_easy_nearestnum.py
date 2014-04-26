a = input()

cand1 = (int)(a ** (0.5))
cand2 = cand1 + 1
cand3 = cand1 - 1

cand1 = cand1 ** 2
cand2 = cand2 ** 2
cand3 = cand3 ** 2 

cand = [cand1,cand2,cand3]
canddif = [abs(cand1-a),abs(cand2-a),abs(cand3-a)]

print cand[canddif.index(min(canddif))]
