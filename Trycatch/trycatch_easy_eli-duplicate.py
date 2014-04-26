import collections
a = map(int,raw_input().split())
counter = collections.Counter(a)
print(counter.keys())

