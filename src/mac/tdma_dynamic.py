"""
UltraRF Dynamic TDMA MAC (Phase 2 prototype)
Supports dynamic slot allocation and QoS classes.
"""
class DynamicTDMA:
    def __init__(self, num_slots=10):
        self.num_slots = num_slots
        self.slots = [None] * num_slots
        self.qos = [None] * num_slots

    def request_slot(self, node_id, qos_class):
        # Prioritize lower qos_class (higher priority)
        for i in range(self.num_slots):
            if self.slots[i] is None:
                self.slots[i] = node_id
                self.qos[i] = qos_class
                return i
        # Preempt lowest priority if new request is higher priority
        min_qos = max(self.qos)
        if qos_class < min_qos:
            idx = self.qos.index(min_qos)
            self.slots[idx] = node_id
            self.qos[idx] = qos_class
            return idx
        return -1

    def release_slot(self, node_id):
        for i in range(self.num_slots):
            if self.slots[i] == node_id:
                self.slots[i] = None
                self.qos[i] = None
                return True
        return False
