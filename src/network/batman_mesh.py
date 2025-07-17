"""
UltraRF BATMAN-inspired Mesh Routing (Phase 2 prototype)
Implements basic mesh routing metric and path selection.
"""
class BatmanMesh:
    def __init__(self):
        self.neighbors = {}

    def update_link(self, neighbor, snr, packet_loss, latency):
        metric = (1 - packet_loss) * min(1.0, snr / 30.0) * max(0.1, 1.0 - (latency / 100.0))
        self.neighbors[neighbor] = metric

    def best_neighbor(self):
        if not self.neighbors:
            return None
        return max(self.neighbors, key=self.neighbors.get)

    def route_packet(self, packet):
        # Placeholder: forward to best neighbor
        return self.best_neighbor()
