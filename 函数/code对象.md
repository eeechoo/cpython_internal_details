1. Python 字节码入门

https://zhuanlan.zhihu.com/p/38194734

笔记：
```
def fib(n):
    if n < 2:
        return n
    current, next = 0, 1
    while n:
        current, next = next, current + next
        n -= 1
    return current

>>>fib.__code__.co_consts
(None, 2, (0, 1), 1)
>>>fib.__code__.co_varnames # local variable names
('n', 'current', 'next')
>>>fib.__code__.co_names  # nonlocal variable names
()

>>>fib.__code__.co_code
b'|\x00d\x01k\x00r\x0c|\x00S\x00d\x02\\\x02}\x01}\x02|\x00r0|\x02|\x01|\x02\x17\x00\x02\x00}\x01}\x02|\x00d\x038\x00}\x00q\x14|\x01S\x00'
>>>import dis
>>>dis.dis(fib)
  2           0 LOAD_FAST                0 (n)
              2 LOAD_CONST               1 (2)
              4 COMPARE_OP               0 (<)
              6 POP_JUMP_IF_FALSE       12
  3           8 LOAD_FAST                0 (n)
             10 RETURN_VALUE
  4     >>   12 LOAD_CONST               2 ((0, 1))
             14 UNPACK_SEQUENCE          2
             16 STORE_FAST               1 (current)
             18 STORE_FAST               2 (next)
  5     >>   20 LOAD_FAST                0 (n)
             22 POP_JUMP_IF_FALSE       48
  6          24 LOAD_FAST                2 (next)
             26 LOAD_FAST                1 (current)
             28 LOAD_FAST                2 (next)
             30 BINARY_ADD
             32 ROT_TWO
             34 STORE_FAST               1 (current)
             36 STORE_FAST               2 (next)
  7          38 LOAD_FAST                0 (n)
             40 LOAD_CONST               3 (1)
             42 INPLACE_SUBTRACT
             44 STORE_FAST               0 (n)
             46 JUMP_ABSOLUTE           20
  8     >>   48 LOAD_FAST                1 (current)
             50 RETURN_VALUE

```


https://docs.python.org/3/library/dis.html

对应 cpython/Python/ceval.c         1325 行
这里是 python 虚拟机



LOAD_CONST >LOAD_FAST > LOAD_NAME or LOAD_GLOBAL


https://zhuanlan.zhihu.com/p/39259061