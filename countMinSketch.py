import hashlib
import numpy as np
import xxhash

class CountMinSketch:
    def __init__(self, width, depth):
        self.width = width # w
        self.depth = depth # d
        self.table = np.zeros((depth, width), dtype=int)
        self.hashes = self._create_hash_functions(depth)

    def _create_hash_functions(self, num_hashes):
        """Generates independent hash functions using xxhash."""
        hashes = []
        for i in range(num_hashes):
            seed = np.random.randint(0, 2**32)
            def hash_function(x, seed=seed):
                return xxhash.xxh32(x.encode('utf-8'), seed=seed).intdigest() % self.width
            
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

def main():
    width = 10
    depth = 5
    cms = CountMinSketch(width, depth)

    items = ['apple', 'banana', 'orange', 'apple', 'banana', 'apple']
    for item in items:
        cms.add(item)

    for item in set(items):
        print(f"Estimated frequency of {item}: {cms.estimate(item)}")


if __name__ == "__main__":
    main()