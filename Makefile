SECTION="NetPing modules"
CATEGORY="Base"
TITLE="EPIC6 OWRT_Module_manager"

PKG_NAME="OWRT_Notifications"
PKG_VERSION="Epic6.V1.S1"
PKG_RELEASE=2

MODULE_FILES=launcher
MODULE_FILES_DIR=/etc/init.d/

ETC_FILES=launcher.py
ETC_DIR=/etc/netping_modulemanager

.PHONY: all install

all: install

install:
	mkdir $(ETC_DIR)
	for f in $(ETC_FILES); do cp $${f} $(ETC_DIR); done
	mkdir $(ETC_DIR)/modules
	for f in $(MODULE_FILES); do cp $${f} $(MODULE_FILES_DIR); done
	cd /etc/rc.d
	ln -s /etc/init.d/launcher /etc/rc.d/S90Launcher

clean:
	rm -rf $(ETC_DIR)
	rm /etc/rc.d/S90Launcher
	rm $(MODULE_FILES_DIR)launcher
