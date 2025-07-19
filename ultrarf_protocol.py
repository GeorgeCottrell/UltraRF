from enum import Enum
import math
# Add ServiceType for service-aware routing
class ServiceType(Enum):
    REALTIME = "realtime"  # chat, audio, video
    BULK = "bulk"          # file transfer, large data
"""
UltraRF Protocol Module

High-speed amateur radio protocol implementation for OffGridComm.
Supports channel bonding, adaptive modulation, and mesh networking.

Author: OffGridComm Development Team
License: GPL-3.0
"""

import logging
import json
import time
import threading
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import lz4.frame

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModulationType(Enum):
    """RF modulation types supported by UltraRF"""
    OFDM = "ofdm"
    QAM64 = "qam64"
    QAM256 = "qam256"
    BPSK = "bpsk"
    QPSK = "qpsk"

@dataclass
class ChannelConfig:
    """Configuration for a single RF channel"""
    frequency: float  # Hz
    bandwidth: float  # Hz
    modulation: str
    power: float  # Watts
    active: bool = False

@dataclass
class NodeInfo:
    """Information about a network node"""
    callsign: str
    node_id: str
    last_seen: float
    signal_strength: float
    distance: Optional[float] = None

@dataclass
class TransmissionResult:
    """Result of a transmission attempt"""
    transmission_id: str
    success: bool
    latency_ms: float
    retry_count: int = 0

