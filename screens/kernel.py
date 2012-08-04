import urwid, os.path
from common import *

defaults = {
	'kernel.install':	'/usr/lib/maxkernel',
	'kernel.model':		'Robot',
}

def option(opts, key):
	return opts[key] if key in opts else defaults[key] if key in defaults else ''


def makepage(opts, objs, loop):
	
	install_dir		= text_new("Install Directory:     ", 'kernel.install', opts, option)
	model_name 		= text_new("Robot model:           ", 'kernel.model', opts, option)
	
	return [
		urwid.Text("Kernel configuration - Information related to the kernel?"),
		urwid.Divider(),
		
		install_dir['ui'],
		model_name['ui'],
	]

def teardown(opts, objs, loop):
	install_dir = option(opts, 'kernel.install')
	model_name = option(opts, 'kernel.model')
	
	if os.path.exists(os.path.expandvars(install_dir)):
		return ( False, 'Installation directory already exists!' )
	
	return ( True, '' )
