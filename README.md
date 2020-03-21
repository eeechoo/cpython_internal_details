# cpython_internal_details
学习笔记：记录 cpython 的内部实现细节，暂时只有中文版

## 第 2 章
- [Python 中的整数对象](#python-------)
  * [参考资料](#----)
    + [Python 源码剖析](#python-----)
    + [Cpython Internals](#cpython-internals)
  * [PyLongObject](#pylongobject)
  * [PyLong_Type](#pylong-type)
  * [Question：整数的加法是如何实现的呢](#question-------------)
  * [PyLongObject new 过程](#pylongobject-new---)
  * [Question: 为什么会出现如下情况](#question------------)
  * [Q：当我们执行 python 代码 ```a = 1234``` 时，cpython究竟做了什么工作？](#q-------python-------a---1234------cpython---------)
  * [Q: built-in function id()](#q--built-in-function-id--)
  * [Q: 'is' operator in python](#q---is--operator-in-python)
  * [Q:hashable immutable](#q-hashable-immutable)
  * [后续更新与反馈](#-------)
  * [后记](#--)

## 第 3 章：PyUnicodeObject
1. PyUnicodeObject 长什么样子
2. PyUnicodeObject 如何分配空间、初始化
3. 字符串 intern 机制
4. 0-127 字符 缓存机制
