#!/bin/bash
for ((i=1; i<=5; i++))
do
    python3 elve.py "200" &
done
