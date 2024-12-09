import socket
import heapq
import pickle
import logging
import numpy as np
import matplotlib.pyplot as plt
from countMinSketch import CountMinSketch

HOST = '127.0.0.1'
PORT = 65432
WIDTH = 50
DEPTH = 10
VARIANCE = 3.86
SEED = 598
LDP = False

class Server:
    def __init__(self, ldp=False):
        self.ldp = ldp
        self.aggregated_cms = CountMinSketch(WIDTH, DEPTH, SEED)

    def aggregate_data(self, table):
        self.aggregated_cms.table += table

    def receive_data(self, conn):
        # get data length
        data_length_bytes = conn.recv(4)
        if not data_length_bytes:
            return None

        # convert data length to integer
        data_length = int.from_bytes(data_length_bytes, 'big')
        
        # receive data of size data_length
        data = b''
        while len(data) < data_length:
            packet = conn.recv(4096)
            if not packet:
                return None
            data += packet
        
        return data

    def run(self):
        total_clients = 0
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            logging.info(f"Server listening on {HOST}:{PORT}")

            while True:
                conn, addr = s.accept()
                with conn:
                    logging.info(f"Connection from {addr}")
                    data = self.receive_data(conn)
                    if data:
                        client_table = pickle.loads(data)
                        self.aggregate_data(client_table)
                        logging.info(f"Received data from {addr}")
                        total_clients += 1
                if total_clients == 5:
                    logging.info("All clients' data received.")
                    self.get_freq(k=10)
                    break

    def query(self, item):
        return self.aggregated_cms.estimate(item)
    
    def get_freq(self, k=10):
        top_k = []
        items = []
        ground_truth = self.load_ground_truth_frequencies("../data/gaussian_frequencies.txt")

        for i in range(1, 151):
            heapq.heappush(top_k, (self.query(i), i))
            items.extend([i] * self.query(i))
        
        # Calculate the histogram frequencies for the first plot
        estimated_frequencies_1 = {i: items.count(i) for i in range(1, 150)}

        mse_1 = self.calculate_mse(estimated_frequencies_1, ground_truth)

        plt.hist(items, bins=200)
        plt.xlim(1, 150)
        plt.autoscale(enable=False)
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        if self.ldp:
            plt.title("Histogram of CMS with LDP")
            plt.savefig("../output/histogram_cms_ldp.png")
            print(f"MSE for histogram CMS (with LDP): {mse_1}")
        else:
            plt.title("Histogram of CMS")
            plt.savefig("../output/histogram_cms.png")
            print(f"MSE for histogram CMS (without noise): {mse_1}")

            self.add_noise()

            items = []
            for i in range(1, 151):
                heapq.heappush(top_k, (self.query(i), i))
                items.extend([i] * self.query(i))
            
            estimated_frequencies_2 = {i: items.count(i) for i in range(1, 150)}

            mse_2 = self.calculate_mse(estimated_frequencies_2, ground_truth)
            print(f"MSE for histogram CMS (with CDP): {mse_2}")
            
            plt.clf()
            plt.hist(items, bins=200)
            plt.xlim(1, 150)
            plt.xlabel("Value")
            plt.ylabel("Frequency")
            plt.title("Histogram of CMS with CDP")
            plt.savefig("../output/histogram_cms_cdp.png")

        top_k = heapq.nlargest(k, top_k)
        print("Heavy Hitters:")
        for value, item in top_k:
            print(f"{item}: {value}")
        return top_k
    
    def load_ground_truth_frequencies(self, file_name):
        ground_truth = {}
        with open(file_name, 'r') as f:
            for line in f:
                value, freq = line.strip().split(',')
                ground_truth[int(value)] = int(freq)
        return ground_truth
    
    def calculate_mse(self, estimated_frequencies, ground_truth):
        mse = 0
        for value in range(1, 151):
            estimated_freq = estimated_frequencies.get(value, 0)
            true_freq = ground_truth.get(value, 0)
            mse += (estimated_freq - true_freq) ** 2
        mse /= 150  # average over the range of values
        return mse
        
    def add_noise(self):
        # add Gaussian noise to each entry in CMS
        variance = VARIANCE
        noise_mat = np.random.normal(0, variance, size=self.aggregated_cms.table.shape)
        self.aggregated_cms.table = self.aggregated_cms.table.astype(float) + noise_mat
        self.aggregated_cms.table = np.rint(self.aggregated_cms.table).astype(int)  # round and convert back to int


if __name__ == "__main__":
    server = Server(ldp=LDP)
    server.run()
