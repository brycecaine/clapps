#!/bin/bash

export FLASK_APP='/data/data/com.termux/files/home/.termux/tasker/app.py'
nohup flask run > app.log 2>&1 &

