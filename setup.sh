#!/bin/bash

echo $PWD
path=$(dirname "$0")

echo "Log : Creating virutalenv"

python3 -m venv "${path}/venv"
source "${path}/venv/bin/activate"
pip install -r "${path}/requirements.txt"
