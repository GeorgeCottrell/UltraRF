"""
UltraRF QoS Manager
Implements slot guarantees for different traffic classes.
"""
class QoSManager:
    def __init__(self):
        self.classes = {
            0: 'Emergency',
            1: 'Voice',
            2: 'Video',
            3: 'Data'
        }
        self.guarantees = {
            0: 1.0,
            1: 0.8,
            2: 0.6,
            3: 0.0
        }

    def get_guarantee(self, qos_class):
        return self.guarantees.get(qos_class, 0.0)
