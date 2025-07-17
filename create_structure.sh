#!/bin/bash
# Create UltraRF project structure

echo "Creating UltraRF Protocol project structure..."

# Create main directories
mkdir -p src/ultrarf/{physical,mac,network,utils}
mkdir -p tests/{unit,integration,performance}
mkdir -p docs/{api,guides,hardware}
mkdir -p flowgraphs
mkdir -p fpga/{vivado,quartus}
mkdir -p tools
mkdir -p examples/{basic,advanced}
mkdir -p config
mkdir -p scripts

# Create __init__.py files for Python packages
touch src/ultrarf/__init__.py
touch src/ultrarf/physical/__init__.py
touch src/ultrarf/mac/__init__.py
touch src/ultrarf/network/__init__.py
touch src/ultrarf/utils/__init__.py
touch tests/__init__.py

# Create placeholder source files
cat > src/ultrarf/__init__.py << 'EOF'
"""
UltraRF Protocol - Ultra high-speed RF networking for amateur radio
"""

__version__ = "0.1.0"
__author__ = "UltraRF Contributors"

from .physical import OFDMModulator, OFDMDemodulator
from .mac import TDMAScheduler, FrameProcessor
from .network import MeshRouter, RoutingTable

__all__ = [
    "OFDMModulator",
    "OFDMDemodulator", 
    "TDMAScheduler",
    "FrameProcessor",
    "MeshRouter",
    "RoutingTable"
]
EOF

# Create basic physical layer module
cat > src/ultrarf/physical/ofdm.py << 'EOF'
"""
OFDM modulation and demodulation
"""

import numpy as np
from typing import Tuple, List, Optional

class OFDMModulator:
    """OFDM modulator for UltraRF protocol"""
    
    def __init__(self, n_subcarriers: int = 64, cp_length: int = 16):
        self.n_subcarriers = n_subcarriers
        self.cp_length = cp_length
        
    def modulate(self, symbols: np.ndarray) -> np.ndarray:
        """Apply OFDM modulation to input symbols"""
        # Implementation placeholder
        pass

class OFDMDemodulator:
    """OFDM demodulator for UltraRF protocol"""
    
    def __init__(self, n_subcarriers: int = 64, cp_length: int = 16):
        self.n_subcarriers = n_subcarriers
        self.cp_length = cp_length
        
    def demodulate(self, signal: np.ndarray) -> np.ndarray:
        """Demodulate OFDM signal"""
        # Implementation placeholder
        pass
EOF

# Create configuration template
cat > config/default.yaml << 'EOF'
# UltraRF Protocol Configuration

protocol:
  version: "0.1.0"
  
physical:
  # OFDM parameters
  n_subcarriers: 64
  cp_length: 16
  sample_rate: 2000000  # 2 MSPS
  
  # Modulation
  default_mcs: 4  # 16-QAM 3/4
  adaptive_mcs: true
  
mac:
  # TDMA parameters
  superframe_duration: 100  # ms
  slot_duration: 5  # ms
  beacon_interval: 100  # ms
  
  # QoS
  qos_enabled: true
  emergency_priority: 0
  
network:
  # Routing
  protocol: "batman-rf"
  metric: "composite"  # snr, loss, latency
  max_hops: 32
  
station:
  callsign: "NOCALL"
  grid_square: "DM79"
  
hardware:
  sdr: "plutosdr"  # plutosdr, bladerf, usrp
  frequency: 10100000000  # 10.1 GHz
  tx_gain: 0  # dB
  rx_gain: 30  # dB
EOF

# Create test framework
cat > tests/test_physical.py << 'EOF'
"""
Physical layer unit tests
"""

import pytest
import numpy as np
from ultrarf.physical import OFDMModulator, OFDMDemodulator

def test_ofdm_modulator_init():
    """Test OFDM modulator initialization"""
    mod = OFDMModulator(n_subcarriers=64, cp_length=16)
    assert mod.n_subcarriers == 64
    assert mod.cp_length == 16

def test_ofdm_loopback():
    """Test OFDM modulation/demodulation loopback"""
    # TODO: Implement when modulator/demodulator are complete
    pass
EOF

# Create CLI entry point
cat > src/ultrarf/cli.py << 'EOF'
"""
UltraRF Command Line Interface
"""

import click
import logging
from . import __version__

