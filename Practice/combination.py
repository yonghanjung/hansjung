import itertools
num = [1,2,3,4,5,6,7,8,9,10]
combinations = itertools.combinations(num,3)

matching = [c for c in combinations if reduce(lambda x, y: x * y, c, 1) == 60]
# 여기에서 60 은 10C3 에서 나온 숫자. 
print matching
