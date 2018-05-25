#!/bin/bash

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# determine script path
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd ${DIR}
virtualenv separator_oracle/venv

source separator_oracle/venv/bin/activate

# install modules and add active session to database
pipenv install

# migrate
./manage.py makemigrations base
./manage.py migrate

# Add active session to database
./manage.py runscript add_active_session --script-args _Username test _Password foobar _Valid 2099-04-04

deactivate

echo "Installation of Separator Oracle done..."
