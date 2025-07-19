"""
Mesh Networking Module for UltraRF

Implements BATMAN-inspired mesh routing for emergency communications.
Provides automatic route discovery, load balancing, and failover.
"""

import logging
import time
import threading
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json

logger = logging.getLogger(__name__)

class RouteMetric(Enum):
    """Route quality metrics"""
    EXCELLENT = 1
    GOOD = 2  
    FAIR = 3
    POOR = 4
    UNREACHABLE = 5

@dataclass
class MeshNode:
    """Mesh network node information"""
    callsign: str
    node_id: str
    last_seen: float
    hop_count: int = 0
    signal_strength: float = 0.0
    battery_level: Optional[float] = None
    is_gateway: bool = False
    routes: Dict[str, 'RouteInfo'] = field(default_factory=dict)

@dataclass  
class RouteInfo:
    """Routing information for mesh network"""
    destination: str
    next_hop: str
    hop_count: int
    metric: RouteMetric
    last_updated: float
    bandwidth_estimate: float = 0.0

class MeshNetwork:
    """
    Mesh networking implementation for UltraRF
    
    Provides automatic route discovery, maintenance, and load balancing
    across multiple RF channels for emergency communications.
    """
    
    def __init__(self, local_callsign: str):
        self.local_callsign = local_callsign
        self.local_node_id = f"{local_callsign}-{int(time.time())}"
        
        self.nodes: Dict[str, MeshNode] = {}
        self.routing_table: Dict[str, RouteInfo] = {}
        self.neighbor_nodes: Set[str] = set()
        
        self.route_update_interval = 30.0  # seconds
        self.node_timeout = 180.0  # seconds
        self.max_hop_count = 5
        
        self.lock = threading.Lock()
        self.running = False
        self.maintenance_thread = None
        
        logger.info(f"Mesh network initialized for {local_callsign}")
    
    def start(self):
        """Start mesh network operations"""
        with self.lock:
            if self.running:
                return
            
            self.running = True
            self.maintenance_thread = threading.Thread(
                target=self._maintenance_loop,
                daemon=True
            )
            self.maintenance_thread.start()
            
        logger.info("Mesh network started")
    
    def stop(self):
        """Stop mesh network operations"""
        with self.lock:
            self.running = False
            
        if self.maintenance_thread:
            self.maintenance_thread.join(timeout=5.0)
            
        logger.info("Mesh network stopped")
    
    def add_neighbor(self, callsign: str, node_id: str, signal_strength: float):
        """Add or update a neighbor node"""
        with self.lock:
            node = MeshNode(
                callsign=callsign,
                node_id=node_id,
                last_seen=time.time(),
                hop_count=1,
                signal_strength=signal_strength
            )
            
            self.nodes[node_id] = node
            self.neighbor_nodes.add(node_id)
            
            # Add direct route
            route = RouteInfo(
                destination=node_id,
                next_hop=node_id,
                hop_count=1,
                metric=self._calculate_metric(signal_strength, 1),
                last_updated=time.time(),
                bandwidth_estimate=self._estimate_bandwidth(signal_strength)
            )
            
            self.routing_table[node_id] = route
            
        logger.info(f"Added neighbor {callsign} ({node_id}) with signal {signal_strength:.2f}")
    
    def process_route_announcement(self, from_node: str, routes: List[Dict]):
        """Process route announcements from other nodes"""
        with self.lock:
            current_time = time.time()
            
            for route_data in routes:
                destination = route_data['destination']
                hop_count = route_data['hop_count'] + 1  # Add one hop
                
                # Skip if too many hops
                if hop_count > self.max_hop_count:
                    continue
                
                # Skip routes to ourselves
                if destination == self.local_node_id:
                    continue
                
                # Calculate metric for this route
                signal_strength = route_data.get('signal_strength', 0.0)
                metric = self._calculate_metric(signal_strength, hop_count)
                
                # Check if this is a better route
                existing_route = self.routing_table.get(destination)
                if existing_route is None or self._is_better_route(metric, hop_count, existing_route):
                    
                    new_route = RouteInfo(
                        destination=destination,
                        next_hop=from_node,
                        hop_count=hop_count,
                        metric=metric,
                        last_updated=current_time,
                        bandwidth_estimate=self._estimate_bandwidth(signal_strength)
                    )
                    
                    self.routing_table[destination] = new_route
                    
                    logger.debug(f"Updated route to {destination} via {from_node} "
                               f"({hop_count} hops, metric: {metric.name})")
    
    def find_route(self, destination: str) -> Optional[RouteInfo]:
        """Find the best route to a destination"""
        with self.lock:
            return self.routing_table.get(destination)
    
    def get_next_hop(self, destination: str) -> Optional[str]:
        """Get the next hop for a destination"""
        route = self.find_route(destination)
        return route.next_hop if route else None
    
    def get_route_announcements(self) -> List[Dict]:
        """Get routes to announce to neighbors"""
        with self.lock:
            announcements = []
            
            for destination, route in self.routing_table.items():
                # Don't announce routes that are too old
                if time.time() - route.last_updated > self.route_update_interval * 2:
                    continue
                
                announcement = {
                    'destination': destination,
                    'hop_count': route.hop_count,
                    'metric': route.metric.value,
                    'signal_strength': route.bandwidth_estimate,
                    'timestamp': route.last_updated
                }
                announcements.append(announcement)
            
            return announcements
    
    def get_mesh_status(self) -> Dict:
        """Get current mesh network status"""
        with self.lock:
            current_time = time.time()
            
            # Count active nodes
            active_nodes = sum(1 for node in self.nodes.values() 
                             if current_time - node.last_seen < self.node_timeout)
            
            # Count routes by metric
            route_metrics = {}
            for route in self.routing_table.values():
                metric_name = route.metric.name
                route_metrics[metric_name] = route_metrics.get(metric_name, 0) + 1
            
            return {
                'local_node': {
                    'callsign': self.local_callsign,
                    'node_id': self.local_node_id
                },
                'network_stats': {
                    'total_nodes': len(self.nodes),
                    'active_nodes': active_nodes,
                    'neighbor_count': len(self.neighbor_nodes),
                    'route_count': len(self.routing_table),
                    'route_metrics': route_metrics
                },
                'running': self.running,
                'timestamp': current_time
            }
    
    def _maintenance_loop(self):
        """Background maintenance for mesh network"""
        while self.running:
            try:
                self._cleanup_stale_routes()
                self._cleanup_stale_nodes()
                time.sleep(self.route_update_interval / 3)
                
            except Exception as e:
                logger.error(f"Mesh maintenance error: {e}")
                time.sleep(5.0)
    
    def _cleanup_stale_routes(self):
        """Remove stale routes from routing table"""
        with self.lock:
            current_time = time.time()
            stale_routes = []
            
            for destination, route in self.routing_table.items():
                if current_time - route.last_updated > self.route_update_interval * 3:
                    stale_routes.append(destination)
            
            for destination in stale_routes:
                del self.routing_table[destination]
                logger.debug(f"Removed stale route to {destination}")
    
    def _cleanup_stale_nodes(self):
        """Remove stale nodes from node list"""
        with self.lock:
            current_time = time.time()
            stale_nodes = []
            
            for node_id, node in self.nodes.items():
                if current_time - node.last_seen > self.node_timeout:
                    stale_nodes.append(node_id)
            
            for node_id in stale_nodes:
                del self.nodes[node_id]
                self.neighbor_nodes.discard(node_id)
                logger.info(f"Removed stale node {node_id}")
    
    def _calculate_metric(self, signal_strength: float, hop_count: int) -> RouteMetric:
        """Calculate route metric based on signal strength and hop count"""
        # Adjust signal strength for hop count penalty
        adjusted_strength = signal_strength * (0.8 ** (hop_count - 1))
        
        if adjusted_strength > 0.8:
            return RouteMetric.EXCELLENT
        elif adjusted_strength > 0.6:
            return RouteMetric.GOOD
        elif adjusted_strength > 0.4:
            return RouteMetric.FAIR
        elif adjusted_strength > 0.2:
            return RouteMetric.POOR
        else:
            return RouteMetric.UNREACHABLE
    
    def _estimate_bandwidth(self, signal_strength: float) -> float:
        """Estimate available bandwidth based on signal strength"""
        # Simple linear estimation (in Mbps)
        return max(0.1, signal_strength * 50.0)
    
    def _is_better_route(self, new_metric: RouteMetric, new_hop_count: int, 
                        existing_route: RouteInfo) -> bool:
        """Determine if a new route is better than existing one"""
        # Better metric wins
        if new_metric.value < existing_route.metric.value:
            return True
        
        # Same metric, fewer hops wins
        if (new_metric.value == existing_route.metric.value and 
            new_hop_count < existing_route.hop_count):
            return True
        
        return False

# Global mesh network instance
_mesh_instance = None

def get_mesh_instance(callsign: str = None) -> MeshNetwork:
    """Get the global mesh network instance"""
    global _mesh_instance
    if _mesh_instance is None and callsign:
        _mesh_instance = MeshNetwork(callsign)
    return _mesh_instance
