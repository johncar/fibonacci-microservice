#!/bin/bash

if ! nose2 2>/dev/null; then
	echo "Installing nose2 (required for run tests project)."
	pip install nose2
	exit 1
fi

echo "Start running test for ${PWD##*/}"

nose2 -c etc/unittest.cfg --verbose