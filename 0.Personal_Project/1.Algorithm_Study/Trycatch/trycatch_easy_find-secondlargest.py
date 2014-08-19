import collections 
a = map(int, raw_input().split())
counter = collections.Counter(a)
b = counter.keys()
b.sort()
print b[len(b)-2]

