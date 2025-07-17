"""
UltraRF QPSK Modem (Phase 1 prototype)
Simple QPSK modulator/demodulator for single-channel operation.
"""
import numpy as np

class QPSKModem:
    def __init__(self):
        # Standard QPSK constellation (00, 01, 11, 10)
        self.constellation = {
            (0, 0): 1+1j,
            (0, 1): 1-1j,
            (1, 1): -1-1j,
            (1, 0): -1+1j
        }


    def modulate(self, bits):
        """Map bits to QPSK symbols."""
        symbols = []
        for i in range(0, len(bits), 2):
            b = (bits[i], bits[i+1])
            # Normalize constellation to unit energy
            symbols.append(self.constellation[b] / np.sqrt(2))
        return np.array(symbols)

    def demodulate(self, symbols):
        """Map QPSK symbols to bits."""
        bits = []
        for s in symbols:
            s = s * np.sqrt(2)  # De-normalize
            b0 = 0 if s.real > 0 else 1
            b1 = 0 if s.imag > 0 else 1
            bits.extend([b0, b1])
        return bits
