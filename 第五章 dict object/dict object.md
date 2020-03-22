








1. 定义空间
typedef struct _object {
    _PyObject_HEAD_EXTRA
    Py_ssize_t ob_refcnt;
    struct _typeobject *ob_type;
} PyObject;

typedef struct {
    PyObject ob_base;
    Py_ssize_t ob_size; /* Number of items in variable part */
} PyVarObject;

#define PyObject_VAR_HEAD      PyVarObject ob_base;
typedef struct _typeobject {
typedef struct _typeobject PyTypeObject;


2. 第一次填充
PyTypeObject PyType_Type = {


#define PyObject_HEAD_INIT(type)        \
    { _PyObject_EXTRA_INIT              \
    1, type },
#define PyVarObject_HEAD_INIT(type, size)       \
    { PyObject_HEAD_INIT(type) size },


3. 第二次填充
PyStatus
_PyTypes_Init(void)


int
PyType_Ready(PyTypeObject *type)


#define _PyVarObject_CAST(op) ((PyVarObject*)(op))
#define Py_TYPE(ob)             (_PyObject_CAST(ob)->ob_type)
