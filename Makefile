SECTION="NetPing modules"
CATEGORY="Base"
TITLE="EPIC6 OWRT_Launcher"

PKG_NAME="OWRT_Notifications"
PKG_VERSION="Epic6.V1.S1"
PKG_RELEASE=1

MODULE_FILES=launcher.py
MODULE_FILES_DIR=/etc/init.d/

ETC_DIR=/etc/netping_launcher

.PHONY: all install

all: install

install:
	mkdir $(ETC_DIR)
	for f in $(MODULE_FILES); do cp $${f} $(MODULE_FILES_DIR); done
	mv $(MODULE_FILES_DIR)launcher.py $(MODULE_FILES_DIR)launcher
	cd /etc/rc.d
	ln -s ../init.d/launcher S90Launcher

clean:
	rm -rf $(ETC_DIR)
	rm /etc/rc.d/S90Launcher
	rm $(MODULE_FILES_DIR)launcher
