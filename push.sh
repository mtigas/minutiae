#!/bin/bash

# Push git repository to server.
git push --force origin master
git push --force github master

# Push static files to app engine
#python2.5 `which appcfg.py` update .

# Reset server's working git copy to HEAD,
# restart server processes.
ssh -C 173.45.236.2 "
cd mt2
git reset --hard HEAD
git gc --aggressive
./update_dependencies.sh

touch wsgi.py
sudo stop uwsgi_miketigas
sudo service nginx restart
sudo start uwsgi_miketigas
find . -name \"*.pyc\" -delete
find . -name \"*.pyo\" -delete
"

# Clean up locally, for the hell of it.
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
git gc --aggressive
