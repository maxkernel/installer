import urwid, os.path
from common import *

defaults = {
	'modules.core':		'console service discovery httpserver netui',
	'modules.list':		'',
}

def option(opts, key):
	return opts[key] if key in opts else defaults[key] if key in defaults else ''


def makepage(opts, objs, loop):
	
	list = [
		urwid.Text("Modules configuration - Select optional modules you would like to install"),
		urwid.Text("Note: These pre-selected modules are required and driven based on your stitcher script selection"),
		urwid.Divider(),
		
	]
	
	return list

def teardown(opts, objs, loop):
	return ( True, '' )
