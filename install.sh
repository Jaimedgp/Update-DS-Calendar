#!/bin/sh

mkdir -p "$HOME/.bin/Update-DS-Calendar/"
cp -r "$PWD/src/" "$HOME/.bin/Update-DS-Calendar"
cp -r "$PWD/doc/" "$HOME/.bin/Update-DS-Calendar"


".$HOME/.bin/Update-DS-Calendar/src/install.py"

mv "$HOME/.bin/Update-DS-Calendar/src/main.py" "$HOME/.bin/Update-DS-Calendar/src/agenda"

chmod +x "$HOME/.bin/Update-DS-Calendar/src/agenda"

export_line='export PATH=$PATH":$HOME/.bin/Update-DS-Calendar/src"'

if ! grep -Fxq "$export_line" $HOME/.bashrc
then
	echo "$export_line" >> "$HOME/.bashrc"
fi
