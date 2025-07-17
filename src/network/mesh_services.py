"""
UltraRF Mesh Services
Implements auto-configuration, multi-path, and load balancing.
"""
class MeshServices:
    def __init__(self):
        self.paths = {}

    def add_path(self, dest, path):
        if dest not in self.paths:
            self.paths[dest] = []
        self.paths[dest].append(path)

    def get_primary(self, dest):
        if dest in self.paths and self.paths[dest]:
            return self.paths[dest][0]
        return None

    def get_backups(self, dest):
        if dest in self.paths:
            return self.paths[dest][1:4]
        return []

    def load_balance(self, dest):
        if dest in self.paths and self.paths[dest]:
            # Round-robin
            path = self.paths[dest].pop(0)
            self.paths[dest].append(path)
            return path
        return None