@click.group()
@click.version_option(version=__version__)
@click.option('--debug/--no-debug', default=False, help='Enable debug logging')
def cli(debug):
    """UltraRF Protocol - Ultra high-speed RF networking for amateur radio"""
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@cli.command()
@click.option('--config', '-c', default='config/default.yaml', help='Configuration file')
def beacon(config):
    """Start UltraRF beacon node"""
    click.echo(f"Starting beacon with config: {config}")
    # TODO: Implement beacon functionality

@cli.command()
@click.option('--config', '-c', default='config/default.yaml', help='Configuration file')
def node(config):
    """Start UltraRF mesh node"""
    click.echo(f"Starting mesh node with config: {config}")
    # TODO: Implement node functionality

@cli.command()
def monitor():
    """Start UltraRF network monitor"""
    click.echo("Starting network monitor...")
    # TODO: Implement monitoring functionality

def main():
    cli()

if __name__ == '__main__':
    main()
EOF

# Create development documentation
cat > docs/development.md << 'EOF'
# UltraRF Development Guide

## Setting Up the Development Environment

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install in development mode: `pip install -e .[dev]`
5. Run tests: `pytest`

## Code Style

- Follow PEP 8 (enforced by Black)
- Use type hints for all functions
- Write docstrings for all public APIs
- Maximum line length: 100 characters

## Testing

- Write unit tests for all new features
- Aim for >80% code coverage
- Run tests before submitting PRs
- Include integration tests for protocol features

## Git Workflow

1. Fork the repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "Add feature"`
4. Push to fork: `git push origin feature/your-feature`
5. Submit pull request

## Architecture Overview

The protocol consists of three main layers:

- **Physical Layer**: OFDM modulation, channel coding, RF interface
- **MAC Layer**: TDMA scheduling, QoS, channel access
- **Network Layer**: Mesh routing, addressing, management
EOF

# Create example notebook
cat > examples/basic/quickstart.py << 'EOF'
#!/usr/bin/env python3
"""
UltraRF Quick Start Example
"""

import numpy as np
from ultrarf.physical import OFDMModulator, OFDMDemodulator
from ultrarf.utils import calculate_snr, generate_qam_symbols

def main():
    print("UltraRF Protocol - Quick Start Example")
    print("=" * 40)
    
    # Create modulator/demodulator
    modulator = OFDMModulator(n_subcarriers=64, cp_length=16)
    demodulator = OFDMDemodulator(n_subcarriers=64, cp_length=16)
    
    # Generate random data
    n_symbols = 520  # 10 OFDM symbols worth
    data_symbols = generate_qam_symbols(n_symbols, modulation_order=16)
    
    print(f"Generated {n_symbols} 16-QAM symbols")
    
    # Modulate
    tx_signal = modulator.modulate(data_symbols)
    print(f"OFDM signal length: {len(tx_signal)} samples")
    
    # Add channel effects (simple AWGN for now)
    snr_db = 20
    noise_power = 10**(-snr_db/10)
    noise = np.sqrt(noise_power/2) * (np.random.randn(len(tx_signal)) + 
                                      1j * np.random.randn(len(tx_signal)))
    rx_signal = tx_signal + noise
    
    # Demodulate
    rx_symbols = demodulator.demodulate(rx_signal)
    
    # Calculate metrics
    evm = np.mean(np.abs(rx_symbols - data_symbols)**2)
    print(f"Error Vector Magnitude: {10*np.log10(evm):.2f} dB")
    
    print("\nQuick start complete!")
    print("Next: Try different modulation schemes and channel conditions")

if __name__ == "__main__":
    main()
EOF

# Create Makefile
cat > Makefile << 'EOF'
# UltraRF Protocol Makefile

.PHONY: help install dev test lint format clean docs

help:
	@echo "UltraRF Protocol Development Commands:"
	@echo "  make install    Install dependencies"
	@echo "  make dev        Install with development dependencies"
	@echo "  make test       Run tests"
	@echo "  make lint       Run linters"
	@echo "  make format     Format code with black"
	@echo "  make docs       Build documentation"
	@echo "  make clean      Clean build artifacts"

install:
	pip install -r requirements.txt

dev:
	pip install -e .[dev,docs,sdr]

test:
	pytest tests/ -v --cov=ultrarf --cov-report=term-missing

lint:
	flake8 src/ tests/
	mypy src/

format:
	black src/ tests/

docs:
	cd docs && sphinx-build -b html . _build/html

clean:
	rm -rf build/ dist/ *.egg-