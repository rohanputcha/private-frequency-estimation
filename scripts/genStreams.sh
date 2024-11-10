#!/bin/bash

# go to src
cd ../src

python3 genData.py # see file to change num samples, mean, std_dev
python3 partitionData.py 5
