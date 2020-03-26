#!/usr/bin/env python

import sys
import getopt
import time

def is_palindrome(number):
    s = 0
    r_num = number
    while r_num != 0:
        mod = r_num % 10
        s = s * 10 + mod
        r_num = r_num // 10
    return s == number

def palindromes(p_start, p_end):
    p = []
    for n in range(p_start, p_end+1):
        if is_palindrome(n):
            p.append(n)
            time.sleep(0.1)
    return p

def main():
    p_start = 0
    p_end = 0
    first = False
    second = False

    print(sys.argv)

    long_opts = ['first', 'second', 'start=', 'end=']
    opts, args = getopt.getopt(sys.argv[1:], '', long_opts)
    for o, a in opts:
        if o == '--first':
            first = True
        elif o == '--second':
            second = True
        elif o == '--start':
            p_start = int(a)
        elif o == '--end':
            p_end = int(a)

    if first:
        p_end = (p_start + p_end) // 2
        depvar_name = 'JSUB_DEPVAR_pal_first'
    elif second:
        p_start = (p_start + p_end) // 2 + 1
        depvar_name = 'JSUB_DEPVAR_pal_second'
    else:
        depvar_name = 'JSUB_DEPVAR_pal'

    print(p_start, p_end)

    pals = palindromes(p_start, p_end)
    pals_str = ''
    for pal in pals:
        pals_str += ' %s' % pal

    print(pals)
    print('%s=%s' % (depvar_name, pals_str))
    return 0

if __name__ == '__main__':
    sys.exit(main())
