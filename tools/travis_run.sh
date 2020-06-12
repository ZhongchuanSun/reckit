#!/bin/bash

if [[ ${PLAT} =~ "linux" ]]
then
    docker pull $DOCKER_IMAGE
    docker run --rm -e PLAT=$PLAT -v `pwd`:/io $DOCKER_IMAGE /io/tools/travis_linux_build_whl.sh
else
    source travis_osx_build_whl.sh
fi
