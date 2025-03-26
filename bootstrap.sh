#!/bin/bash

# Vérifier si pyenv est installé
if ! command -v pyenv &> /dev/null; then
    echo "Installing pyenv..."
    curl https://pyenv.run | bash
    export PATH="$HOME/.pyenv/bin:$PATH"
    eval "$(pyenv init --path)"
    eval "$(pyenv init -)"
fi

# Installer la version de Python requise
pyenv install 3.8.0 -s
pyenv global 3.8.0

# Installer pipenv
pip install pipenv

# Installer les dépendances Python
pipenv install -r requirements.txt

# Installer nodeenv
pip install nodeenv

# Créer un environnement Node.js
nodeenv -p --prebuilt

# Installer les dépendances Node.js
npm install

# Lancer l'application
echo "Installation terminée !"
echo "Lancer l'application avec :"
echo "npm start"
