"""
UltraRF Adaptive Modem
Implements adaptive modulation and coding (QPSK, 16QAM, 256QAM) selection based on SNR.
"""
import numpy as np

class AdaptiveModem:
    def __init__(self):
        self.mcs_table = [
            {'mod':'QPSK', 'snr':5},
            {'mod':'16QAM', 'snr':12},
            {'mod':'256QAM', 'snr':25}
        ]

    def select_mcs(self, snr):
        for entry in reversed(self.mcs_table):
            if snr >= entry['snr']:
                return entry['mod']
        return 'QPSK'

    def modulate(self, bits, snr):
        mcs = self.select_mcs(snr)
        # Placeholder: call appropriate modem
        return mcs

    def demodulate(self, symbols, snr):
        mcs = self.select_mcs(snr)
        # Placeholder: call appropriate demod
        return mcs
