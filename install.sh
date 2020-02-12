#!/bin/sh

newFolder = "$HOME/.bin/Update-DS-Calendar/"

mkdir -p "${newFolder}"
cp -r "$PWD/src/" "${newFolder}"
cp -r "$PWD/doc/" "${newFolder}"


/usr/bin/python3 "${newFolder}/src/install.py"

mv "${newFolder}/src/main.py" "${newFolder}/src/agenda"

chmod +x "${newFolder}/src/agenda"

export_line='export PATH=$PATH":${newFolder}/src"'

if ! grep -Fxq "$export_line" $HOME/.bashrc
then
	echo "$export_line" >> "$HOME/.bashrc"
fi
