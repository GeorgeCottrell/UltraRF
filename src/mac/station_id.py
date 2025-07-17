"""
UltraRF Station Identification
Implements digital callsign beaconing every 10 minutes.
"""
import time

class StationID:
    def __init__(self, callsign):
        self.callsign = callsign
        self.last_sent = 0

    def should_send(self):
        now = time.time()
        if now - self.last_sent > 600:
            self.last_sent = now
            return True
        return False

    def get_id_frame(self):
        return self.callsign.encode('ascii')
