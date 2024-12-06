import socket
import pickle
import logging
import sys
from countMinSketch import CountMinSketch
import numpy as np

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 65432
WIDTH = 100
DEPTH = 20
SEED = 598

class Client:
    def __init__(self, client_port, ldp=False):
        self.ldp = ldp
        self.cms = CountMinSketch(WIDTH, DEPTH, SEED)
        self.client_port = client_port
        self.partition_file = f"../data/partitioned/gaussian_samples_part_{client_port - 5000}.txt"

    def load_data_from_partition(self):
        try:
            with open(self.partition_file, 'r') as file:
                for line in file:
                    item = line.strip()
                    self.cms.add(int(item))
            logging.info(f"Data loaded from {self.partition_file}")
        except FileNotFoundError:
            logging.error(f"File {self.partition_file} not found.")
            sys.exit(1)

    def send_data(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('', self.client_port))
            s.connect((SERVER_HOST, SERVER_PORT))

            if self.ldp:
                self.add_noise()
            
            serialized_table = pickle.dumps(self.cms.table)
            data_length = len(serialized_table)
            
            # send length of data
            s.sendall(data_length.to_bytes(4, 'big'))
            # send pickle data of CMS
            s.sendall(serialized_table)
            logging.info("Data sent to server.")
            s.close()

    def run(self):
        self.load_data_from_partition()
        self.send_data()

    def add_noise(self):
        # add Gaussian noise to each entry in CMS
        variance = 20
        noise_mat = np.random.normal(0, variance, size=self.cms.table.shape)
        self.cms.table = self.cms.table.astype(float) + noise_mat
        self.cms.table = np.rint(self.cms.table).astype(int)  # round and convert back to int

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client.py <client_port>")
        sys.exit(1)
    
    client_port = int(sys.argv[1])
    client = Client(client_port, ldp=True)
    client.run()
