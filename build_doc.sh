#!/bin/bash
set -e
if [[ "$1" == "-g" ]]; then
    python3 tools/generator/generator.py build_docs
    shift
fi
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
