import hashlib
import numpy as np
import xxhash

class CountMinSketch:
    def __init__(self, width, depth, seed=None):
        self.width = width # w
        self.depth = depth # d
        self.table = np.zeros((depth, width), dtype=int)
        self.hashes = self._create_hash_functions(depth, seed)

    def _create_hash_functions(self, num_hashes, seed):
        hashes = []
        seed = np.random.randint(0, 2**32) if seed is None else seed
        for i in range(num_hashes):
            new_seed = seed + i
            def hash_function(x, seed=new_seed):
                byte_length = (x.bit_length() + 7) // 8 or 1
                byte_rep = x.to_bytes(byte_length, byteorder='big', signed=True)
                return xxhash.xxh32(byte_rep, seed=seed).intdigest() % self.width
            hashes.append(hash_function)
        return hashes


    def add(self, item):
        for i in range(self.depth):
            index = self.hashes[i](item)
            self.table[i][index] += 1

    def estimate(self, item):
        min_estimate = float('inf')
        for i in range(self.depth):
            index = self.hashes[i](item)
            min_estimate = min(min_estimate, self.table[i][index])
        return min_estimate

# def main():
#     width = 100
#     depth = 20
#     seed = 598
#     cms = CountMinSketch(width, depth, seed)

#     items = ['apple', 'banana', 'orange', 'apple', 'banana', 'apple']
#     for item in items:
#         cms.add(item)

#     for item in set(items):
#         print(f"Estimated frequency of {item}: {cms.estimate(item)}")


# if __name__ == "__main__":
#     main()