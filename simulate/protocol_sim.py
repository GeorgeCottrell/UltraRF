"""
UltraRF Protocol Simulation
Simulates end-to-end PHY+MAC operation with OFDM and TDMA.
"""
import numpy as np
from src.physical.ofdm_modem import OFDMModem
from src.mac.tdma_dynamic import DynamicTDMA

def simulate_protocol(num_channels=4, num_slots=4, snr=15, n_nodes=2, bits_per_node=64):
    # Generate random data for each node
    node_data = {chr(65+i): np.random.randint(0, 2, bits_per_node) for i in range(n_nodes)}
    # MAC: allocate slots
    mac = DynamicTDMA(num_slots=num_slots)
    slot_map = {}
    for i, node in enumerate(node_data):
        slot_map[node] = mac.request_slot(node, i)  # Different QoS for each
    # PHY: OFDM modem
    phy = OFDMModem(num_channels=num_channels, mcs='QPSK')
    # Simulate transmission for each node
    results = {}
    for node, bits in node_data.items():
        tx_syms = phy.modulate(bits)
        # Add AWGN noise (simulate SNR)
        noisy_syms = [s + np.random.normal(0, 1/np.sqrt(snr), s.shape) for s in tx_syms]
        rx_bits = phy.demodulate(noisy_syms)
        ber = np.mean(bits != rx_bits[:len(bits)])
        results[node] = {'slot': slot_map[node], 'ber': ber}
    return results

if __name__ == '__main__':
    results = simulate_protocol()
    for node, res in results.items():
        print(f'Node {node}: Slot {res["slot"]}, BER={res["ber"]:.3e}')
