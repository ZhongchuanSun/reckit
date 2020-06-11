#!/bin/bash
set -e -u -x

# Compile cpp
cd io/

#mkdir compiled_so
for PYBIN in /opt/python/*/bin; do
    if [[ ${PYBIN} =~ "3" ]]
    then
        echo ${PYBIN}
        PIP_EXE="${PYBIN}/pip"
        ${PIP_EXE} install -r requirements.txt
        PYTHON_EXE="${PYBIN}/python"
        ${PYTHON_EXE} setup.py sdist bdist_wheel
    fi

done
