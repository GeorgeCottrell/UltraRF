#!/usr/bin/env python3
"""
UltraRF Physical Layer Simulation
Demonstrates OFDM modulation, LDPC coding, and channel effects
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from commpy.modulation import QAMModem
from commpy.channels import SISOFlatChannel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OFDMTransmitter:
    """OFDM transmitter for 100 kHz channel"""
    
    def __init__(self, n_subcarriers=64, n_data_subcarriers=52, cp_length=16):
        self.n_subcarriers = n_subcarriers
        self.n_data_subcarriers = n_data_subcarriers
        self.cp_length = cp_length
        
        # Subcarrier allocation
        self.data_carriers = np.arange(6, 32).tolist() + np.arange(33, 59).tolist()
        self.pilot_carriers = [11, 25, 39, 53]  # Pilot positions
        
        # Pilot symbols (BPSK)
        self.pilot_symbols = np.array([1, 1, -1, 1])
        
    def modulate(self, data_symbols):
        """Apply OFDM modulation"""
        n_ofdm_symbols = len(data_symbols) // self.n_data_subcarriers
        
        ofdm_symbols = []
        for i in range(n_ofdm_symbols):
            # Extract data for this OFDM symbol
            symbol_data = data_symbols[i*self.n_data_subcarriers:(i+1)*self.n_data_subcarriers]
            
            # Initialize frequency domain symbol
            freq_symbol = np.zeros(self.n_subcarriers, dtype=complex)
            
            # Insert data subcarriers
            freq_symbol[self.data_carriers] = symbol_data
            
            # Insert pilot subcarriers
            freq_symbol[self.pilot_carriers] = self.pilot_symbols
            
            # IFFT to time domain
            time_symbol = np.fft.ifft(np.fft.fftshift(freq_symbol))
            
            # Add cyclic prefix
            cp = time_symbol[-self.cp_length:]
            ofdm_symbol = np.concatenate([cp, time_symbol])
            
            ofdm_symbols.append(ofdm_symbol)
            
        return np.concatenate(ofdm_symbols)

class OFDMReceiver:
    """OFDM receiver with channel estimation"""
    
    def __init__(self, n_subcarriers=64, n_data_subcarriers=52, cp_length=16):
        self.n_subcarriers = n_subcarriers
        self.n_data_subcarriers = n_data_subcarriers
        self.cp_length = cp_length
        
        # Must match transmitter
        self.data_carriers = np.arange(6, 32).tolist() + np.arange(33, 59).tolist()
        self.pilot_carriers = [11, 25, 39, 53]
        self.pilot_symbols = np.array([1, 1, -1, 1])
        
    def demodulate(self, rx_signal):
        """Demodulate OFDM signal"""
        symbol_length = self.n_subcarriers + self.cp_length
        n_symbols = len(rx_signal) // symbol_length
        
        rx_symbols = []
        for i in range(n_symbols):
            # Extract OFDM symbol
            symbol_start = i * symbol_length
            ofdm_symbol = rx_signal[symbol_start:symbol_start + symbol_length]
            
            # Remove cyclic prefix
            symbol_no_cp = ofdm_symbol[self.cp_length:]
            
            # FFT to frequency domain
            freq_symbol = np.fft.fftshift(np.fft.fft(symbol_no_cp))
            
            # Channel estimation using pilots
            pilot_rx = freq_symbol[self.pilot_carriers]
            h_est = pilot_rx / self.pilot_symbols
            
            # Simple interpolation for channel estimation
            h_interp = np.interp(range(self.n_subcarriers), 
                               self.pilot_carriers, h_est)
            
            # Equalize data subcarriers
            data_eq = freq_symbol[self.data_carriers] / h_interp[self.data_carriers]
            
            rx_symbols.extend(data_eq)
            
        return np.array(rx_symbols)

class ChannelSimulator:
    """Simulate SHF channel effects"""
    
    def __init__(self, snr_db=20, multipath=True):
        self.snr_db = snr_db
        self.multipath = multipath
        
    def apply(self, signal):
        """Apply channel effects"""
        # Multipath fading
        if self.multipath:
            # Simple 2-tap channel model
            h = np.array([1.0, 0.3 * np.exp(1j * np.pi/4)])
            signal = np.convolve(signal, h, mode='same')
        
        # Add AWGN
        signal_power = np.mean(np.abs(signal)**2)
        noise_power = signal_power / (10**(self.snr_db/10))
        noise = np.sqrt(noise_power/2) * (np.random.randn(len(signal)) + 
                                          1j * np.random.randn(len(signal)))
        
        return signal + noise

def simulate_link(mcs_index=4, n_frames=100):
    """Simulate complete link performance"""
    
    # MCS table (simplified)
    mcs_table = {
        0: {'modulation': 2, 'name': 'BPSK'},    # BPSK
        1: {'modulation': 4, 'name': 'QPSK'},    # QPSK
        2: {'modulation': 4, 'name': 'QPSK'},    # QPSK
        3: {'modulation': 16, 'name': '16-QAM'},  # 16-QAM
        4: {'modulation': 16, 'name': '16-QAM'},  # 16-QAM
        5: {'modulation': 64, 'name': '64-QAM'},  # 64-QAM
        6: {'modulation': 64, 'name': '64-QAM'},  # 64-QAM
        7: {'modulation': 256, 'name': '256-QAM'} # 256-QAM
    }
    
    mcs = mcs_table[mcs_index]
    
    # Initialize components
    modem = QAMModem(mcs['modulation'])
    tx = OFDMTransmitter()
    rx = OFDMReceiver()
    
    # Simulation parameters
    bits_per_symbol = int(np.log2(mcs['modulation']))
    bits_per_frame = tx.n_data_subcarriers * bits_per_symbol * 10  # 10 OFDM symbols
    
    # SNR range for BER curve
    snr_range = np.arange(0, 35, 3)
    ber_results = []
    
    logger.info(f"Simulating MCS{mcs_index} ({mcs['name']}) over SNR range")
    
    for snr_db in snr_range:
        channel = ChannelSimulator(snr_db=snr_db, multipath=True)
        bit_errors = 0
        total_bits = 0
        
        for frame in range(n_frames):
            # Generate random bits
            tx_bits = np.random.randint(0, 2, bits_per_frame)
            
            # Modulate
            tx_symbols = modem.modulate(tx_bits)
            
            # OFDM modulation
            tx_signal = tx.modulate(tx_symbols[:tx.n_data_subcarriers * 10])
            
            # Channel
            rx_signal = channel.apply(tx_signal)
            
            # OFDM demodulation
            rx_symbols = rx.demodulate(rx_signal)
            
            # QAM demodulation
            rx_bits = modem.demodulate(rx_symbols[:len(tx_symbols)], 'hard')
            
            # Count errors
            bit_errors += np.sum(tx_bits[:len(rx_bits)] != rx_bits)
            total_bits += len(rx_bits)
        
        ber = bit_errors / total_bits
        ber_results.append(ber)
        logger.info(f"  SNR: {snr_db:2d} dB, BER: {ber:.2e}")
    
    return snr_range, ber_results, mcs

def plot_results(results):
    """Plot BER curves for different MCS"""
    plt.figure(figsize=(10, 6))
    
    for mcs_index, (snr, ber, mcs) in results.items():
        plt.semilogy(snr, ber, 'o-', label=f"MCS{mcs_index} ({mcs['name']})")
    
    plt.xlabel('SNR (dB)')
    plt.ylabel('Bit Error Rate')
    plt.title('UltraRF Physical Layer Performance')
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xlim(0, 35)
    plt.ylim(1e-5, 1)
    
    # Add target BER line
    plt.axhline(y=1e-3, color='r', linestyle='--', label='Target BER')
    
    plt.tight_layout()
    plt.savefig('ultrarf_ber_curves.png', dpi=150)
    plt.show()

def calculate_throughput():
    """Calculate theoretical throughput for each MCS"""
    print("\nUltraRF Theoretical Throughput (100 kHz channel):")
    print("=" * 50)
    print(f"{'MCS':<5} {'Modulation':<10} {'Coding':<8} {'Throughput':<12}")
    print("-" * 50)
    
    # OFDM parameters
    symbol_duration = 800e-6  # 640 + 160 us
    symbols_per_sec = 1 / symbol_duration
    data_subcarriers = 52
    
    mcs_configs = [
        (0, 'BPSK', '1/2', 1, 0.5),
        (1, 'QPSK', '1/2', 2, 0.5),
        (2, 'QPSK', '3/4', 2, 0.75),
        (3, '16-QAM', '1/2', 4, 0.5),
        (4, '16-QAM', '3/4', 4, 0.75),
        (5, '64-QAM', '2/3', 6, 0.67),
        (6, '64-QAM', '3/4', 6, 0.75),
        (7, '256-QAM', '3/4', 8, 0.75),
    ]
    
    for mcs, mod, coding, bits_per_symbol, code_rate in mcs_configs:
        throughput = symbols_per_sec * data_subcarriers * bits_per_symbol * code_rate
        throughput_kbps = throughput / 1000
        print(f"{mcs:<5} {mod:<10} {coding:<8} {throughput_kbps:>8.1f} kbps")
    
    print("\nWith 50-channel bonding (5 MHz):")
    print(f"Maximum aggregate throughput: {50 * 390:.1f} kbps = {50 * 390 / 1000:.1f} Mbps")

if __name__ == "__main__":
    print("UltraRF Physical Layer Simulation")
    print("=================================\n")
    
    # Calculate theoretical throughput
    calculate_throughput()
    
    # Run simulations for different MCS
    print("\nRunning BER simulations...")
    results = {}
    
    for mcs in [1, 4, 7]:  # QPSK, 16-QAM, 256-QAM
        snr, ber, mcs_info = simulate_link(mcs_index=mcs, n_frames=50)
        results[mcs] = (snr, ber, mcs_info)
    
    # Plot results
    plot_results(results)
    
    print("\nSimulation complete! Check 'ultrarf_ber_curves.png' for results.")
    print("\nNext steps:")
    print("1. Implement LDPC coding for 3-8 dB gain")
    print("2. Add channel bonding for multi-channel operation")
    print("3. Implement adaptive modulation based on SNR")
    print("4. Port to GNU Radio for real-time operation")