/*
__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-04-18"
*/

#include "common.h"


static void
hls2rgb(double hue, double lightness, double saturation, double *red,
		double *green, double *blue)
{
	*red = 0.0;
	*green = 0.0;
	*blue = 0.0;
	double v = (lightness <= 0.5) ? (lightness * (1.0 + saturation)) : \
			(lightness + saturation - lightness * saturation);
	if (v > 0.0)
	{
		double m = lightness + lightness - v;
		hue *= 6.0;
		int sextant = (int) hue;
		double vsf = (v - m) * (hue - sextant);
		double mid1 = m + vsf;
		double mid2 = v - vsf;
		switch (sextant)
		{
			case 0:
				*red = v;
				*green = mid1;
				*blue = m;
				break;
			case 1:
				*red = mid2;
				*green = v;
				*blue = m;
				break;
			case 2:
				*red = m;
				*green = v;
				*blue = mid1;
				break;
			case 3:
				*red = m;
				*green = mid2;
				*blue = v;
				break;
			case 4:
				*red = mid1;
				*green = m;
				*blue = v;
				break;
			case 5:
				*red = v;
				*green = m;
				*blue = mid2;
				break;
		}
	}
}


static void
rgb2hls(double red, double green, double blue, double *hue,
		double *lightness, double *saturation)
{
	double v, m;
	*hue = 0;
	*saturation = 0;
	*lightness = 0;
	v = MAX(red, green);
	v = MAX(v, blue);
	m = MIN(red, green);
	m = MIN(m, blue);
	*lightness = (m + v) / 2.0;
	if (*lightness <= 0.0)
		return;
	double vm = v - m;
	if (vm <= 0.0)
		return;
	*saturation = vm / (((*lightness) <= 0.5) ? (v + m) : (2.0 - v - m));
	double r2 = (v - red) / vm;
	double g2 = (v - green) / vm;
	double b2 = (v - blue) / vm;
	if (red == v)
		*hue = ((green == m) ? 5.0 + b2 : 1.0 - g2) / 6.0;
	else if (green == v)
		*hue = ((blue == m) ? 1.0 + r2 : 3.0 - b2) / 6.0;
	else
		*hue = ((red == m) ? 3.0 + g2 : 5.0 - r2) / 6.0;
	if (*hue == 1.0)
		*hue = 0.0;
}


static PyObject *
apply_hue_lightness_saturation(PyObject *self, PyObject *args)
{
	PyObject *py_image_in, *py_image_out;
	double hue, lightness, saturation;
	int keep_luminance;
	if (!PyArg_ParseTuple(args, "OOdddi", &py_image_in, &py_image_out, &hue,
			&lightness, &saturation, &keep_luminance))
	{
		return Py_BuildValue("is", -1, "ERROR: Could not parse argument tuple.");
	}
	Imaging img_in = pyobject_to_imaging(py_image_in);
	Imaging img_out = pyobject_to_imaging(py_image_out);
	int y, x;
	double h, l, s;
	double fr, fg, fb;
	for (y = 0; y < img_out->ysize; y++)
	{
		RGBA* in = (RGBA*) img_in->image[y];
		RGBA* out = (RGBA*) img_out->image[y];
		for (x = 0; x < img_out->xsize; x++, in++, out++)
		{
			rgb2hls(in->red / 255.0, in->green / 255.0, in->blue / 255.0,
					&h, &l, &s);
			h += hue;
			if (h > 1.0)
				h -= 1.0;
			else if (h < 0.0)
				h += 1.0;
			s = val01(s + saturation);
			if (!keep_luminance)
				l = val01(l + lightness);
			hls2rgb(h, l, s, &fr, &fg, &fb);
			out->red = f2i256(fr);
			out->green = f2i256(fg);
			out->blue = f2i256(fb);
			out->alpha = in->alpha;
		}
	}
	return Py_BuildValue("is", 0, "");
}


static PyObject *
create_hls_noise(PyObject *self, PyObject *args)
{
	PyObject *py_image_in;
	double hue, lightness, saturation;
	if (!PyArg_ParseTuple(args, "Oddd", &py_image_in, &hue, &lightness,
			&saturation))
	{
		return Py_BuildValue("is", -1, "ERROR: Could not parse argument tuple.");
	}
	Imaging img_in = pyobject_to_imaging(py_image_in);
	int y, x;
	double h, l, s;
	double r, g, b;
	for (y = 0; y < img_in->ysize; y++)
	{
		RGBA* in = (RGBA*) img_in->image[y];
		for (x = 0; x < img_in->xsize; x++, in++)
		{
			h = hue * rand() / RAND_MAX;
			l = lightness * rand() / RAND_MAX;
			s = saturation * rand() / RAND_MAX;
			hls2rgb(h, l, s, &r, &g, &b);
			in->red = f2i256(r);
			in->green = f2i256(g);
			in->blue = f2i256(b);
		}
	}
	return Py_BuildValue("is", 0, "");
}



static PyMethodDef Photomagick[] = {
	{"apply_hue_lightness_saturation", apply_hue_lightness_saturation, 1,
			"apply_hue_lightness_saturation(image1, imagrOut, hue, lightness, "
			"saturation, keep_luminance)"},
	{"create_hls_noise", create_hls_noise, 1,
			"create_hls_noise(image, hue, lightness, saturation)"},
	{NULL, NULL}
};


PyMODINIT_FUNC
init_colors(void)
{
	srand((unsigned) time(NULL));
	Py_InitModule("photomagick.support._colors", Photomagick);
}
