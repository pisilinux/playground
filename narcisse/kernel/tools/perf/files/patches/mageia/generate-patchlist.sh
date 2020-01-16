#!/bin/bash
counter=100

for line in $(cat series);do
    echo -e Patch0$counter:'\t'$line;
    ((counter++))
done
