"""
UltraRF Phase 2 Protocol Test
Test OFDM modem, dynamic TDMA, and BATMAN mesh routing.
"""
import numpy as np
from src.physical.ofdm_modem import OFDMModem
from src.mac.tdma_dynamic import DynamicTDMA
from src.network.batman_mesh import BatmanMesh

def test_ofdm_modem():
    modem = OFDMModem(num_channels=4, mcs='QPSK')
    data = np.random.randint(0, 2, 32)
    symbols = modem.modulate(data)
    recovered = modem.demodulate(symbols)
    assert recovered.shape == data.shape

def test_dynamic_tdma():
    tdma = DynamicTDMA(num_slots=2)
    assert tdma.request_slot('A', 0) == 0
    assert tdma.request_slot('B', 1) == 1
    assert tdma.request_slot('C', 2) == -1
    assert tdma.release_slot('A')
    assert tdma.request_slot('C', 2) == 0

def test_batman_mesh():
    mesh = BatmanMesh()
    mesh.update_link('A', snr=20, packet_loss=0.1, latency=10)
    mesh.update_link('B', snr=10, packet_loss=0.2, latency=20)
    assert mesh.best_neighbor() == 'A'
    assert mesh.route_packet(b'data') == 'A'

if __name__ == '__main__':
    test_ofdm_modem()
    test_dynamic_tdma()
    test_batman_mesh()
    print('Phase 2 protocol tests passed.')
