/*
__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-18"
*/


#include "common.h"


	inline
int f2i256(double input)
{
	if (input < 0.0)
		return 0;
	if (input > 1.0)
		return 255;
	return (int) (input * 255);
}


inline
double val01(double input)
{
	if (input < 0.0)
		return 0.0;
	if (input > 1.0)
		return 1.0;
	return input;
}


Imaging
pyobject_to_imaging(PyObject *imgobj) {
	PyObject *im = PyObject_GetAttrString(imgobj, "im");
	if (!im)
		return NULL;
	PyObject *id = PyObject_GetAttrString(im, "id");
	Py_DECREF(im);
	if (!id)
		return NULL;
	Imaging image  = (Imaging) PyLong_AsLong(id);
	Py_DECREF(id);
	return image;
}
