
echo "DATA SPACE REPORT" # > ../reports/data_space_report.txt
echo "Total datasets: $(./list_datasets.sh | wc -l)"
echo "Total records: $(cat $(./list_datasets.sh) | wc -l)"
echo "Objects found for query OBJ-003: $(cat ../providers/*/observations.csv | grep "OBJ-003" | wc -l)"
#if [ $(./compare_queries) -eq "Same output" ]; then
#	echo "Consistency check: yes"
#else
#	echo "Consistency check: no"
#fi

#Total datasets: <number>
#Total records: <number>
#Objects found for query OBJ-003: <number>
#Consistency check: <yes/no>
