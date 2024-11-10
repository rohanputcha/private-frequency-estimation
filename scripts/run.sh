#!/bin/bash

# go to src
cd ../src

# start server
echo "Starting server..."
python3 server.py & sleep 2

# Start multiple clients
echo "Starting clients..."
for i in {5001..5005}; do
    python3 client.py $i & sleep 1
done

wait
echo "All processes completed."
