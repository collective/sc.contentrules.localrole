#!/bin/bash

function handle_exit {
    if [ $? -ne 0 ]; then
        EXITCODE=1
    fi
}

EXITCODE=0

echo 'Running tests'
bin/test; handle_exit

echo '====== Running PyFlakes ======'
bin/zopepy setup.py flakes; handle_exit

echo '====== Running pep8 =========='
bin/pep8 --ignore=E501 sc/contentrules/localrole; handle_exit
bin/pep8 --ignore=E501 setup.py; handle_exit

if [ $EXITCODE -ne 0 ]; then
    exit 1
fi
