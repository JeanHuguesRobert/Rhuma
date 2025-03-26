@echo off

:: Vérifier si pyenv est installé
pyenv --version >nul 2>&1
if errorlevel 1 (
    echo Installing pyenv...
    curl -L https://github.com/pyenv-win/pyenv-win/archive/master.zip -o pyenv.zip
    tar -xzf pyenv.zip -C "%USERPROFILE%\AppData\Local\Programs"
    set PATH=%USERPROFILE%\AppData\Local\Programs\pyenv-win\bin;%USERPROFILE%\AppData\Local\Programs\pyenv-win\shims;%PATH%
)

:: Installer la version de Python requise
pyenv install 3.8.0 -s
pyenv global 3.8.0

:: Installer pipenv
pip install pipenv

:: Installer les dépendances Python
pipenv install -r requirements.txt

:: Installer nodeenv
pip install nodeenv

:: Créer un environnement Node.js
nodeenv -p --prebuilt

:: Installer les dépendances Node.js
npm install

:: Lancer l'application
echo Installation terminée !
echo Pour lancer l'application, utilisez :
echo npm start
