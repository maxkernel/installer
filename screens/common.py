import urwid, subprocess


def parsebool(b):
    return b.lower() in ('yes', 'y', 'true', 't', '1')


def text_setkey(text, new_txt, userdata):
    userdata['opts'][userdata['key']] = new_txt

def text_new(caption, key, opts, option):
    txt = { 'key': key, 'opts': opts, 'edit': urwid.Edit(caption, option(opts, key)) }
    txt['ui'] = urwid.AttrWrap(txt['edit'], 'edit', 'edit active')
    urwid.connect_signal(txt['edit'], 'change', text_setkey, txt)
    return txt


def checkbox_setkey(text, new_state, userdata):
    userdata['opts'][userdata['key']] = 'Yes' if new_state else 'No'

def checkbox_new(caption, key, opts, option):
    cb = { 'key': key, 'opts': opts, 'checkbox': urwid.CheckBox(caption, parsebool(option(opts, key))) }
    cb['ui'] = urwid.AttrWrap(cb['checkbox'], 'check', 'check active')
    urwid.connect_signal(cb['checkbox'], 'change', checkbox_setkey, cb)
    return cb


class Busy:
    def __init__(self, text, width, height, loop):
        self.loop = loop
        self.parent = loop.widget
        self.text = urwid.Text('')
        
        frame = urwid.Frame(urwid.SolidFill(' '))
        frame.header = urwid.Padding(self.text, align='center')
        
        loop.widget = urwid.Overlay( urwid.AttrWrap(urwid.LineBox(frame), 'dialog'), loop.widget, 'center', width, 'middle', height)
        self.settext(text)
    
    def settext(self, text):
        self.text.set_text(text)
        self.redraw()
        
    def redraw(self):
        self.loop.draw_screen()
        
    def hide(self):
        self.loop.widget=self.parent
        self.redraw()

class Task:
    def __init__(self, textbox, loop, target, args):
        self.done = False
        self.textbox = textbox
        
        cmd = [ 'make', target ]
        for k, v in args.items():
            cmd.append('"'+k+'='+v+'"')
        pipe = subprocess.Popen(' '.join(cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout
        
        def task(loop, userdata):
            data = pipe.readline()
            if len(data) == 0:
                self.done = True
                return
            else:
                self._append(data)
                loop.set_alarm_in(0.03, task)
        
        loop.set_alarm_in(0.03, task)
    
    def _append(self, str):
        self.textbox.set_text(self.textbox.get_text()[0] + str)
    
    def check(self):
        if not self.done:
            return ( False, '' )
        
        success = 'Done (success)' in self.textbox.get_text()[0]
        return ( success, '' if success else 'Error occurred during execution' )
