#!/bin/bash

cd ~/git/ray-quickstart
python -m build
twine upload dist/*
python setup.py clean
