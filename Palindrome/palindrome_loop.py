#!/usr/bin/env python3
"""Check if a given sting is a palindrome"""
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("string not specified")
    
    str_len=len(sys.argv[1])
    for i in range(int(str_len/2)):
        if sys.argv[1][i] !=  sys.argv[1][-(i+1)]:
            sys.exit("Not a palindrome")
    sys.exit("Palindrome")
