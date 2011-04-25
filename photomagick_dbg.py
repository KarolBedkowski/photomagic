#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
"""
from __future__ import with_statement

__author__ = "Karol Będkowski"
__copyright__ = "Copyright (c) Karol Będkowski, 2011"
__version__ = "2011-03-20"

import sys
if '--profile' not in sys.argv:
	sys.argv.append('-d')


def _profile():
	''' profile app '''
	import cProfile
	print 'Profiling....'
	cProfile.run('from photomagick.main import main; main()', 'profile.tmp')
	import pstats
	import time
	with open('profile_result_%d.txt' % int(time.time()), 'w') as out:
		stat = pstats.Stats('profile.tmp', stream=out)
		#s.strip_dirs()
		stat.sort_stats('cumulative').print_stats('photomagick', 50)
		out.write('\n\n----------------------------\n\n')
		stat.sort_stats('time').print_stats('photomagick', 50)
		out.write('\n\n============================\n\n')
		stat.sort_stats('cumulative').print_stats('', 50)
		out.write('\n\n----------------------------\n\n')
		stat.sort_stats('time').print_stats('', 50)


def _memprofile():
	''' mem profile app '''
	from photomagick.main import main
	main()
	import gc
	gc.collect()
	while gc.collect() > 0:
		print 'collect'

	import objgraph
	objgraph.show_most_common_types(20)

	import pdb
	pdb.set_trace()


if '--profile' in sys.argv:
	sys.argv.remove('--profile')
	_profile()
elif '--memprofile' in sys.argv:
	sys.argv.remove('--memprofile')
	_memprofile()
elif '--version' in sys.argv:
	from photomagick import version
	print version.INFO
else:
	from photomagick.main import main
	main()
