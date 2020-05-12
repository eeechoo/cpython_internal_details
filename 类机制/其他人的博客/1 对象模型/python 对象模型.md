

```python
>>> isinstance(a, A)
True
>>> isinstance(A, object)
True
>>> isinstance(a, object)
True
>>> isinstance(a, type)    # why??????????????????????
False

# isinstance 
# whether an object is an instance of a class or of a subclass thereof
# 调用了这个函数
# PyObject_IsInstance(PyObject *inst, PyObject *cls)
```





```c
// Objects/longobject.c

PyTypeObject PyLong_Type = {
    ……
    &long_as_number,                            /* tp_as_number */
    ……
};
 
static PyNumberMethods long_as_number = {
    (binaryfunc)long_add,       /*nb_add*/
    ……
};
```




```
[typeobject.c]
PyTypeObject PyType_Type = {
    ...
    sizeof(PyHeapTypeObject),                   /* tp_basicsize */
    ...
    0,                                          /* tp_richcompare */
}

#define TPSLOT(NAME, SLOT, FUNCTION, WRAPPER, DOC) \
    {NAME, offsetof(PyTypeObject, SLOT), (void *)(FUNCTION), WRAPPER, \
     PyDoc_STR(DOC)}

#define ETSLOT(NAME, SLOT, FUNCTION, WRAPPER, DOC) \
    {NAME, offsetof(PyHeapTypeObject, SLOT), (void *)(FUNCTION), WRAPPER, \
     PyDoc_STR(DOC)}

#define BINSLOT(NAME, SLOT, FUNCTION, DOC) \
    ETSLOT(NAME, as_number.SLOT, FUNCTION, wrap_binaryfunc_l, \
           NAME "($self, value, /)\n--\n\nReturn self" DOC "value.")

static slotdef slotdefs[] = {
    ...
    TPSLOT("__eq__", tp_richcompare, slot_tp_richcompare, richcmp_eq,
        "__eq__($self, value, /)\n--\n\nReturn self==value."),
    ...
    BINSLOT("__add__", nb_add, slot_nb_add,
        "+"),
    ...
}
```