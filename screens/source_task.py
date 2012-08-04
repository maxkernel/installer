import urwid, subprocess
from common import *


def option(opts, key):
	return opts[key] if key in opts else '?'


def makepage(opts, objs, loop):
	args = {
		'I_TMPDIR': option(opts, 'installer.tmpdir'),
		'I_KERNEL_SRC': option(opts, 'installer.kernel_src'),
		'I_STITCHER_SRC': option(opts, 'installer.stitcher_src'),
		'I_MODULES_SRC': option(opts, 'installer.modules_src'),
	}
	
	text = urwid.Text('')
	objs['source_task'] = Task(text, loop, 'source', args)
	
	return [
		urwid.Text("Running task. This may take a while..."),
		urwid.Divider("-"),
		text,
	]

def teardown(opts, objs, loop):
	return objs['source_task'].check()
