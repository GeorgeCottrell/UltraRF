"""
UltraRF Phase 1 Protocol Test
Test QPSK modem, simple TDMA, and null network layer.
"""
import numpy as np
from src.physical.qpsk_modem import QPSKModem
from src.mac.tdma_simple import SimpleTDMA
from src.network.null_network import NullNetwork

def test_qpsk_modem():
    modem = QPSKModem()
    # Test all 4 QPSK symbols
    bit_patterns = [
        ([0,0], 0.70710678+0.70710678j),
        ([0,1], 0.70710678-0.70710678j),
        ([1,1], -0.70710678-0.70710678j),
        ([1,0], -0.70710678+0.70710678j)
    ]
    for bits, expected_symbol in bit_patterns:
        symbols = modem.modulate(bits)
        assert np.allclose(symbols[0], expected_symbol, atol=1e-6)
        recovered = modem.demodulate(symbols)
        assert bits == recovered

def test_tdma():
    tdma = SimpleTDMA(num_slots=2)
    assert tdma.request_slot('A') == 0
    assert tdma.request_slot('B') == 1
    assert tdma.request_slot('C') == -1
    assert tdma.release_slot('A')
    assert tdma.request_slot('C') == 0

def test_null_network():
    net = NullNetwork()
    data = b'hello'
    assert net.route(data) == data

if __name__ == '__main__':
    test_qpsk_modem()
    test_tdma()
    test_null_network()
    print('Phase 1 protocol tests passed.')
