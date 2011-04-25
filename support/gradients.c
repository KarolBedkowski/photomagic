/*
__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-18"
*/


#include "common.h"


static PyObject *
create_gradient(PyObject *self, PyObject *args)
{
	PyObject *py_image_in;
	double size, offset, center_w, center_h;
	if (!PyArg_ParseTuple(args, "Odddd", &py_image_in, &size, &offset,
			&center_w, &center_h))
	{
		return Py_BuildValue("is", -1, "ERROR: Could not parse argument tuple.");
	}
	// create gradient
	if (offset <= 0)
		offset = 1.0;
	int colors[256];
	int c;
	if (offset == 1)
	{
		for (c=0; c<256; c++)
			colors[c] = 255 - c;
	}
	else
	{
		for (c=0; c<256; c++)
			colors[c] = 255 - pow(c / 255.0, offset) * 255;
	}
	Imaging img_in = pyobject_to_imaging(py_image_in);
	int y, x;
	double dist;
	int center_x = img_in->xsize * val01(center_w);
	int center_y = img_in->ysize * val01(center_h);
	double step = 2.0 / (MAX(img_in->xsize, img_in->ysize) * size);
	for (y = 0; y < img_in->ysize; y++)
	{
		RGBA* in = (RGBA*) img_in->image[y];
		for (x = 0; x < img_in->xsize; x++, in++)
		{
			dist = sqrt((x - center_x) * (x - center_x) + \
					(y - center_y) * (y - center_y));
			int color = colors[f2i256(step * dist)];
			in->red = color;
			in->green = color;
			in->blue = color;
		}
	}
	return Py_BuildValue("is", 0, "");
}



static PyMethodDef Photomagick[] = {
	{"create_gradient", create_gradient, 1,
			"create_gradient(image, size, offset, center_w, center_h)"},
	{NULL, NULL}
};


PyMODINIT_FUNC
init_gradients(void)
{
	srand((unsigned) time(NULL));
	Py_InitModule("photomagick.support._gradients", Photomagick);
}
