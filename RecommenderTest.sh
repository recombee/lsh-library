#!/usr/bin/env bash

python3 src//RunRecommenderPrecision.py -i "data/ratings.csv" -o "stats_out/test_movie_lens_precision" -k 20000 -di 9 11 -c 1 -m 0 -M 32 -t 0.01 -compare -log logs/rec.log debug -terminal debug