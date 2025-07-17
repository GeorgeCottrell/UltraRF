# Hardware Setup Guide

This guide describes recommended hardware for UltraRF operation.

## Minimum Setup
- SDR: PlutoSDR or equivalent
- Converter: 10 GHz downconverter
- Antenna: 18 dBi dish or horn
- Computer: Raspberry Pi 4 or laptop

## Recommended Setup
- SDR: BladeRF 2.0 micro
- Converter: Kuhne Electronic MKU 10 G3
- Antenna: 24 dBi parabolic dish
- Computer: Desktop with GPU

## SDR Software Setup

- **Python 3.8+** and required packages (see `requirements.txt`)
- **GNU Radio 3.10+** for real-time SDR prototyping
- **Simulation**: All protocol features can be tested in software without hardware using the provided simulation scripts (`simulate/physical_layer.py`, `simulate/protocol_sim.py`).

See the README for more details and instructions on running simulations and tests.
