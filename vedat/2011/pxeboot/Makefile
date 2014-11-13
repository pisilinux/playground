CC = gcc
CFLAGS = -g -Wall `xml2-config --cflags`

LIBCURSES := -lncurses -lmenu `xml2-config --libs`

TARGETS = client/pxe_select_boot/pxebootselect

INITRAMFS = ` ls /boot | sort -r | grep -m 1 initramfs- `
VERSION = ` ls /boot | sort -r | grep -m 1 initramfs- | cut -c11- `
KERNEL = kernel-$(VERSION)
TFTPBOOT_PATH = /tftpboot/pts/latest-ptsp

all:
	$(CC) $(CFLAGS) client/pxe_select_boot/pxebootselect.c -o $(TARGETS) $(LIBCURSES)

clean:
	rm -f $(TARGETS)

configure:
	mkdir /tftpboot/pts/$(VERSION)-ptsp
	rm -rf $(TFTPBOOT_PATH)
	ln -s $(VERSION)-ptsp $(TFTPBOOT_PATH)
	
	mkdir $(TFTPBOOT_PATH)/pxelinux.cfg
	
	cd $(TFTPBOOT_PATH) 
	ln -s $(KERNEL) $(TFTPBOOT_PATH)/latestkernel
	ln -s $(INITRAMFS) $(TFTPBOOT_PATH)/latestinitramfs
	
	cp client/pxe_select_boot/pxebootselect /lib/initramfs
	python server/iso_to_xml.py /opt/ptsp
	python client/initramfs/mkinitramfs -o $(TFTPBOOT_PATH) --pxeboot --network -k $(VERSION)

uninstall:
	rm -f /lib/initramfs/pxebootselect
	rm -f /opt/ptsp/pxeboot_iso_files.xml
	rm -rf $(TFTPBOOT_PATH)
	rm -rf /tftpboot/pts/$(VERSION)-ptsp
	
install: configure
	cp client/initramfs/init /lib/initramfs
	
	cp pxelinux/pxelinux.cfg/default $(TFTPBOOT_PATH)/pxelinux.cfg/
	cp pxelinux/pxelinux.0 $(TFTPBOOT_PATH)
	cp /boot/$(KERNEL) $(TFTPBOOT_PATH)
