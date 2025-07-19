"""
UltraRF Python Package

This package provides the Python implementation of the UltraRF protocol
for high-speed amateur radio communications with channel bonding and mesh networking.
"""

from .ultrarf_protocol import (
    UltraRFProtocol,
    ChannelConfig,
    NodeInfo,
    TransmissionResult,
    ModulationType,
    configure_channel,
    enable_bonding,
    send_directed,
    broadcast,
    emergency_broadcast,
    health_check,
    get_average_latency,
    get_packet_loss_rate,
    get_protocol_instance
)

__version__ = "2.0.0"
__author__ = "OffGridComm Development Team"
__license__ = "GPL-3.0"

__all__ = [
    "UltraRFProtocol",
    "ChannelConfig", 
    "NodeInfo",
    "TransmissionResult",
    "ModulationType",
    "configure_channel",
    "enable_bonding", 
    "send_directed",
    "broadcast",
    "emergency_broadcast",
    "health_check",
    "get_average_latency",
    "get_packet_loss_rate",
    "get_protocol_instance"
]
