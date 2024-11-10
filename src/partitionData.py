# partition_gaussian.py

import os
import sys

def partition_file(input_file, num_partitions):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    partition_size = len(lines) // num_partitions
    remainder = len(lines) % num_partitions

    output_directory = "../data/partitioned/"
    os.makedirs(output_directory, exist_ok=True)

    for i in range(num_partitions):
        start_index = i * partition_size
        end_index = start_index + partition_size

        if i < remainder:
            end_index += 1
        
        partition_file_name = os.path.join(output_directory, f"{os.path.splitext(os.path.basename(input_file))[0]}_part_{i+1}.txt")
        with open(partition_file_name, 'w') as part_file:
            part_file.writelines(lines[start_index:end_index])

        print(f"Partition {i+1} saved as {partition_file_name}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python partition_gaussian.py <num_partitions>")
        sys.exit(1)

    n = int(sys.argv[1])
    partition_file("../data/gaussian_samples.txt", num_partitions=n)
