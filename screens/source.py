import urwid, os.path, urllib2
from common import *


defaults = {
	'installer.tmpdir':			'/tmp/maxkernel-install',
	'installer.kernel_src':		'file://${HOME}/kernel.tar.gz',
	'installer.stitcher_src':	'file://${HOME}/stitcher.tar.gz',
	'installer.modules_src':	'file://${HOME}/modules.tar.gz',
}

def option(opts, key):
	return opts[key] if key in opts else defaults[key] if key in defaults else ''


def makepage(opts, objs, loop):
	
	kernel_src   = text_new("Kernel Source:          ", 'installer.kernel_src', opts, option)
	stitcher_src = text_new("Stitcher Scripts:       ", 'installer.stitcher_src', opts, option)
	modules_src  = text_new("Module Sources:         ", 'installer.modules_src', opts, option)
	tmpdir       = text_new("Temporary Directory:    ", 'installer.tmpdir', opts, option)
	
	return [
		urwid.Text("Source code - Where is the source code located?"),
		urwid.Divider(),
		
		urwid.Text("Enter a URL (http://...) or filepath (file://...) to the TAR.GZ file containing the kernel:"),
		kernel_src['ui'],
		urwid.Divider(),
		
		urwid.Text("Enter space-separated URLs (http://...) and/or filepaths (file://...) to the TAR.GZ file containing the following:"),
		stitcher_src['ui'],
		modules_src['ui'],
		urwid.Divider(),
		
		urwid.Text("Enter a temporary path where maxkernel will be configured:"),
		tmpdir['ui'],
	]

def teardown(opts, objs, loop):
	kernel_path = option(opts, 'installer.kernel_src')
	stitcher_paths = option(opts, 'installer.stitcher_src').split(' ')
	modules_paths = option(opts, 'installer.modules_src').split(' ')
	tmpdir = option(opts, 'installer.tmpdir')
	
	b = Busy("Checking paths...", 45, 4, loop)
	def checkpath(name, path):
		if len(path) == 0:
			return ( False, 'No %s path given!' %(name) )
		
		try:
			code = urllib2.urlopen(os.path.expandvars(path), timeout=5).getcode()
			if code not in (None, 200):
				raise Exception('Could not locate file or contact server')
			
		except Exception as err:
			return ( False, '%s path error:\n%s' %(name, err) )
	try:
		checkpath('Kernel', kernel_path)
		for v in stitcher_paths:
			checkpath('Stitcher', v)
		for v in modules_paths:
			checkpath('Modules', v)
		
		if os.path.exists(os.path.expandvars(tmpdir)):
			return ( False, 'Temporary folder already exists' )
		
	finally:
		b.hide()
	
	return ( True, '' )
