# -*- coding: utf-8 -*-
"""
Licence and version informations.
"""

__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011-2012"
__version__ = "2012-04-14"


try:
	_('Photomagick')
except NameError:
	import gettext
	_ = gettext.gettext


SHORTNAME = 'photomagick'
NAME = _("Photomagick")
VERSION = '0.2'
VERSION_INFO = (0, 2, 0, 'beta', 0)
RELEASE = '2012-04-14'
DESCRIPTION = _('''Photomagick''')
DEVELOPERS = u'''Karol Będkowski'''
TRANSLATORS = u'''Karol Będkowski'''
COPYRIGHT = u"Copyright (c) Karol Będkowski, 2011-2012"
LICENSE = _('''\
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
''')


INFO = _("""\
%(name)s version %(version)s (%(release)s)
%(copyright)s

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

For details please see COPYING file.
""") % dict(name=NAME, version=VERSION, copyright=COPYRIGHT, release=RELEASE)
