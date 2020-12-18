#!/bin/bash
for ((i=1; i<=20; i++))
do
    python3 elve.py "10" &
done
