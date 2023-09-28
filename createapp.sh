#!/bin/bash

APP_NAME="PMCLI"
EXECUTABLE="pmcli"

DESKTOP_DIR="/usr/share/applications/"

DESKTOP_CONTENT="[Desktop Entry]\nName=${APP_NAME}\nExec=${EXECUTABLE}\nTerminal=true\nType=Application\nCategories=Utility;"

DESKTOP_FILE="${DESKTOP_DIR}${APP_NAME}.desktop"

if [ -e "${DESKTOP_FILE}" ]; then
  echo "The .desktop file already exists: ${DESKTOP_FILE}"
else
  echo -e "${DESKTOP_CONTENT}" | sudo tee "${DESKTOP_FILE}" > /dev/null

  sudo update-desktop-database

  echo "The .desktop file has been created: ${DESKTOP_FILE}"
  echo "You can now launch your app with Rofi or Wofi by typing '${APP_NAME}'."
fi
