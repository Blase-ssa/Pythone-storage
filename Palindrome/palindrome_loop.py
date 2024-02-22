#!/usr/bin/env python3
"""Check if a given sting is a palindrome"""
import sys


def palindrome_loop(txt: str) -> bool:
    str_len = len(txt)
    for i in range(int(str_len / 2)):
        if txt[i] != txt[-(i + 1)]:
            return False
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv[1]) < 1:
        sys.exit("string not specified")
    if palindrome_loop(sys.argv[1]):
        sys.exit("Palindrome")
    sys.exit("Not a palindrome")
