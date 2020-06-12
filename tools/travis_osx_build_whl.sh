#!/bin/bash

python -m pip install cibuildwheel==1.4.2

python -m pip install -r requirements.txt
# python setup.py sdist bdist_wheel
python -m cibuildwheel --output-dir wheelhouse
