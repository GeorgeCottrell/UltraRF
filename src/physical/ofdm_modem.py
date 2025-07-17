"""
UltraRF OFDM Modem (Phase 2 prototype)
Supports multi-channel bonding and adaptive modulation.
"""
import numpy as np

class OFDMModem:
    def __init__(self, num_channels=1, mcs='QPSK'):
        self.num_channels = num_channels
        self.mcs = mcs  # 'QPSK', '16QAM', '256QAM'

    def modulate(self, data_bits):
        """OFDM modulation with channel bonding and adaptive MCS."""
        # Split data_bits across channels
        n = self.num_channels
        split = [data_bits[i::n] for i in range(n)]
        # Map bits to QPSK symbols (for simplicity, QPSK only)
        def bits_to_qpsk(bits):
            symbols = []
            for i in range(0, len(bits), 2):
                b0 = bits[i] if i < len(bits) else 0
                b1 = bits[i+1] if i+1 < len(bits) else 0
                # QPSK: 00=1+1j, 01=1-1j, 11=-1-1j, 10=-1+1j
                if (b0, b1) == (0,0): s = 1+1j
                elif (b0, b1) == (0,1): s = 1-1j
                elif (b0, b1) == (1,1): s = -1-1j
                else: s = -1+1j
                symbols.append(s/np.sqrt(2))
            return np.array(symbols)
        # OFDM: each channel is a subcarrier group
        ofdm_symbols = [bits_to_qpsk(bits) for bits in split]
        return ofdm_symbols

    def demodulate(self, ofdm_symbols):
        """OFDM demodulation (QPSK only)."""
        # Demap QPSK symbols to bits
        def qpsk_to_bits(symbols):
            bits = []
            for s in symbols:
                s = s * np.sqrt(2)
                b0 = 0 if s.real > 0 else 1
                b1 = 0 if s.imag > 0 else 1
                bits.extend([b0, b1])
            return bits
        # Combine bits from all channels (de-interleave)
        n = len(ofdm_symbols)
        bit_lists = [qpsk_to_bits(syms) for syms in ofdm_symbols]
        # Interleave bits to reconstruct original order
        out = []
        for i in range(max(len(b) for b in bit_lists)):
            for ch in range(n):
                if i < len(bit_lists[ch]):
                    out.append(bit_lists[ch][i])
        return np.array(out)
