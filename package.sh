#!/bin/bash
cd ..
rm asdc.zip
find asdc -maxdepth 2 -regextype posix-egrep -regex ".*\.(py|js|jsx|json|txt|html|scss)$" -print | zip asdc.zip -@
cd -

