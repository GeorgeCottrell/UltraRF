"""
UltraRF Channel Bonding
Implements contiguous and non-contiguous channel aggregation.
"""
import numpy as np

class ChannelBonding:
    def __init__(self, channels):
        self.channels = channels  # list of channel indices

    def aggregate(self, data):
        # Placeholder: split data across channels
        n = len(self.channels)
        return [data[i::n] for i in range(n)]

    def combine(self, channel_data):
        # Interleave data from channels to reconstruct original order
        n = len(channel_data)
        lengths = [len(x) for x in channel_data]
        min_len = min(lengths)
        # Interleave up to min_len
        out = []
        for i in range(min_len):
            for ch in range(n):
                out.append(channel_data[ch][i])
        # Add any remaining elements (ragged end)
        for ch in range(n):
            out.extend(channel_data[ch][min_len:])
        return np.array(out)
