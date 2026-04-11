#!/bin/bash
echo "Object Distribution Across Providers:"
awk -F',' '{print $2}' ../providers/*/observations.csv | sort | uniq -c | sort -nr
