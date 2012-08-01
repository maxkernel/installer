
FILE			=default.cfg
ARGS			=

I_TMPDIR		=/tmp/maxkernel-install
I_KERNEL_SRC	=file://${HOME}/kernel.tar.gz
I_STITCHER_SRC	=file://${HOME}/stitcher.tar.gz
I_MODULES_SRC	=file://${HOME}/modules.tar.gz


.PHONY: prepare all installer source clean

all: installer

installer:
	# Run the curses installer
	python installer.py $(ARGS) "$(FILE)"

source: prepare
	# Make temporary directory
	[ ! -d '$(I_TMPDIR)' ] || ( echo "Temporary directory $(I_TMPDIR) exists!" >>buildlog && cat buildlog && false )
	mkdir -p $(I_TMPDIR) $(I_TMPDIR)/kernel $(I_TMPDIR)/stitcher $(I_TMPDIR)/modules
	
	# Kernel (This may take a while)
	( echo "** This may take a while" && curl -LsS "$(I_KERNEL_SRC)" 2>>buildlog | tar -xz -C $(I_TMPDIR)/kernel --strip-components=1 2>>buildlog ) || ( cat buildlog && false )
	( cp -r $(I_TMPDIR)/kernel/modules/* $(I_TMPDIR)/modules ) || ( cat buildlog && false )
	( cp contrib/Makefile.nop $(I_TMPDIR)/kernel/modules/Makefile ) || ( cat buildlog && false )
	
	# Stitcher (This may take a while)
	( echo "** This may take a while" && $(foreach stitcher_src,$(I_STITCHER_SRC), curl -LsS "$(stitcher_src)" 2>>buildlog | tar -xz -C $(I_TMPDIR)/stitcher --strip-components=1 2>>buildlog &&) true ) || ( cat buildlog && false )
	
	# Modules (This may take a while)
	( echo "** This may take a while" && $(foreach modules_src,$(I_MODULES_SRC), curl -LsS "$(modules_src)" 2>>buildlog | tar -xz -C $(I_TMPDIR)/modules --strip-components=1 2>>buildlog &&) true ) || ( cat buildlog && false )
	( cp contrib/Makefile.modules $(I_TMPDIR)/modules/Makefile ) || ( cat buildlog && false )
	
	# Print success
	( echo "Done (success)" >>buildlog && cat buildlog )

clean:
	rm -rf $(I_TMPDIR)

prepare:
	# Prepare the log file
	echo "Installer log ==----------------------== [$(shell date)]" >buildlog

