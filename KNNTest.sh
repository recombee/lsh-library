#!/usr/bin/env bash


python3 src//RunKnnPrecision.py -i "data/ratings.csv" -o "stats_out/B" -buckets -k 10 -d 10 -c 0 -m 0.0 -M 32 -t 0.003 -log logs/knn.log basic -terminal debug

