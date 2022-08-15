#!/bin/bash
set -ex

SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR

sudo apt install -y python3-pip
sudo apt install -y python3-virtualenv

virtualenv -p python3 env

source env/bin/activate
pip install -r requirements.txt

export FLASK_APP=manage
flask deploy
flask run
