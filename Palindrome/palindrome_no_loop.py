#!/usr/bin/env python3
"""Check if a given sting is a palindrome"""
import sys


def palindrome_no_loop(txt: str) -> bool:
    return txt == txt[::-1]


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv[1]) < 1:
        sys.exit("string not specified")
    if palindrome_no_loop(sys.argv[1]):
        sys.exit("Palindrome")
    sys.exit("Not a palindrome")
