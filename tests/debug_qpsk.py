import numpy as np
from src.physical.qpsk_modem import QPSKModem

modem = QPSKModem()
bit_patterns = [[0,0],[0,1],[1,1],[1,0]]
for bits in bit_patterns:
    symbols = modem.modulate(bits)
    print('bits:', bits, '-> symbols:', symbols)
    recovered = modem.demodulate(symbols)
    print('recovered:', recovered)
