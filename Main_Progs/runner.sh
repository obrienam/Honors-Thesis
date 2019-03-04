#!/bin/bash
if [ ! -f preferences.txt ]; then
	python setup.py
fi
python feedparsing.py
