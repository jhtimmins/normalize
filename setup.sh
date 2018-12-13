#!/bin/bash

virtualenv -p python3 virtualenv
source virtualenv/bin/activate
pip3 install -r requirements.txt
