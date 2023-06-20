#!/bin/bash

chmod +x install.sh

sed -i '/export PATH=".:$PATH" && source ~\/.zshrc/d' ~/.zshrc
sed -i '/export PATH=".:$PATH" && source ~\/bashrc/d' ~/bashrc
sed -i '/set -gx PATH . $PATH; source ~\/.config\/fish\/config.fish/d' ~/.config/fish/config.fish
sed -i '/config set path $nu.path $nu.path:./d' ~/.config/nu/config.toml

git pull --force

bash install.sh

clear
