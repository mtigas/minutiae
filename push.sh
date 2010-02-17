#!/bin/bash

# Push git repository to server.
git push --force origin master
git push --force github master

# Push static files to app engine
#appcfg.py update .

# Reset server's working git copy to HEAD,
# restart server processes.
ssh -C 173.45.236.2 "
cd mt2
git reset --hard HEAD
git gc
./update_dependencies.sh

touch wsgi.py
sudo service nginx restart
sudo service apache2 restart
sudo service memcached restart
find . -name \"*.pyc\" -delete
find . -name \"*.pyo\" -delete
"

# Clean up locally, for the hell of it.
find . -name "*.pyc" -delete
find . -name "*.pyo" -delete
git gc
