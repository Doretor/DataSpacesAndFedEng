#!/bin/bash

# Zbieramy wyniki z poprzednich skryptów (P6, P7, P8)
COVERAGE=$(./data_space_coverage.sh | grep "COVERAGE SCORE" | awk '{print $3}')
DRIFT_CHECK=$(./schema_drift_detector.sh | grep "SCHEMA DRIFT DETECTED")
FED_CHECK=$(./federated_completeness.sh | grep "INCOMPLETE")

STATUS="GOOD"
REASON=""

# Logika oceny zdrowia systemu
if [ -n "$DRIFT_CHECK" ]; then
    STATUS="CRITICAL"
    REASON="schema drift detected"
elif [ -n "$FED_CHECK" ]; then
    STATUS="WARNING"
    REASON="incomplete coverage and federated loss detected"
fi

# Wyświetlenie końcowego wyniku
echo "DATA SPACE HEALTH: $STATUS"
if [ "$STATUS" != "GOOD" ]; then
    echo "Reason: $REASON"
fi
