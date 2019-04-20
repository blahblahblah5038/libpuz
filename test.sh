#!/bin/sh

#This testing script requires that pytest-3 is installed. Try 'sudo apt-get install pytest-3'
mkdir pytest-logs
pytest-3 -v --color=yes --durations=3 tst
