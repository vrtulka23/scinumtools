#!/bin/bash
set -e
python3 build_tables.py
cd docs
if [[ "$1" != "-u" ]]; then
    make clean
    rm -fr ./source/api
fi
sphinx-apidoc -o ./source/api ../src/*
sphinx-build -b html source build/html -v
cd build/html
echo "Documentation HTML:"
echo $(pwd)/index.html
