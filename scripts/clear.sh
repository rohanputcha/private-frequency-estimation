#!/bin/bash

# go to data
cd ../data

rm -rf gaussian_samples.txt partitioned

pkill -f '/server.py$'
pkill -f '/client.py$'