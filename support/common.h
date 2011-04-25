/*
__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-18"
*/

#ifndef __common_h__
#define __common_h__

#include "Python.h"
#include "ImPlatform.h"
#include "Imaging.h"

typedef struct
{
	UINT8 red;
	UINT8 green;
	UINT8 blue;
	UINT8 alpha;
} RGBA;


#define MAX(x, y) (((x) > (y)) ? (x) : (y))
#define MIN(x, y) (((x) < (y)) ? (x) : (y))


inline
int f2i256(double input);

inline
double val01(double input);

Imaging
pyobject_to_imaging(PyObject *imgobj);


#endif
