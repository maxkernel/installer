import urwid, subprocess
from common import *


def option(opts, key):
	return opts[key] if key in opts else '?'

task = None

def makepage(opts, loop):
	global task
	
	args = {
		'I_TMPDIR': option(opts, 'installer.tmpdir'),
		'K_INSTALL': option(opts, 'kernel.install'),
		'K_MODEL': option(opts, 'kernel.model'),
		'S_LIST': option(opts, 'stitcher.list'),
		'M_LIST': option(opts, 'modules.list'),
	}
	
	text = urwid.Text('')
	task = Task(text, loop, 'generate', args)
	
	return [
		urwid.Text("Running task. This may take a while..."),
		urwid.Divider("-"),
		text,
	]

def teardown(opts, loop):
	global task
	
	return task.check()
