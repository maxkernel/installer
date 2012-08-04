import urwid, shlex
from common import *

defaults = {
	'installer.tmpdir':		'/tmp/maxkernel-install',
	'stitcher.list':		'',
	'stitcher.config':		'',
}

def option(opts, key):
	return opts[key] if key in opts else defaults[key] if key in defaults else ''


def makepage(opts, objs, loop):
	configs = dict()
	
	toks = [t for t in shlex.shlex(option(opts, 'stitcher.config'))]
	for i in range(len(toks))[::-1]:
		if toks[i] in ('.',):
			toks[i-1] = ''.join(toks[i-1:i+2])
			del toks[i:i+2]
	
	for i in range(0, len(toks), 5):
		if toks[i+1] != ':' or toks[i+3] != '=':
			continue
		configs[''.join(toks[i+0:i+3])] = toks[i+4]
	
	
	objs['stitcher2'] = []
	
	prefix = option(opts, 'installer.tmpdir') + '/stitcher/'
	for name in option(opts, 'stitcher.list').split(' '):
		obj = dict()
		obj['name'] = name
		obj['path'] = prefix + name
		obj['info'] = stitcher_lua_info(obj['path'])
		
		
		for config in obj['info']['configuration']:
			key = ''.join([ obj['name'], ':', config['name'] ])
			config['modified'] = key in configs
			config['value'] = configs.get(key, config['value'])
		
		objs['stitcher2'].append(obj)
	
	
	items = [
		urwid.Text("Stitcher configuration - Configure the stitcher scripts you selected"),
		urwid.Divider(),
	]
	
	for obj in objs['stitcher2']:
		subitems = [ urwid.Text(obj['name'] + '  - ' + obj['info']['description']) ]
		
		for config in obj['info']['configuration']:
			def text_onchange(text, new_txt, userdata):
				userdata['value'] = new_txt
				userdata['modified'] = True
			
			edit = urwid.Edit("     %-25s= " %(config['name']), config['value'])
			urwid.connect_signal(edit, 'change', text_onchange, config)
			
			subitems.append(urwid.AttrWrap(urwid.Columns([
				edit,
				urwid.Text(config['documentation']),
			]), 'edit', 'edit active'))
		
		items.append(urwid.LineBox(urwid.Pile(subitems)))
	
	return items

def teardown(opts, objs, loop):
	configs = ''
	for obj in objs['stitcher2']:
		for config in obj['info']['configuration']:
			if config['modified']:
				configs = ' '.join([ configs, ''.join([ obj['name'], ':', config['name'], '=', config['value'] ]) ])
	
	opts['stitcher.config'] = configs.strip()
	return ( True, '' )
