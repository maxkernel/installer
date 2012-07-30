import urwid

defaults = {
    'installer.download':       'Yes',
    'installer.kernel_src':     '~/kernel.zip',
    'installer.stitcher_src':   '~/stitcher.zip',
    'installer.modules_src':    '~/modules.zip',
}

def option(opts, key):
    return opts[key] if key in opts else defaults[key] if key in defaults else ''

def parsebool(b):
    return b.lower() in ('yes', 'y', 'true', 't', '1')

def toggle_getwww(checkbox, new_state, opts):
    opts['installer.download'] = 'Yes' if new_state else 'No'

def text_setkey(text, new_txt, ud):
    ud.opts[ud.key] = new_txt

def makepage(opts):
    text = urwid.Text("Source code - Where is the source code located?")
    getwww = urwid.CheckBox(
        "Download files over internet? [Requires internet on this computer]",
        parsebool(option(opts, 'installer.download')),
        on_state_change=toggle_getwww, user_data=opts
    )
    
    src = urwid.Text("Enter a URL or File Path to the ZIP file containing the following:")
    
    kernel_src =   urwid.Edit("Kernel Source:       ", option(opts, 'installer.kernel_src'))
    stitcher_src = urwid.Edit("Stitcher Scripts:    ", option(opts, 'installer.stitcher_src'))
    modules_src =  urwid.Edit("Modules Source:      ", option(opts, 'installer.modules_src'))
    
    kernel_src.key = 'installer.kernel_src'
    stitcher_src.key = 'installer.stitcher_src'
    modules_src.key = 'installer.modules_src'
    
    kernel_src.opts = opts
    stitcher_src.opts = opts
    modules_src.opts = opts
    
    urwid.connect_signal(kernel_src, 'change', text_setkey, kernel_src)
    urwid.connect_signal(stitcher_src, 'change', text_setkey, stitcher_src)
    urwid.connect_signal(modules_src, 'change', text_setkey, modules_src)
    
    return [
        text,
        urwid.Divider(),
        urwid.AttrWrap(getwww, 'check', 'check active'),
        urwid.Divider(),
        src,
        urwid.AttrWrap(kernel_src, 'edit', 'edit active'),
        urwid.AttrWrap(stitcher_src, 'edit', 'edit active'),
        urwid.AttrWrap(modules_src, 'edit', 'edit active'),
    ]