class UltraRFProtocol:
    def send_packet(self, target_node: str, message: bytes, transmission_id: str, service_type: ServiceType) -> bool:
        """
        Send a packet using service-aware routing.
        Args:
            target_node (str): Destination node.
            message (bytes): Data to send.
            transmission_id (str): Unique ID.
            service_type (ServiceType): Type of service.
        Returns:
            bool: Success.
        """
        if service_type == ServiceType.REALTIME:
            return self._send_realtime(target_node, message, transmission_id)
        elif service_type == ServiceType.BULK:
            return self._send_bulk(target_node, message, transmission_id)
        else:
            logger.error("Unknown service type")
            return False

    def _send_realtime(self, target_node, message, transmission_id):
        """
        Direct mesh routing, minimal hops, low latency for real-time traffic.
        """
        # Compress message for RF
        compressed_message = compress_data(message)
        # Simulate direct mesh transmission
        success = self._simulate_transmission()
        latency = 10 + math.ceil(len(compressed_message) / 1000)  # Simulated low latency
        result = TransmissionResult(
            transmission_id=transmission_id,
            success=success,
            latency_ms=latency
        )
        with self.lock:
            self.transmission_history.append(result)
            self.total_transmissions += 1
            if success:
                self.successful_transmissions += 1
            self.total_latency += latency
        logger.info(f"Real-time transmission to {target_node}: {'SUCCESS' if success else 'FAILED'} ({latency}ms, compressed size: {len(compressed_message)} bytes)")
        return success

    def _send_bulk(self, target_node, message, transmission_id):
        """
        Swarm-style chunked transfer for bulk/file data.
        """
        chunk_size = 2048
        chunks = [message[i:i+chunk_size] for i in range(0, len(message), chunk_size)]
        all_success = True
        for idx, chunk in enumerate(chunks):
            chunk_id = f"{transmission_id}-chunk{idx}"
            compressed_chunk = compress_data(chunk)
            # Simulate swarm relay (multiple relays, higher reliability)
            success = self._simulate_transmission(priority=True)
            latency = 30 + math.ceil(len(compressed_chunk) / 1000)  # Simulated higher latency
            result = TransmissionResult(
                transmission_id=chunk_id,
                success=success,
                latency_ms=latency
            )
            with self.lock:
                self.transmission_history.append(result)
                self.total_transmissions += 1
                if success:
                    self.successful_transmissions += 1
                self.total_latency += latency
            logger.info(f"Bulk chunk {idx+1}/{len(chunks)} to {target_node}: {'SUCCESS' if success else 'FAILED'} ({latency}ms, compressed size: {len(compressed_chunk)} bytes)")
            if not success:
                all_success = False
        return all_success
    """
    Main UltraRF protocol implementation
    
    Provides high-speed RF communication with channel bonding,
    adaptive modulation, and mesh networking capabilities.
    """
    
    def __init__(self):
        self.channels: Dict[str, ChannelConfig] = {}
        self.bonded_channels: List[str] = []
        self.nodes: Dict[str, NodeInfo] = {}
        self.transmission_history: List[TransmissionResult] = []
        self.is_initialized = False
        self.lock = threading.Lock()
        
        # Performance metrics
        self.total_transmissions = 0
        self.successful_transmissions = 0
        self.total_latency = 0.0
        
        logger.info("UltraRF Protocol initialized")
    
    def configure_channel(self, channel_id: str, config: Dict[str, Any]) -> bool:
        """Configure a single RF channel"""
        try:
            with self.lock:
                channel_config = ChannelConfig(
                    frequency=float(config['frequency']),
                    bandwidth=float(config['bandwidth']),
                    modulation=str(config['modulation']),
                    power=float(config['power'])
                )
                
                self.channels[channel_id] = channel_config
                
                logger.info(f"Configured channel {channel_id}: "
                          f"{channel_config.frequency/1e6:.3f} MHz, "
                          f"{channel_config.modulation}, "
                          f"{channel_config.power}W")
                return True
                
        except Exception as e:
            logger.error(f"Failed to configure channel {channel_id}: {e}")
            return False
    
    def enable_bonding(self, channel_ids: List[str]) -> bool:
        """Enable channel bonding for multiple channels"""
        try:
            with self.lock:
                # Validate all channels exist
                for channel_id in channel_ids:
                    if channel_id not in self.channels:
                        logger.error(f"Channel {channel_id} not found for bonding")
                        return False
                
                self.bonded_channels = channel_ids.copy()
                
                # Activate bonded channels
                for channel_id in channel_ids:
                    self.channels[channel_id].active = True
                
                logger.info(f"Enabled bonding for {len(channel_ids)} channels")
                return True
                
        except Exception as e:
            logger.error(f"Failed to enable channel bonding: {e}")
            return False
    
    # Legacy API for FFI compatibility
    def send_directed(self, target_node: str, message: str, transmission_id: str) -> bool:
        """Send a directed message to a specific node (with compression)
        Args:
            target_node (str): Destination node.
            message (str): Message content (string).
            transmission_id (str): Unique transmission ID.
        Returns:
            bool: Success.
        """
        return self.send_packet(target_node, message.encode('utf-8'), transmission_id, ServiceType.REALTIME)

    def broadcast(self, message: str, transmission_id: str) -> bool:
        """Broadcast a message to all nodes (with compression)
        Args:
            message (str): Message content (string).
            transmission_id (str): Unique transmission ID.
        Returns:
            bool: Success.
        """
        return self.send_packet("BROADCAST", message.encode('utf-8'), transmission_id, ServiceType.REALTIME)

    def emergency_broadcast(self, channel_id: str, message: str, transmission_id: str) -> bool:
        """Send emergency broadcast on specific channel (with compression)
        Args:
            channel_id (str): Channel to broadcast on.
            message (str): Message content (string).
            transmission_id (str): Unique transmission ID.
        Returns:
            bool: Success.
        """
        # For emergency, treat as real-time for lowest latency
        return self.send_packet(channel_id, message.encode('utf-8'), transmission_id, ServiceType.REALTIME)
    def send_file(self, target_node: str, file_bytes: bytes, transmission_id: str) -> bool:
        """
        Send a file using swarm-style bulk transfer.
        Args:
            target_node (str): Destination node.
            file_bytes (bytes): File data.
            transmission_id (str): Unique transmission ID.
        Returns:
            bool: Success.
        """
        return self.send_packet(target_node, file_bytes, transmission_id, ServiceType.BULK)
    
    def health_check(self) -> str:
        """Get system health information"""
        try:
            with self.lock:
                health_data = {
                    "status": "healthy" if self.is_initialized else "initializing",
                    "channels_configured": len(self.channels),
                    "bonded_channels": len(self.bonded_channels),
                    "active_nodes": len(self.nodes),
                    "total_transmissions": self.total_transmissions,
                    "success_rate": (self.successful_transmissions / max(1, self.total_transmissions)) * 100,
                    "average_latency_ms": self.get_average_latency(),
                    "packet_loss_rate": self.get_packet_loss_rate(),
                    "timestamp": time.time()
                }
            
            return json.dumps(health_data)
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return json.dumps({"status": "error", "message": str(e)})
    
    def get_average_latency(self) -> float:
        """Get average transmission latency in milliseconds"""
        try:
            with self.lock:
                if self.total_transmissions == 0:
                    return 0.0
                return self.total_latency / self.total_transmissions
                
        except Exception as e:
            logger.error(f"Failed to get average latency: {e}")
            return 0.0
    
    def get_packet_loss_rate(self) -> float:
        """Get packet loss rate as percentage"""
        try:
            with self.lock:
                if self.total_transmissions == 0:
                    return 0.0
                
                failed_transmissions = self.total_transmissions - self.successful_transmissions
                return (failed_transmissions / self.total_transmissions) * 100
                
        except Exception as e:
            logger.error(f"Failed to get packet loss rate: {e}")
            return 0.0
    
    def _simulate_transmission(self, priority: bool = False) -> bool:
        """
        Simulate RF transmission with realistic success rates
        
        In a real implementation, this would interface with actual RF hardware.
        """
        import random
        
        # Base success rate
        base_success_rate = 0.95 if priority else 0.90
        
        # Factor in channel bonding (more channels = higher reliability)
        if len(self.bonded_channels) > 1:
            bonding_bonus = min(0.05, len(self.bonded_channels) * 0.01)
            base_success_rate += bonding_bonus
        
        # Add some randomness for realistic simulation
        return random.random() < base_success_rate

