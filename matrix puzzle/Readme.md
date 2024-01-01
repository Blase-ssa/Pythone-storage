Write an efficient algorithm that searches for a value target in an m x n integer matrix matrix. This matrix has the following properties:

    Integers in each row are sorted in ascending from left to right.
    Integers in each column are sorted in ascending from top to bottom.

## Example 1

matrix:
|   |   |   |   |   |
|---|---|---|---|---|
| 1 | 4 | 7 | 11| 15|
| 2 | 5 | 8 | 12| 19|
| 3 | 6 | 9 | 16| 22|
| 10| 13| 14| 17| 24|
| 18| 21| 23| 26| 30|

target = 5

## Example 2

matrix:
|   |   |   |   |   |
|---|---|---|---|---|
| 1 | 4 | 7 | 11| 15|
| 2 | 5 | 8 | 12| 19|
| 3 | 6 | 9 | 16| 22|
| 10| 13| 14| 17| 24|
| 18| 21| 23| 26| 30|

target = 20

## Example 3

matrix:
|   |   |   |   |   |
|---|---|---|---|---|
| 1 | 2 | 5 | 10| 17|
| 3 | 4 | 8 | 14| 22|
| 6 | 7 | 9 | 15| 23|
| 11| 12| 13| 16| 24|
| 18| 19| 20| 21| 25|

target = 15