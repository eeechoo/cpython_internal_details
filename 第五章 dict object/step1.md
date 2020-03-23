### 入门阅读
- Raymond Hettinger(python core developer)（妙人）（这个人很会讲笑话）（入门必看视频）
 - https://www.youtube.com/watch?v=npw4s1QTmPg
 - https://www.youtube.com/watch?v=p33CVV29OG8
 - you can follow him on Twitter（https://twitter.com/raymondh）
 - 他讲课用的代码参见 step2.py

- Stack Overflow 关于 python 字典的问题
 https://stackoverflow.com/questions/39980323/are-dictionaries-ordered-in-python-3-6
 https://stackoverflow.com/questions/50872498/will-ordereddict-become-redundant-in-python-3-7



 ###  open address 处理 collide/conflict
给定一个 hashvalue  和 spacelength，将 hashvalue 映射到 0 到 spacelength-1 的空间中
```python
def gen_probe(hashvalue, mask):
    if hashvalue < 0:
        hashvalue = -hashvalue

    i = hashvalue & mask
    yield i

    while True:
      i = (5 * i + 1)
      yield i & mask

# 当 spacelength 是 2 的指数倍时，(这个是必须条件，否则不能遍历完整个空间)
# gen_probe 仅需一次就可以完成所有空间的遍历（incredible吧，数论就是这么神奇！）

# 代码验证如下
space_size = 2**10

s = set()
times = 0
for i in gen_probe(1111111111, space_size-1):
    print(i)
    times += 1
    if i not in s:
        s.add(i)
        if len(s) == space_size:
            break
print(times)
# 遍历 1024 大小的空间仅需要 执行1024次
```
that's not enough！！evolution to a stronger generator function！！！

```PYTHON
def gen_probe(hashvalue, mask):
    if hashvalue < 0:
        hashvalue = -hashvalue

    i = hashvalue & mask
    yield i

    PERTURB_SHIFT = 5
    perturb = hashvalue
    i = (5 * i + 1)
    while True:
      i = (5 * i + perturb + 1) & 0xFFFFFFFFFFFFFFFF
      yield i & mask
      perturb >>= PERTURB_SHIFT

# 这个函数遍历 1024 大小的空间需要 1034 次(更加难以置信了吧，没错！我看见这个函数也惊呆了(ｷ｀ﾟДﾟ´)!!)
```


