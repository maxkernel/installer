#!/usr/bin/python

import sys, getopt, ConfigParser, urwid

sys.path.append("screens")

options = [
	'installer.cfgfile',
	'installer.download',
	'installer.kernel_src',
	'installer.stitcher_src',
	'installer.modules_src',
	
	'kernel.install'
]

class InstallerFrame(urwid.Frame):
	def keypress(self, size, key):
		if key == 'tab':
			self.set_focus('body' if self.focus_part == 'footer' else 'footer')
		return self.__super.keypress(size, key)

class Installer:
	screens = [
		'welcome',
		'source'
	]
	
	palette = [
		('header',		'white,bold',	'dark red',		''),
		('body',		'white',		'dark blue',	''),
		('footer',		'white',		'dark blue',	'standout'),
		
		('button',		'black',		'light gray',	'standout'),
		('button active','black',		'white',		'standout'),
		('check',		'white',		'dark blue'),
		('check active',	'white',	'light blue',	'bold'),
		('edit',		'white',		'dark blue'),
		('edit active',	'white',		'light blue',	'bold'),
	]
	
	def __init__(self, opts):
		self.opts = opts
		self.body = []
		
		# Import the screens
		self.pages = []
		self.onpage = 0
		for s in self.screens:
			self.pages.append(__import__(s))
		
		# Create the layout
		header = urwid.Text("  MaxKernel installer  ")
		body = urwid.ListBox(self.body)
		footer = urwid.GridFlow(
			[
				urwid.AttrWrap(urwid.Button("Previous", on_press=lambda b: self.show(self.onpage - 1)), 'button', 'button active'),
				urwid.AttrWrap(urwid.Button("Next", on_press=lambda b: self.show(self.onpage + 1)), 'button', 'button active')
			], 15, 2, 0, 'right'
		)
		footer.set_focus(1);
		
		self.frame = InstallerFrame(
			urwid.AttrWrap(urwid.LineBox(body), 'body'),
			urwid.AttrWrap(urwid.LineBox(header), 'header'),
			urwid.AttrWrap(urwid.LineBox(footer), 'footer'),
			focus_part='footer'
		)
		self.loop = urwid.MainLoop(self.frame, self.palette, unhandled_input=self.unhandled_input)
		self.show(0)
	
	def show(self, page):
		self.onpage = sorted((0, page, len(self.pages)))[1]		# Clamp page between 0 - len(pages)
		if self.onpage == len(self.pages):
			raise urwid.ExitMainLoop()
		self.body[:] = self.pages[self.onpage].makepage(self.opts)
		self.frame.set_focus('body')
	
	def unhandled_input(self, input):
		if input == 'esc':
			raise urwid.ExitMainLoop()
	
	def main(self):
		self.loop.run()
		print(self.opts)

def warning(msg):
	print >> sys.stderr, "** Warning:", msg
	
def fatal(msg):
	print >> sys.stderr, "** Fatal error:", msg
	sys.exit(1)

def main(opts, args):
	if len(args) not in (0, 1):
		fatal("Configuration file is only optional argument")
	
	cfgfile = args[0] if len(args) > 0 else ''
	if cfgfile != '':
		try:
			fp = open(cfgfile, 'r')
			
			parser = ConfigParser.ConfigParser()
			parser.readfp(fp)
			
			installer_items = map(lambda t: ('installer.'+t[0], t[1]), parser.items('installer') if parser.has_section('installer') else [])
			kernel_items = map(lambda t: ('kernel.'+t[0], t[1]), parser.items('kernel') if parser.has_section('kernel') else [])
			modules_items = map(lambda t: ('modules.'+t[0], t[1]),parser.items('modules') if parser.has_section('modules') else [])
			stitcher_items = map(lambda t: ('stitcher.'+t[0], t[1]),parser.items('stitcher') if parser.has_section('stitcher') else [])
			
			opts = dict(installer_items + kernel_items + modules_items + stitcher_items + opts.items())
			
			fp.close()
		except IOError as err:
			fatal("Could not open configuration file: %s" %(err))
	
	if 'installer.cfgfile' not in opts:
		opts['installer.cfgfile'] = cfgfile
	
	for k, v in opts.items():
		if k not in options:
			warning("Unknown option %s = %s: Ignoring!" %(k, v))
	
	Installer(opts).main()

if __name__ == "__main__":
	try:
		opts, args = getopt.getopt(sys.argv[1:], '', map(lambda v: v+'=', options))
		opts = dict(map(lambda t: (t[0][2:], t[1]), opts))
	except getopt.GetoptError as err:
		fatal("Could not parse command line options: %s" %(err))
	
	main(opts, args)
