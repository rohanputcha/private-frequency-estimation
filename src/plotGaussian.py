# plot_gaussian.py

import matplotlib.pyplot as plt
from collections import Counter

def plot_gaussian_distribution(file_name, output_file_name):
    with open(file_name, 'r') as f:
        samples = [int(line.strip()) for line in f]

    value_counts = Counter(samples)
    
    with open(output_file_name, 'w') as out_f:
        for value in range(1, 151):
            out_f.write(f"{value},{value_counts.get(value, 0)}\n")

    plt.hist(samples, bins=200)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.xlim(1, 150)
    plt.title("Histogram of Gaussian Distribution")
    plt.savefig("../output/histogram_direct.png")

plot_gaussian_distribution("../data/gaussian_samples.txt", output_file_name="../data/gaussian_frequencies.txt")
