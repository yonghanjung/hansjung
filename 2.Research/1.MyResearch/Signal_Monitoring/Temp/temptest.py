# -*- coding: utf-8 -*-
import numpy as np
import math

num_people = 1000000000
hotel_period_day = 100
num_hotel = 100000
consider_day = 1000

def digit_compute(x):
    return np.log10(x)

# look for people who on two different days, were both at the same hotel
# 두 번 같은 호텔에 있어야 한다.

pr_day_hotel = float (1) / float(hotel_period_day)
pr_hotel_choose = float(1) / float(num_hotel)
pr_two_pp_same_day = pr_day_hotel ** 2
pr_two_pp_same_hotel_same_day = pr_two_pp_same_day * pr_hotel_choose
pr_two_pp_same_hotel_two_day = pr_two_pp_same_hotel_same_day ** 3

## how many events will happen

# 두개고를 경우의 수
def casenum(x):
    return (x ** 2) / 2

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)

## Expected number of events that look like evil-doing

case_pair = casenum(num_people)
#day_pair = casenum(consider_day)
day_pair = nCr(1000,3)
num_case_evil = case_pair * day_pair * pr_two_pp_same_hotel_two_day

## The number of evil-doer pairs




### ### ### ### ### ### ### ### ### ###

print "우리가 고려하는 사람들의 수", num_people
print "한 사람은 100일에 한 번 호텔에 갑니다.", hotel_period_day
print "따라서 하루에 호텔에 묵는 사람의 수는", num_people / hotel_period_day
print "여러 Days 중 한 사람이 호텔에 묵고 있는 날이 오늘일 확률", pr_day_hotel
print "어떤 사람이 여러 호텔 중 어느 특정 호텔을 택했을 확률", pr_hotel_choose
print "어느 두 사람이 오늘 호텔에 묵는 날일 확률", pr_two_pp_same_day
print "어느 특정한 날에 두 사람에 같은 호텔에 묵고 있을 확률", pr_two_pp_same_day * pr_hotel_choose
print "어느 특정한 '두개의 날' 에 두 사람이 같은 호텔에 묶고 있을 확률", (pr_two_pp_same_day * pr_hotel_choose) ** 2

print ""

print "The numbers of suspected pairs : ", float(num_case_evil)


