# from itertools import combinations 

# print(list(combinations(range(3),2)))

# print(list(combinations([0,1,2],2)))

from collections import namedtuple 

ND = namedtuple("show",["first","second"])

cc = ND("my","hello")
print(cc.first)