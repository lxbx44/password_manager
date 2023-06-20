#!/usr/bin/bash

echo "Installing requirements\n"
pip install -r requirements.txt

chmod +x main.py
mv main.py pm

clear
echo "Are you using zsh (1), bash (2), fish(3) or nu (4)"

read -p ">> " input

if [ "$input" == "1" ]; then
    export PATH=".:$PATH"
elif [ "$input" == "2" ]; then
    export PATH=".:$PATH"
elif [ "$input" == "3" ]; then
    set -gx PATH . $PATH; source ~/.config/fish/config.fish
elif [ "$input" == "4" ]; then
    config set path $nu.path $nu.path:.
else
    true
fi

echo ""
echo "All done."
echo ""
echo "DO NOT DELETE THIS FOLDER"


