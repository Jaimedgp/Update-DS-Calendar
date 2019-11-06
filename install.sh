#!/bin/sh

mkdir "$HOME/.bin"
cp "../Update-DS-Calendar/" "$HOME/.bin/"


/usr/bin/python3 "$HOME/.bin/Upload-DS-Calendar/src/install.py

mv "$HOME/.bin/Upload-DS-Calendar/src/main.py" "$HOME/.bin/Upload-DS-Calendar/src/agenda"

chmod +x "$HOME/.bin/Upload-DS-Calendar/src/agenda"

echo 'export PATH=$PATH":$HOME/.bin/Upload-DS-Calendar/src"' >> "$HOME/.bashrc"
