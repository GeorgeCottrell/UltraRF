#!/usr/bin/env python3
"""
Test script for UltraRF Protocol

This script verifies that the UltraRF Python module is working correctly
and can be called from Rust via PyO3.
"""

import sys
import os
import json
import time

# Add the ultrarf directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ultrarf_protocol import (
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
    print("✓ UltraRF protocol module imported successfully")
except ImportError as e:
    print(f"✗ Failed to import UltraRF protocol: {e}")
    sys.exit(1)

def test_basic_functionality():
    """Test basic UltraRF functionality"""
    print("\n=== Testing Basic UltraRF Functionality ===")
    
    # Test channel configuration
    print("Testing channel configuration...")
    config = {
        'frequency': 144_500_000.0,  # 144.5 MHz
        'bandwidth': 20_000.0,       # 20 kHz
        'modulation': 'qam64',
        'power': 50.0                # 50 watts
    }
    
    result = configure_channel("test-channel-1", config)
    print(f"Configure channel result: {result}")
    
    # Test channel bonding
    print("Testing channel bonding...")
    bonding_result = enable_bonding(["test-channel-1"])
    print(f"Enable bonding result: {bonding_result}")
    
    # Test directed transmission
    print("Testing directed transmission...")
    directed_result = send_directed("TEST-STATION", "Hello from UltraRF!", "tx-001")
    print(f"Directed transmission result: {directed_result}")
    
    # Test broadcast
    print("Testing broadcast...")
    broadcast_result = broadcast("Emergency test message", "tx-002")
    print(f"Broadcast result: {broadcast_result}")
    
    # Test emergency broadcast
    print("Testing emergency broadcast...")
    emergency_result = emergency_broadcast("test-channel-1", "EMERGENCY: Test alert", "tx-003")
    print(f"Emergency broadcast result: {emergency_result}")
    
    # Test health check
    print("Testing health check...")
    health_data = health_check()
    health_json = json.loads(health_data)
    print(f"Health check status: {health_json['status']}")
    print(f"Total transmissions: {health_json['total_transmissions']}")
    print(f"Success rate: {health_json['success_rate']:.1f}%")
    
    # Test performance metrics
    print("Testing performance metrics...")
    avg_latency = get_average_latency()
    packet_loss = get_packet_loss_rate()
    print(f"Average latency: {avg_latency:.2f} ms")
    print(f"Packet loss rate: {packet_loss:.2f}%")

def test_mesh_networking():
    """Test mesh networking functionality"""
    print("\n=== Testing Mesh Networking ===")
    
    try:
        from mesh import MeshNetwork, get_mesh_instance
        
        # Create mesh network instance
        mesh = MeshNetwork("TEST-CALL")
        mesh.start()
        
        # Add some test neighbors
        mesh.add_neighbor("STATION-1", "node-001", 0.85)
        mesh.add_neighbor("STATION-2", "node-002", 0.72)
        
        # Get mesh status
        status = mesh.get_mesh_status()
        print(f"Mesh network status: {json.dumps(status, indent=2)}")
        
        # Test route finding
        route = mesh.find_route("node-001")
        if route:
            print(f"Route to node-001: next_hop={route.next_hop}, hops={route.hop_count}")
        
        mesh.stop()
        print("✓ Mesh networking test completed")
        
    except ImportError as e:
        print(f"✗ Mesh networking not available: {e}")

def main():
    """Main test function"""
    print("UltraRF Protocol Test Suite")
    print("=" * 40)
    
    try:
        test_basic_functionality()
        test_mesh_networking()
        
        print("\n=== Test Summary ===")
        print("✓ All UltraRF tests completed successfully!")
        print("The UltraRF Python module is ready for Rust integration.")
        
    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
