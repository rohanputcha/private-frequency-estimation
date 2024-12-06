import socket
import heapq
import pickle
import logging
import numpy as np
import matplotlib.pyplot as plt
from countMinSketch import CountMinSketch

HOST = '127.0.0.1'
PORT = 65432
WIDTH = 100
DEPTH = 20
SEED = 598

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
                    self.get_top_k(k=10)
                    break

    def query(self, item):
        return self.aggregated_cms.estimate(item)
    
    def get_top_k(self, k=10):
        top_k = []
        items = []
        for i in range(-40, 41):
            heapq.heappush(top_k, (self.query(i), i))
            items.extend([i] * self.query(i))

        plt.hist(items, bins=200)
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        if self.ldp:
            plt.title("Histogram of CMS with LDP")
            plt.savefig("../output/histogram_cms_ldp.png")
        else:
            plt.title("Histogram of CMS")
            plt.savefig("../output/histogram_cms.png")

            self.add_noise()

            items = []
            for i in range(-40, 41):
                heapq.heappush(top_k, (self.query(i), i))
                items.extend([i] * self.query(i))
            
            plt.clf()
            plt.hist(items, bins=200)
            plt.xlabel("Value")
            plt.ylabel("Frequency")
            plt.title("Histogram of CMS with CDP")
            plt.savefig("../output/histogram_cms_cdp.png")

        top_k = heapq.nlargest(k, top_k)
        print("Heavy Hitters:")
        for value, item in top_k:
            print(f"{item}: {value}")
        return top_k
    
    def add_noise(self):
        # add Gaussian noise to each entry in CMS
        variance = 20
        noise_mat = np.random.normal(0, variance, size=self.aggregated_cms.table.shape)
        self.aggregated_cms.table = self.aggregated_cms.table.astype(float) + noise_mat
        self.aggregated_cms.table = np.rint(self.aggregated_cms.table).astype(int)  # round and convert back to int


if __name__ == "__main__":
    server = Server(ldp=True)
    server.run()
