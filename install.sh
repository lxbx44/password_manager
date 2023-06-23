#!/bin/bash

echo "Installing requirements\n"
pip install -r requirements.txt

chmod +x main.py
mv main.py pm

clear
echo "Are you using zsh (1), bash (2), fish(3) or nu (4)"

curdir="${pwd}"

read -p ">> " input

if [ "$input" = "1" ]; then
    alias pm="${curdir}/$(basename "$0")"
    source ~/.zshrc

elif [ "$input" = "2" ]; then
    alias pm="${curdir}/$(basename "$0")"
    source ~/.bashrc

elif [ "$input" = "3" ]; then
    function pm { ${curdir}/$(basename "$0"); }
    source ~/.config/fish/config.fish

elif [ "$input" = "4" ]; then
    config set path \$nu.path \$nu.path:${curdir}
    echo "Restart your terminal"
fi


echo ""
echo "All done."
echo ""
echo "DO NOT DELETE THIS FOLDER"


