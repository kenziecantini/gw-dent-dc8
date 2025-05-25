import hashlib

class Block:
    def __init__(self, data, prev_hash, difficulty=4):
        self.data = data
        self.prev_hash = prev_hash
        self.nonce = 0
        self.difficulty = difficulty
        self.hash = self.mine_block()

    def calculate_hash(self):
        content = self.data + self.prev_hash + str(self.nonce)
        return hashlib.sha256(content.encode()).hexdigest()

    def mine_block(self):
        prefix = "0" * self.difficulty
        while True:
            hash_attempt = self.calculate_hash()
            if hash_attempt.startswith(prefix):
                return hash_attempt
            self.nonce += 1

# linear equation
# first_block + "Nonce" = "0000"

# Create blockchain with difficulty
block1 = Block("First Block", "0")
block2 = Block("Second Block", block1.hash)
block3 = Block("Third Block", block2.hash)

# Print chain
for blk in [block1, block2, block3]:
    print(f"Data: {blk.data}\nNonce: {blk.nonce}\nHash: {blk.hash}\nPrevHash: {blk.prev_hash}\n")
