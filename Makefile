BINDIR = /usr/local/bin
ICON_PATH = /usr/share/icons
DESKTOP_DIR = /usr/share/applications

install:
	sudo cp .icon/icon.png $(ICON_PATH)/pmcli.png
	sudo cp src/main.py $(BINDIR)/pmcli
	sudo chmod +x $(BINDIR)/pmcli
	pip install cryptography
	pip install terminaltables
	sudo cp src/PasswdManager.desktop $(DESKTOP_DIR)/PasswdManager.desktop
	sudo update-desktop-database

uninstall:
	sudo rm -f $(BINDIR)/pmcli
	sudo rm -f $(ICON_PATH)/pmcli.png
	sudo rm -f $(DESKTOP_PATH)/PasswdManager.desktop
	sudo rm -rf ~/.config/PasswdManager
