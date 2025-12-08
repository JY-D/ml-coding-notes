import random


class ReservoirSampling:
    def __init__(self, k: int):
        self.k = k
        self.sample = []
        self.count = 0  # To track how many items we've seen (N)

    def process_stream(self, val: int) -> None:
        """
        Process a new value from the stream.
        """
        # 1. Update total count of items seen
        self.count += 1

        # 2. If we haven't filled the reservoir yet, take it
        if len(self.sample) < self.k:
            self.sample.append(val)
        else:
            # 3. The Magic: With probability k/count, keep the new item
            # random.randint(0, self.count - 1) generates a number from 0 to N-1
            r = random.randint(0, self.count - 1)

            if r < self.k:
                # Replace the element at the chosen index
                self.sample[r] = val
            # else: Drop the new value (do nothing)

    def get_sample(self) -> list[int]:
        return self.sample
