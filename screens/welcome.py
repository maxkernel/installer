import urwid

def makepage(opts):
	info = """
Welcome to the MaxKernel installer script
----------------------------------------------------------------------------

This script enables simple and easy installation of MaxKernel on a target
platform, whether that platform be local to this machine, or remote on a
separate machine.


To navigate this wizard, use these keys:

    TAB         - Switch between the content frame and the NEXT/PREV buttons
    UP/DOWN     - Move focus between inputs
    LEFT/RIGHT  - Move focus between buttons
    SPACE       - Select the button or checkbox
    ESC         - Quit this wizard



The steps covered in this wizard are as follows:

    1.  Locate the source code for the kernel
    2.  Choose appropriate stitcher scripts
    3.  Choose appropriate modules
    4.  Create deployable source bundle
    5.  Optional - Compile and/or deploy to remote



Questions about these steps and problems encountered can be emailed to
andrew@maxkernel.com
"""
	return [ urwid.Text(info) ]
