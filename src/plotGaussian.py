# plot_gaussian.py

import matplotlib.pyplot as plt

def plot_gaussian_distribution(file_name):
    with open(file_name, 'r') as f:
        samples = [int(line.strip()) for line in f]

    plt.hist(samples, bins=200)
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.title("Histogram of Gaussian Distribution")
    plt.savefig("../output/histogram_direct.png")

plot_gaussian_distribution("../data/gaussian_samples.txt")
