# import sys
# def DistanceToHigher(height):
#     # write code here
#     a=[]
#     a.append(0)
#     length=0
#     for i in height:
#         length+=1
#     print(length)
#     for i in range(1,length):
#         lengtha=0
#         for j in range(i-1,0,-1):
#             if height[j]>height[i]:
#                 a.append(i-j)
#                 lengtha=1
#                 break
#         if lengtha==0:
#             a.append(0)
#     return a
    
# line = sys.stdin.readline().strip()
# height= list(map(int, line.split()))
# a=DistanceToHigher(height)
# print(a)
# import sys
# line = sys.stdin.readline().strip()
# number= list(map(int, line.split()))
# length=0
# a=[]
# lengtha=0
# for i in number:
#     length+=1

# for i in range(2,length):
#     m=sorted(number[:i])
#     # print(m)
#     if(number[i]<m[i-1] and number[i]>=m[i-2]):
#         a.append(i)
#     else:
#         pass
# for i in a:
#     lengtha+=1
# if lengtha==0:
#     print('-1')
# else:
#     print(a)
import re
from bs4 import BeautifulSoup


import sys
line = sys.stdin.readline().strip(',')
number= list(map(int, line.split()))
bea_number1=[]
re.findall('1*')
for i in number:
    s=str(i).

