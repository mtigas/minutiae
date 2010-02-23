#!/bin/bash

export PROJECT_DIR=`pwd`

export PATH=$PROJECT_DIR/third_party/django/bin:$PATH
export PYTHONPATH=$PROJECT_DIR/server:$PROJECT_DIR/third_party:$PYTHONPATH
export PYTHONOPTIMIZE=1

export DJANGO_SETTINGS_MODULE=minutiae.settings.development

# Kill outdated Python temp files 
alias cleanpy='find $PROJECT_DIR -name "*.pyc" -delete;find $PROJECT_DIR -name "*.pyo" -delete'
cleanpy

# Refresh the 'third_party' directory.
#./update_dependencies.sh
