#!/bin/sh

# Installs the unofficial youtube-dl Web interface

which -s brew
if [[ $? != 0 ]] ; then
    # Install Homebrew
    ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
else
    brew update
fi

# Install dependecies
brew install python3 ffmpeg youtube-dl git

pip3 install Flask

cd $HOME/Documents
git clone https://github.com/hkamran80/youtubedl-web
cd youtubedl-web
echo "Ready for usage!"
echo "Type 'python3 main.py' to activate the web interface"
