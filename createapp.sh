#!/bin/bash

APP_NAME="PasswdManager"
EXECUTABLE="pmcli"

DESKTOP_DIR="/usr/share/applications/"

CUR_ICON=".icon/icon.ico"
ICON_PATH="/usr/share/icons/pmcli.ico"

DESKTOP_CONTENT="[Desktop Entry]\nName=${APP_NAME}\nExec=${EXECUTABLE}\nIcon=${ICON_PATH}\nTerminal=true\nType=Application\nCategories=Utility;"

DESKTOP_FILE="${DESKTOP_DIR}${APP_NAME}.desktop"

if [ -e "${DESKTOP_FILE}" ]; then
  echo "The .desktop file already exists: ${DESKTOP_FILE}\nUpdating file"
  sudo rm ${DESKTOP_FILE}
fi

sudo mv ${CUR_ICON} ${ICON_PATH}

echo -e "${DESKTOP_CONTENT}" | sudo tee "${DESKTOP_FILE}" > /dev/null

sudo update-desktop-database

echo "The .desktop file has been created: ${DESKTOP_FILE}"
echo "You can now launch your app with Rofi or Wofi by typing '${APP_NAME}'."
