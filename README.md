# UltraRF Protocol - Ultra High-Speed RF Networking for Amateur Radio SHF Bands

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)
[![Amateur Radio](https://img.shields.io/badge/Amateur%20Radio-SHF%20Bands-blue.svg)]()

## 🚀 Project Overview

UltraRF is an experimental ultra high-speed RF networking protocol designed for amateur radio SHF bands (10 GHz and 24 GHz). Our goal is to push the boundaries of amateur radio digital communications, achieving 20-50 Mbps throughput while maintaining full FCC Part 97 compliance.

### Key Features
- **Channel Bonding**: Aggregate multiple 100 kHz channels for 20-50 Mbps total throughput
- **Adaptive Modulation**: Dynamic switching between QPSK, 16-QAM, and 256-QAM based on RF conditions
- **Mesh Networking**: Self-healing, distributed architecture optimized for emergency communications
- **SDR-Based**: Works with affordable software-defined radios (PlutoSDR, BladeRF, USRP)
- **Open Source**: Fully open development with community collaboration

## 📋 Technical Specifications

### Performance Targets
- **Single Channel**: 600-800 kbps per 100 kHz channel
- **Aggregate**: 20-50 Mbps using channel bonding (25-60 channels)
- **Latency**: <10ms for real-time applications
- **Range**: 10-50km line-of-sight (depending on power/antenna)

### Frequency Bands
- **10.0-10.5 GHz** (3cm band) - 500 MHz available spectrum
- **24.0-24.25 GHz** (1.2cm band) - 250 MHz available spectrum

### Modulation & Coding
- **Modulation**: OFDM with QPSK/16-QAM/256-QAM
- **Error Correction**: LDPC codes (3-8 dB coding gain)
- **Spectral Efficiency**: 6-8 bits/s/Hz theoretical maximum

## 🛠️ Getting Started

### Prerequisites
- Amateur Radio License (Technician class or higher)
- SDR Hardware (PlutoSDR, BladeRF, or USRP)
- SHF frequency converter/transverter
- GNU Radio 3.10+ or Python 3.8+
- Basic knowledge of digital signal processing

### Quick Start
```bash
# Clone the repository
git clone https://github.com/GeorgeCottrell/UltraRF/ultrarf.git
cd ultrarf-protocol

# Install dependencies
pip install -r requirements.txt

# Run the physical layer simulation
python simulate/physical_layer.py

# Run the protocol-level simulation (PHY+MAC)
python simulate/protocol_sim.py

# Run all protocol feature tests
python -m unittest discover tests

# Start the GNU Radio prototype
gnuradio-companion flowgraphs/ultrarf_prototype.grc
```

## 📁 Repository Structure

ultrarf-protocol/
├── docs/                    # Documentation and specifications
│   ├── protocol-spec.md     # Complete protocol specification
│   ├── fcc-compliance.md    # FCC Part 97 compliance guide
│   └── hardware-guide.md    # Hardware setup instructions
├── src/                     # Source code
│   ├── physical/           # Physical layer implementation
│   ├── mac/               # MAC layer implementation
│   └── network/           # Network layer (mesh routing)
├── simulate/               # Simulation scripts
│   ├── channel_model.py   # SHF channel modeling
│   └── physical_layer.py  # PHY performance simulation
├── flowgraphs/            # GNU Radio flowgraphs
├── fpga/                  # FPGA implementations
├── tests/                 # Unit and integration tests
├── tools/                 # Utility scripts
└── examples/              # Example configurations

```
```
ultrarf-protocol/
├── docs/                    # Documentation and specifications
│   ├── protocol-spec.md     # Complete protocol specification
│   ├── fcc-compliance.md    # FCC Part 97 compliance guide
│   └── hardware-guide.md    # Hardware setup instructions
├── src/                     # Source code
│   ├── physical/            # Physical layer implementation (ofdm_modem.py, qpsk_modem.py, etc.)
│   ├── mac/                 # MAC layer implementation (tdma_dynamic.py, qos_manager.py, etc.)
│   └── network/             # Network layer (mesh routing, mesh_services.py)
├── simulate/                # Simulation scripts
│   ├── channel_model.py     # SHF channel modeling
│   ├── physical_layer.py    # PHY performance simulation
│   └── protocol_sim.py      # End-to-end protocol simulation (PHY+MAC)
├── flowgraphs/              # GNU Radio flowgraphs
├── fpga/                    # FPGA implementations
├── tests/                   # Unit and integration tests (test_phase1.py, test_phase2.py, test_features.py)
├── tools/                   # Utility scripts
└── examples/                # Example configurations
```

You can run protocol and physical layer simulations, as well as all feature tests:

```bash
# Run the physical layer simulation
python simulate/physical_layer.py

# Run the protocol-level simulation (PHY+MAC)
python simulate/protocol_sim.py

# Run all protocol feature tests
python -m unittest discover tests
```


## 🤝 Contributing

We welcome contributions from the amateur radio community! Whether you're an RF engineer, software developer, or enthusiastic ham operator, there's a place for you in this project.

### Ways to Contribute
- **Code Development**: Implement protocol features in Python/C++
- **Testing**: Field test the protocol and report results
- **Documentation**: Improve guides and specifications
- **Hardware**: Design/test frequency converters and antennas
- **Community**: Share the project and recruit testers

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 🗺️ Roadmap

### Phase 1: Foundation (Q1 2026)
- [x] Initial protocol specification
- [ ] Single-channel QPSK prototype
- [ ] Basic TDMA implementation
- [ ] GNU Radio proof-of-concept

### Phase 2: Enhancement (Q2 2026)
- [ ] Multi-channel bonding (5-10 channels)
- [ ] Adaptive coding and modulation
- [ ] BATMAN-based mesh routing
- [ ] Field testing with 5 nodes

### Phase 3: Optimization (Q3 2026)
- [ ] 20+ Mbps aggregate throughput
- [ ] QoS for emergency traffic
- [ ] Beamforming integration
- [ ] Regional test network deployment

### Phase 4: Standardization (Q4 2026)
- [ ] Community beta release
- [ ] ARRL/TAPR proposal submission
- [ ] Integration with AREDN/HamWAN
- [ ] Version 1.0 release

## 📡 Hardware Requirements

### Minimum Setup
- **SDR**: PlutoSDR ($149) or equivalent
- **Converter**: 10 GHz downconverter (~$200)
- **Antenna**: 18 dBi dish or horn antenna (~$100)
- **Computer**: Raspberry Pi 4 or laptop

### Recommended Setup
- **SDR**: BladeRF 2.0 micro ($480)
- **Converter**: Kuhne Electronic MKU 10 G3 ($500)
- **Antenna**: 24 dBi parabolic dish ($200)
- **Computer**: Desktop with GPU for DSP acceleration

### SDR Software Setup
- **Python 3.8+** and required packages (see `requirements.txt`)
- **GNU Radio 3.10+** for real-time SDR prototyping
- **Simulation**: All protocol features can be tested in software without hardware using the provided simulation scripts.

## 📊 Performance Benchmarks

| Modulation | Coding Rate | SNR Required | Throughput (100 kHz) |
|------------|-------------|--------------|---------------------|
| QPSK       | 1/2         | 5 dB         | 100 kbps           |
| QPSK       | 3/4         | 8 dB         | 150 kbps           |
| 16-QAM     | 1/2         | 12 dB        | 200 kbps           |
| 16-QAM     | 3/4         | 15 dB        | 300 kbps           |
| 256-QAM    | 3/4         | 25 dB        | 600 kbps           |

## 📜 FCC Compliance

This protocol is designed for full FCC Part 97 compliance:
- ✅ 100 kHz bandwidth limit per channel
- ✅ Automated station identification every 10 minutes
- ✅ Spurious emissions meet "greatest extent practicable"
- ✅ Secondary user interference avoidance

See [docs/fcc-compliance.md](docs/fcc-compliance.md) for detailed information.

## 📚 Resources

- [ARRL Band Plan](http://www.arrl.org/band-plan)
- [FCC Part 97 Regulations](https://www.law.cornell.edu/cfr/text/47/part-97)
- [GNU Radio Tutorials](https://wiki.gnuradio.org/index.php/Tutorials)
- [AREDN Mesh Networking](https://www.arednmesh.org/)

## 🙏 Acknowledgments

- The amateur radio community for ongoing support and testing
- ARRL and TAPR for technical resources
- GNU Radio project for the SDR framework
- All contributors and testers

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## ⚠️ Disclaimer

This is experimental software for amateur radio use only. Users are responsible for ensuring compliance with all applicable regulations in their jurisdiction. Always verify proper operation before transmitting.

---

*For questions or support, open an issue or contact the development team.*