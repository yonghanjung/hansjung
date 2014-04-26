cdef extern from "Python.h":
    ctypedef long size_t 
    void* PyMem_Malloc(size_t n) 
    void PyMem_Free(void* mem) 
    object PyErr_NoMemory()
    object PyBool_FromLong(long)
    object PyString_FromString(char*)

    cdef struct _typeobject:
        pass
    cdef struct PyObject:
        _typeobject* ob_type

    int PyObject_AsReadBuffer(object, void **rbuf, int *len)
    int PyObject_AsWriteBuffer(object, void **rbuf, int *len)


    # list

    int PyList_Check(object p) 
    int PyList_CheckExact(object p) 
    object PyList_New( int len) 
    int PyList_Size(object list) 
    object PyList_GetItem(object list, int index) 
    int PyList_SetItem(object list, int index, PyObject* item) 
    int PyList_Append(object list, object item) 

    PyObject* PyFloat_FromDouble(double v) 

    PyObject* PyInt_FromLong(long v)

