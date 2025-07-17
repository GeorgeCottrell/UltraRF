# UltraRF Protocol Specification v0.1

## Table of Contents
1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [Physical Layer](#physical-layer)
4. [MAC Layer](#mac-layer)
5. [Network Layer](#network-layer)
6. [Frame Formats](#frame-formats)
7. [Regulatory Compliance](#regulatory-compliance)
8. [Implementation Notes](#implementation-notes)

## Introduction

The UltraRF protocol is designed to achieve maximum throughput within FCC Part 97 constraints for amateur radio SHF bands. This specification defines the technical implementation details for all protocol layers.

### Design Principles
- **Modularity**: Each layer can be upgraded independently
- **Efficiency**: Minimize overhead, maximize throughput
- **Adaptability**: Dynamic adjustment to RF conditions
- **Compliance**: Full FCC Part 97 regulatory compliance
- **Simplicity**: Implementable on affordable SDR hardware

## System Architecture

```
┌─────────────────────────────────────────┐
│          Application Layer              │
├─────────────────────────────────────────┤
│          Network Layer                  │
│    (BATMAN-inspired Mesh Routing)       │
├─────────────────────────────────────────┤
│          MAC Layer                      │
│    (TDMA with Dynamic Allocation)       │
├─────────────────────────────────────────┤
│          Physical Layer                 │
│    (OFDM + LDPC + Channel Bonding)     │
├─────────────────────────────────────────┤
│          RF Hardware                    │
│    (SDR + Frequency Converter)          │
└─────────────────────────────────────────┘
```

## Physical Layer

### Modulation Parameters

#### OFDM Configuration
- **FFT Size**: 64 points
- **Subcarriers**: 52 data, 4 pilot, 8 null (guard)
- **Subcarrier Spacing**: 1.5625 kHz
- **Symbol Duration**: 640 μs + 160 μs guard interval
- **Effective Symbol Rate**: 1250 symbols/second
- **Implemented in**: `src/physical/ofdm_modem.py`, `simulate/physical_layer.py`

#### Adaptive Modulation Schemes
| MCS Index | Modulation | Coding Rate | Bits/Symbol | Min SNR | Data Rate* |
|-----------|------------|-------------|-------------|---------|------------|
| 0         | BPSK       | 1/2         | 26          | 3 dB    | 32.5 kbps  |
| 1         | QPSK       | 1/2         | 52          | 5 dB    | 65 kbps    |
| 2         | QPSK       | 3/4         | 78          | 8 dB    | 97.5 kbps  |
| 3         | 16-QAM     | 1/2         | 104         | 12 dB   | 130 kbps   |
| 4         | 16-QAM     | 3/4         | 156         | 15 dB   | 195 kbps   |
| 5         | 64-QAM     | 2/3         | 208         | 20 dB   | 260 kbps   |
| 6         | 64-QAM     | 3/4         | 234         | 22 dB   | 292.5 kbps |
| 7         | 256-QAM    | 3/4         | 312         | 28 dB   | 390 kbps   |

*Per 100 kHz channel
- **Implemented in**: `src/physical/adaptive_modem.py`, `simulate/physical_layer.py`

### Forward Error Correction

#### LDPC Configuration
- **Code Length**: 1944 bits
- **Code Rates**: 1/2, 2/3, 3/4, 5/6
- **Decoding**: Sum-product algorithm
- **Iterations**: 50 maximum
- **Early Termination**: Syndrome check
- **Implemented in**: `src/physical/ldpc_codec.py` (interface, ready for real code)

### Channel Bonding

#### Bonding Modes
1. **Contiguous**: Adjacent 100 kHz channels
2. **Non-contiguous**: Separated channels with independent fading

#### Channel Allocation
```
10 GHz Band Example:
Ch1: 10.100 - 10.200 MHz
Ch2: 10.200 - 10.300 MHz
...
Ch50: 10.4900 - 10.5000 MHz

Maximum Channels: 50 (5 MHz aggregate)
Maximum Throughput: 19.5 Mbps @ MCS7
```
- **Implemented in**: `src/physical/channel_bonding.py`

### Pilot Signals
- **Pattern**: Scattered pilots at subcarriers -21, -7, 7, 21
- **Sequence**: Zadoff-Chu sequence for channel estimation
- **Power**: +3 dB boost relative to data subcarriers
- **Implemented in**: `simulate/physical_layer.py`

## MAC Layer

### TDMA Frame Structure

```
┌──────────────────────────────────────────────────┐
│                  Superframe (100 ms)             │
├────────┬────────┬────────┬────────┬─────────────┤
│ Beacon │ Slot 1 │ Slot 2 │  ...   │   Slot N    │
│ (5 ms) │ (5 ms) │ (5 ms) │        │   (5 ms)    │
└────────┴────────┴────────┴────────┴─────────────┘
```

#### Beacon Slot
- **Duration**: 5 ms
- **Content**: Network ID, timing reference, slot allocation map
- **Transmission**: By elected coordinator node
- **Format**: QPSK 1/2 for maximum reliability

#### Data Slots
- **Duration**: 5 ms each
- **Allocation**: Dynamic based on traffic demand
- **Guard Time**: 100 μs between slots
- **Content**: User data + MAC headers

### Channel Access

#### Slot Request Procedure
1. New node listens for beacon
2. Sends join request in designated contention slot
3. Coordinator allocates slots based on QoS requirements
4. Node acknowledges allocation

#### QoS Classes
| Priority | Class | Application | Slot Guarantee |
|----------|-------|-------------|----------------|
| 0        | Emergency | Life safety | 100% |
| 1        | Voice | Real-time audio | 80% |
| 2        | Video | Streaming | 60% |
| 3        | Data | File transfer | Best effort |

### Station Identification
- **Method**: Digital packet every 10 minutes
- **Format**: ASCII callsign in beacon slot
- **Encoding**: QPSK 1/2 with triple redundancy

## Network Layer

### Routing Protocol

#### BATMAN-RF Modifications
- **Metric**: Composite of SNR, packet loss, and latency
- **OGM Interval**: 1 second (adjustable)
- **Window Size**: 64 packets for link quality
- **TTL**: 32 hops maximum

#### Routing Metric Calculation
```
link_quality = (1 - packet_loss) * snr_factor * latency_factor

where:
  snr_factor = min(1.0, snr_db / 30.0)
  latency_factor = max(0.1, 1.0 - (latency_ms / 100.0))
```

### Mesh Services

#### Auto-configuration
- **IPv6**: Link-local addresses from MAC
- **IPv4**: Optional DHCP relay
- **DNS**: Multicast DNS for name resolution

#### Multi-path Support
- **Primary Path**: Highest metric route
- **Backup Paths**: Top 3 alternatives maintained
- **Load Balancing**: Round-robin for equal-cost paths

## Frame Formats

### Physical Layer Frame

```
┌─────────┬─────────┬─────────┬──────────┬─────────┐
│Preamble │ PLCP    │ Header  │ Payload  │   FCS   │
│(320 μs) │ Header  │ (CRC16) │(variable)│ (CRC32) │
│         │ (80 μs) │         │          │         │
└─────────┴─────────┴─────────┴──────────┴─────────┘
```

#### Preamble
- **Short Training**: 10 repetitions of 16 samples
- **Long Training**: 2 repetitions of 64 samples
- **Purpose**: AGC, timing, frequency synchronization

#### PLCP Header
- **Length**: 4 bytes
- **Fields**: MCS (3 bits), Length (12 bits), Reserved (17 bits)
- **Encoding**: BPSK 1/2 (most robust)

### MAC Layer Frame

```
┌─────────┬─────────┬─────────┬──────────┬─────────┐
│Frame    │ Duration│ Address │ Sequence │ Payload │
│Control  │   ID    │ Fields  │ Control  │         │
│(2 bytes)│(2 bytes)│(18 bytes)│(2 bytes) │(0-2304) │
└─────────┴─────────┴─────────┴──────────┴─────────┘
```

#### Frame Control
- **Type**: 2 bits (Management, Control, Data)
- **Subtype**: 4 bits
- **To DS/From DS**: Mesh routing flags
- **Retry**: Retransmission indicator
- **Power Management**: Sleep mode support

### Network Layer Packet

```
┌─────────┬─────────┬─────────┬──────────┬─────────┐
│ Version │ Type    │  TTL    │ Sequence │ Payload │
│(4 bits) │(4 bits) │(8 bits) │(16 bits) │         │
└─────────┴─────────┴─────────┴──────────┴─────────┘
```

## Regulatory Compliance

### Bandwidth Compliance
- **Channel Width**: 100 kHz maximum (99 kHz occupied)
- **Spectral Mask**: -26 dB at ±150 kHz offset
- **Adjacent Channel**: -40 dB rejection

### Power Control
- **Maximum Power**: 1500W PEP (per Part 97)
- **Automatic Level Control**: Maintain linear operation
- **Power Classes**: 1W, 10W, 100W, 1500W

### Spurious Emissions
- **Standard**: "Greatest extent practicable"
- **Target**: -60 dBc out-of-band
- **Harmonics**: -40 dBc minimum

## Implementation Notes

### Hardware Requirements
- **ADC Resolution**: 12-bit minimum, 16-bit preferred
- **Sample Rate**: 2 MSPS per 100 kHz channel
- **Processing**: ~1 GFLOPS per channel
- **Latency Budget**: <5 ms processing delay

### Software Architecture
```
Application API
     ↓
Network Stack (Linux kernel module)
     ↓
MAC Processor (User space daemon)
     ↓
PHY Engine (GNU Radio or custom DSP)
     ↓
SDR Driver (UHD, SoapySDR, etc.)
```

### Performance Optimization
- **SIMD**: Use AVX2/NEON for DSP operations
- **Threading**: Separate threads for TX/RX chains
- **Buffering**: Triple buffering for smooth streaming
- **GPU**: Optional OpenCL/CUDA acceleration

### Debugging Features
- **Test Modes**: Single carrier, fixed MCS
- **Loopback**: Digital and RF loopback
- **Monitoring**: SNR, BER, throughput metrics
- **Logging**: Configurable verbosity levels

## Appendices

### A. Channel Frequencies

#### 10 GHz Band (3 cm)
- **Range**: 10.000 - 10.500 GHz
- **Channels**: 500 (numbered 0-499)
- **Center Frequency**: 10.000 + (channel * 0.001) GHz

#### 24 GHz Band (1.25 cm)
- **Range**: 24.000 - 24.250 GHz
- **Channels**: 250 (numbered 0-249)
- **Center Frequency**: 24.000 + (channel * 0.001) GHz

### B. Timing Parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| Slot Time | 20 μs | Basic time unit |
| SIFS | 40 μs | Short interframe space |
| DIFS | 100 μs | Distributed coordination |
| Beacon Interval | 100 ms | Superframe period |
| Max Dwell | 400 ms | Regulatory limit |

### C. Error Codes

| Code | Description | Recovery Action |
|------|-------------|-----------------|
| 0x01 | CRC Failure | Request retransmission |
| 0x02 | Timeout | Increase timeout value |
| 0x03 | No Beacon | Scan other channels |
| 0x04 | Buffer Overflow | Reduce data rate |
| 0x05 | Invalid MCS | Fall back to QPSK |

---

*This specification is a living document. Version 0.1 - January 2025*