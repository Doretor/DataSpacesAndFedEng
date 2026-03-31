#!/bin/bash

echo "$(./search_distributed.sh)" > ./temp1.txt
echo "$(./search_federated.sh)" > ./temp2.txt

if cmp -s "temp1.txt" "temp2.txt"; then
	echo "Same output"
else
	echo "Different output"

fi

$(rm "./temp1.txt")

$(rm "./temp2.txt")

