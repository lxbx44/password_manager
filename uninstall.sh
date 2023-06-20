#!/bin/bash

# Remove 'pm' executable
rm pm

# Restore PATH modifications
sed -i '/export PATH=".:$PATH" && source ~\/.zshrc/d' ~/.zshrc
sed -i '/export PATH=".:$PATH" && source ~\/bashrc/d' ~/bashrc
sed -i '/set -gx PATH . $PATH; source ~\/.config\/fish\/config.fish/d' ~/.config/fish/config.fish
sed -i '/config set path $nu.path $nu.path:./d' ~/.config/nu/config.toml

rm -r ~/.config/PasswdManager


# Delete entire program directory
current_directory=$(pwd)
parent_directory=$(dirname "$current_directory")
rm -rf "$parent_directory"

echo "Program and all associated files have been deleted."

