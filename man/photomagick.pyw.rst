================
 photomagick.pyw
================

-----------------------------------
Photomagick
-----------------------------------

:Author: Karol Będkowski
:Date:   2011-04-27
:Copyright: Copyright(c) Karol Będkowski, 2011
:Version: 0.1
:Manual section: 1
:Manual group: Photomagick


SYNOPSIS
========

photomagick.pyw

DESCRIPTION
===========

Stupid, small application for modifying photos by apply pre-defined filters.


OPTIONS
=======

-d, --debug  Enable debug messages
-h, --help   Show help message and exit
--version    Show information about application version
-D, --debug_scripts   draw additional debug information when processing images
-F FILTER, --filter=FILTER  filter names (separate by ,) for batch processing
--list-filters  show available filters
-b, --batch     run batch processing
-v, --verbose   print more messages
-o OUTPUT, --output=OUTPUT    output directory for batch processed images
-p POSTFIX, --postfix=POSTFIX   output file name postfix for batch processed images


EXAMPLES
========

To run this program in GUI-mode (standard way) type:
   photomagick.pwd

For load on startup some images please append its names:
  photomagick.pyw image.jpg

Example use of batch processing:
  photomagick.pyw -b -F lomo,filmframe4x5 image.jpg


FILES
=======

~/.local/share/photomagick/filters/
    User filters

~/.config/photomagick/photomagick.cfg
    Application configuration file.
