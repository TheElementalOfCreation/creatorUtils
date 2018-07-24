"""
This class is used for compatibility with python installations that do
not have the progressbar (or progressbar2 if using Python 3) module
installed. This does not actually implement a progress bar. All it does
is allow my scripts that use progress bars to function even without the
actual progressbar module.

This script will first check if it can find the progressbar module. If it
cannot, it will define the necessary classes.
"""
import sys;

try:
	from progressbar import *;
	__isRealProgressBar__ = True;
except:
	__isRealProgressBar__ = False;
	if sys.version_info[0] < 3:
		h = '';
	else:
		h = '2';
	print('Could not import progressbar{} module! Disabling progress bars...'.format(h));
	del h;

	class ProgressBar(object):
		def __init__(self, *args, **kwargs):
			object.__init__(self);
		def __call__(self, inp):
			return inp;
