BINDIR = /usr/local/bin
ICON_PATH = /usr/share/icons
DESKTOP_DIR = /usr/share/applications

install:
	cp .icon/icon.png $(ICON_PATH)/pmcli.png
	cp src/main.py $(BINDIR)/pmcli
	chmod +x $(BINDIR)/pmcli
	pip install cryptography
	pip install terminaltables
	cp src/PasswdManager.desktop $(DESKTOP_DIR)/PasswdManager.desktop
	update-desktop-database

uninstall:
	rm -f $(BINDIR)/pmcli
	rm -f $(ICON_PATH)/pmcli.png
	rm -f $(DESKTOP_PATH)/PasswdManager.desktop
	rm -rf ~/.config/PasswdManager
