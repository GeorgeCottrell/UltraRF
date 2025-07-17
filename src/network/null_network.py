"""
UltraRF Null Network Layer (Phase 1 prototype)
No mesh routing; direct point-to-point only.
"""
class NullNetwork:
    def route(self, data):
        """Directly pass data to MAC layer (no routing)."""
        return data
