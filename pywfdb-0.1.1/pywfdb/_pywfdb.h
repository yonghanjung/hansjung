#ifdef __cplusplus
#define __PYX_EXTERN_C extern "C"
#else
#define __PYX_EXTERN_C extern
#endif
__PYX_EXTERN_C DL_IMPORT(PyTypeObject) RecordType;

struct PyRecord {
  PyObject_HEAD
  struct __pyx_vtabstruct_7_pywfdb_Record *__pyx_vtab;
  PyObject *init_record_name;
  PyObject *record;
  PyObject *basedir;
  int nsig;
  WFDB_Frequency frequency;
  PyObject *signal_names;
  WFDB_Siginfo (*siginfo);
};
__PYX_EXTERN_C DL_IMPORT(PyTypeObject) AnnotationType;

struct PyAnnotation {
  PyObject_HEAD
  PyObject *init_record_name;
  PyObject *record;
  PyObject *basedir;
  WFDB_Anninfo anninfo;
  PyObject *name;
};
PyMODINIT_FUNC init_pywfdb(void);
