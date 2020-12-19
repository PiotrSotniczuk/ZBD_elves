#!/bin/bash
psql -U ps -d elves_workspace -a -f create_and_insert.sql
for ((i=1; i<=18; i++))
do
    python3 elve.py "10" "0"&
done

# sleepy elve
for ((i=1; i<=2; i++))
do
    python3 elve.py "10" "3"&
done
