import random

class KeyPool:
    def __init__(self, keys):
        self.keys = [k for k in keys if k]

    def get(self):
        return random.choice(self.keys) if self.keys else None
