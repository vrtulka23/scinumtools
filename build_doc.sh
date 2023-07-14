#!/bin/bash

rm -rf docs/build/*
rm -fr ./docs/source/api
sphinx-apidoc -o ./docs/source/api ./src/*
cd docs
#make html latexpdf
#make html
sphinx-build -b html source build/html -v
cd ..
