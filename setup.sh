#!/bin/bash

# Installer nodeenv
pip install nodeenv

# Créer un environnement Node.js
nodeenv -p

# Installer Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
