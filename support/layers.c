/*
__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-18"
*/

#include "common.h"


static PyObject *
merge_layers_overlay(PyObject *self, PyObject *args)
{
	PyObject *py_image_in1, *py_image_in2, *py_image_out;
	if (!PyArg_ParseTuple(args, "OOO", &py_image_in1, &py_image_in2,
			&py_image_out))
	{
		return Py_BuildValue("is", -1, "ERROR: Could not parse argument tuple.");
	}
	Imaging img_in1 = pyobject_to_imaging(py_image_in1);
	Imaging img_in2 = pyobject_to_imaging(py_image_in2);
	Imaging img_out = pyobject_to_imaging(py_image_out);
	int y, x;
	for (y = 0; y < img_out->ysize; y++)
	{
		UINT8* out = (UINT8*) img_out->image[y];
		UINT8* in1 = (UINT8*) img_in1->image[y];
		UINT8* in2 = (UINT8*) img_in2->image[y];
		for (x = 0; x < img_out->linesize; x++) {
			int val = (int) (in1[x] / 255.0 * (in1[x] + 2 * in2[x] / 255.0 * \
						(255 - in1[x])));
			if (val < 0)
				out[x] = 0;
			else if (val > 255)
				out[x] = 255;
			else
				out[x] = val;
		}
	}
	return Py_BuildValue("is", 0, "");
}


static PyObject *
merge_layers_soft_light(PyObject *self, PyObject *args)
{
	PyObject *py_image_in1, *py_image_in2, *py_image_out;
	if (!PyArg_ParseTuple(args, "OOO", &py_image_in1, &py_image_in2,
			&py_image_out))
	{
		return Py_BuildValue("is", -1, "ERROR: Could not parse argument tuple.");
	}
	Imaging img_in1 = pyobject_to_imaging(py_image_in1);
	Imaging img_in2 = pyobject_to_imaging(py_image_in2);
	Imaging img_out = pyobject_to_imaging(py_image_out);
	int y, x;
	for (y = 0; y < img_out->ysize; y++) {
		UINT8* out = (UINT8*) img_out->image[y];
		UINT8* in1 = (UINT8*) img_in1->image[y];
		UINT8* in2 = (UINT8*) img_in2->image[y];
		for (x = 0; x < img_out->linesize; x++) {
			int val = (in1[x] * in2[x] * (255 - in1[x]) + in2[x] * (655025 - \
						(255 - in1[x]) * (255 - in2[x]))) / 655025.0;
			if (val < 0)
				out[x] = 0;
			else if (val > 255)
				out[x] = 255;
			else
				out[x] = val;
		}
	}
	return Py_BuildValue("is", 0, "");
}


static PyMethodDef Photomagick[] = {
	{"merge_layers_overlay", merge_layers_overlay, 1,
			"merge_layers_overlay(image1, image2, image_out)"},
	{"merge_layers_soft_light", merge_layers_soft_light, 1,
			"merge_layers_soft_light(image1, image2, image_out)"},
	{NULL, NULL}
};


PyMODINIT_FUNC
init_layers(void)
{
	Py_InitModule("photomagick.support._layers", Photomagick);
}
