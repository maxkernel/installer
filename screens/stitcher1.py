import urwid, os
from common import *

defaults = {
	'installer.tmpdir':		'/tmp/maxkernel-install',
	'stitcher.list':		'',
}

def option(opts, key):
	return opts[key] if key in opts else defaults[key] if key in defaults else ''


def makepage(opts, objs, loop):
	objs['stitcher1'] = []

	prefix = option(opts, 'installer.tmpdir') + '/stitcher/'
	for name in os.listdir(prefix):
		if True not in (name.endswith('.lua'),):
			continue
		
		obj = dict()
		obj['name'] = name
		obj['path'] = prefix + name
		obj['checked'] = obj['name'] in option(opts, 'stitcher.list').split(' ')
		obj['info'] = stitcher_lua_info(obj['path'])
		objs['stitcher1'].append(obj)
	
	items = [
		urwid.Text("Stitcher selection - Select stitcher scripts you would like to install"),
		urwid.Divider(),
	]
	
	for obj in objs['stitcher1']:
		def check_onchange(text, new_state, userdata):
			userdata['checked'] = new_state
		
		title = urwid.CheckBox(obj['name'], obj['checked'])
		urwid.connect_signal(title, 'change', check_onchange, obj)
		
		items.append(urwid.AttrWrap(urwid.Columns([
			title,
			urwid.Text(' - ' + obj['info']['description']),
		]), 'check', 'check active'))
	
	return items

def teardown(opts, objs, loop):
	list = ''
	for obj in objs['stitcher1']:
		if obj['checked'] is True:
			list = ' '.join([ list, obj['name'] ])
	
	opts['stitcher.list'] = list.strip()
	return ( True, '' )