def compress_data(data: bytes) -> bytes:
    """Compress data using LZ4 (fast, low overhead, not obfuscating)"""
    return lz4.frame.compress(data)


def decompress_payload(payload: bytes) -> bytes:
    """
    Decompresses an LZ4-compressed payload.
    Returns decompressed bytes, or empty bytes on failure.
    """
    try:
        return lz4.frame.decompress(payload)
    except lz4.frame.LZ4FrameError as e:
        logger.error(f"LZ4 decompression failed: {e}")
        return b''
    def receive_directed(self, rf_packet: bytes):
        decompressed = decompress_payload(rf_packet)
        if not decompressed:
            logger.warning("Directed packet decompression failed, dropping packet.")
            return
        # ...existing code to parse/process decompressed...

    def receive_broadcast(self, rf_packet: bytes):
        decompressed = decompress_payload(rf_packet)
        if not decompressed:
            logger.warning("Broadcast packet decompression failed, dropping packet.")
            return
        # ...existing code to parse/process decompressed...

    def receive_emergency(self, rf_packet: bytes):
        decompressed = decompress_payload(rf_packet)
        if not decompressed:
            logger.warning("Emergency packet decompression failed, dropping packet.")
            return
        # ...existing code to parse/process decompressed...

# Global protocol instance
_protocol_instance = None

def get_protocol_instance() -> UltraRFProtocol:
    """Get the global protocol instance"""
    global _protocol_instance
    if _protocol_instance is None:
        _protocol_instance = UltraRFProtocol()
    return _protocol_instance

# Module-level functions that Rust will call
def configure_channel(channel_id: str, config: Dict[str, Any]) -> bool:
    """Configure a channel (module-level function)"""
    return get_protocol_instance().configure_channel(channel_id, config)

def enable_bonding(channel_ids: List[str]) -> bool:
    """Enable channel bonding (module-level function)"""
    return get_protocol_instance().enable_bonding(channel_ids)

def send_directed(target_node: str, message: str, transmission_id: str) -> bool:
    """Send directed message (module-level function)
    Args:
        target_node (str): Destination node.
        message (str): Message content.
        transmission_id (str): Unique transmission ID.
    Returns:
        bool: Success.
    """
    return get_protocol_instance().send_directed(target_node, message, transmission_id)

def broadcast(message: str, transmission_id: str) -> bool:
    """Broadcast message (module-level function)
    Args:
        message (str): Message content.
        transmission_id (str): Unique transmission ID.
    Returns:
        bool: Success.
    """
    return get_protocol_instance().broadcast(message, transmission_id)

def emergency_broadcast(channel_id: str, message: str, transmission_id: str) -> bool:
    """Emergency broadcast (module-level function)
    Args:
        channel_id (str): Channel to broadcast on.
        message (str): Message content.
        transmission_id (str): Unique transmission ID.
    Returns:
        bool: Success.
    """
    return get_protocol_instance().emergency_broadcast(channel_id, message, transmission_id)
def send_file(target_node: str, file_bytes: bytes, transmission_id: str) -> bool:
    """
    Send file (module-level function)
    Args:
        target_node (str): Destination node.
        file_bytes (bytes): File data.
        transmission_id (str): Unique transmission ID.
    Returns:
        bool: Success.
    """
    return get_protocol_instance().send_file(target_node, file_bytes, transmission_id)

def health_check() -> str:
    """Health check (module-level function)"""
    return get_protocol_instance().health_check()

def get_average_latency() -> float:
    """Get average latency (module-level function)"""
    return get_protocol_instance().get_average_latency()

def get_packet_loss_rate() -> float:
    """Get packet loss rate (module-level function)"""
    return get_protocol_instance().get_packet_loss_rate()

# Initialize on import
logger.info("UltraRF Protocol module loaded")
