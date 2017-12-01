#!/bin/bash
#Script to automate the virtualenv components
virtualenv env
source env/bin/activate
pip install -r requirements.txt
