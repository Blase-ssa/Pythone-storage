#!/usr/bin/env python3
"""Check if a given sting is a palindrome"""
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("string not specified")
    
    if sys.argv[1] !=  sys.argv[1][::-1]:
        sys.exit("Not a palindrome")
    sys.exit("Palindrome")
