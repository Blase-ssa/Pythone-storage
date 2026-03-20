#!/usr/bin/env python3
"""Check if a given sting is a palindrome"""
import sys

def palindrome_loop(txt: str) -> bool:
    str_len = len(txt)
    j = str_len -1
    i = 0
    while i < j:
        while not txt[j].isalnum():
            j -= 1
        while not txt[i].isalnum():
            i += 1
        if j < i: break
        # print(txt[i].lower(), "!=", txt[j].lower(), "|| i =", i, "j =", j, ";") # debug data :)
        if txt[i].lower() != txt[j].lower():
            return False
        j -= 1
        i += 1
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv[1]) < 1:
        sys.exit("string not specified")
    if palindrome_loop(sys.argv[1]):
        sys.exit("Palindrome")
    sys.exit("Not a palindrome")
