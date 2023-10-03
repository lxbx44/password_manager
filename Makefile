
BINDIR = /usr/local/bin
ICON_PATH = /usr/share/icons
DESKTOP_DIR = /usr/share/applications

install:
	cp .icon/icon.ico $(ICON_PATH)/pmcli.ico
	cp src/main.py $(BINDIR)/pmcli
	chmod +x $(BINDIR)/pmcli
	pip install -r src/requirements.txt
	cp src/PasswdManager.desktop $(DESKTOP_DIR)/PasswdManager.desktop
	update-desktop-database

uninstall:
	rm -f $(BINDIR)/pmcli
	rm -f $(ICON_PATH)/pmcli.ico
	rm -f $(DESKTOP_PATH)/PasswdManager.desktop
	rm -rf ~/.config/PasswdManager
