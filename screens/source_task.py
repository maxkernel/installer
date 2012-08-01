import urwid, subprocess
from common import *


defaults = {

}

def option(opts, key):
	return opts[key] if key in opts else defaults[key] if key in defaults else ''

task = None

def makepage(opts, loop):
	global task
	
	args = {
		'I_TMPDIR': option(opts, 'installer.tmpdir'),
		'I_KERNEL_SRC': option(opts, 'installer.kernel_src'),
		'I_STITCHER_SRC': option(opts, 'installer.stitcher_src'),
		'I_MODULES_SRC': option(opts, 'installer.modules_src'),
	}
	
	text = urwid.Text('')
	task = Task(text, loop, 'source', args)
	
	return [
		urwid.Text("Running task. This may take a while..."),
		urwid.Divider("-"),
		text,
	]

def teardown(opts, loop):
	global task
	
	return task.check()
