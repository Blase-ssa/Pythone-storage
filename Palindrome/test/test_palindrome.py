#!/usr/bin/env python3
"""Unit tests for palindrome scripts"""
import pytest
import subprocess
import palindrome_loop
import palindrome_no_loop

TEST_DATA=[
    ("1", True),
    ("x", True),
    ("11", True),
    ("1x1", True),
    ("111 xxx 1?1 xxx 111", True),
    ("", True),
    ("12", False),
    ("1 ", False)
]

@pytest.mark.parametrize("text, result", TEST_DATA)
def test_answer_palindrome_loop_function(text, result):
    assert palindrome_loop.palindrome_loop(text) == result

@pytest.mark.parametrize("text, result", TEST_DATA)
def test_answer_palindrome_no_loop_function(text, result):
    assert palindrome_no_loop.palindrome_no_loop(text) == result

@pytest.mark.parametrize("text, state", TEST_DATA)
def test_answer_palindrome_loop(text, state):
    test_output="Not a palindrome"
    if state: test_output="Palindrome"
    if len(text) == 0: test_output="string not specified"
    result = subprocess.run(['python', 'palindrome_loop.py', f"{text}"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert result.stdout.decode('utf-8').strip() == test_output

@pytest.mark.parametrize("text, state", TEST_DATA)
def test_answer_palindrome_no_loop(text, state):
    test_output="Not a palindrome"
    if state: test_output="Palindrome"
    if len(text) == 0: test_output="string not specified"
    result = subprocess.run(['python', 'palindrome_no_loop.py', f"{text}"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    assert result.stdout.decode('utf-8').strip() == test_output