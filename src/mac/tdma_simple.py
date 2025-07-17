"""
UltraRF Simple TDMA MAC (Phase 1 prototype)
Basic TDMA slot allocation for single-channel QPSK.
"""

class SimpleTDMA:
    def __init__(self, num_slots=10):
        self.num_slots = num_slots
        self.slots = [None] * num_slots

    def request_slot(self, node_id):
        # Assign first available slot
        for i in range(self.num_slots):
            if self.slots[i] is None:
                self.slots[i] = node_id
                return i
        return -1  # No slot available

    def get_slot_map(self):
        """Return current slot allocation map."""
        return list(self.slots)

    def release_slot(self, node_id):
        for i in range(self.num_slots):
            if self.slots[i] == node_id:
                self.slots[i] = None
                return True
        return False
