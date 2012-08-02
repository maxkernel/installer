import urwid, os.path
from common import *

defaults = {
	'stitcher.list':		'',
}

def option(opts, key):
	return opts[key] if key in opts else defaults[key] if key in defaults else ''


def makepage(opts, loop):
	
	list = [
		urwid.Text("Stitcher configuration - Select stitcher scripts you would like to install"),
		urwid.Divider(),
	]
	
	return list

def teardown(opts, loop):
	return ( True, '' )
