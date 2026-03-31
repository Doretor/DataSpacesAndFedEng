#!/bin/bash

for file in ../providers/*/observations.csv
do
        echo "$(dirname $file | cut -d '/' -f3): $(wc -l < $file)"
done
