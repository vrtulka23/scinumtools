#!/bin/bash
cd docs
make clean
rm -fr ./source/api
sphinx-apidoc -o ./source/api ../src/*
sphinx-build -b html source build/html -v
cd build/html
echo "Documentation HTML:"
echo $(pwd)/index.html
