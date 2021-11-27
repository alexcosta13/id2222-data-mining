import random


class TriestImpr:
    def __init__(self, M):
        assert M >= 6, "M has to be >= 6"
        self.t = 0
        self.S = set()
        self.M = M
        self.tau = 0
        self.tau_local = {}

    def sample_edge(self):
        if self.t <= self.M:
            return True
        elif random.uniform(0, 1) < (self.M / self.t):
            edge = random.choice(tuple(self.S))
            self.S -= {edge}
            return True
        return False

    def get_common_neighbors(self, edge):
        neigh_u, neigh_v = set(), set()
        u, v = edge
        for elem in self.S:
            if u in elem:
                neigh_u |= set(elem) - {u}
            if v in elem:
                neigh_v |= set(elem) - {v}
        return neigh_u & neigh_v

    def update_counters(self, edge):
        neighbors = self.get_common_neighbors(edge)
        eta = max(1, ((self.t - 1) * (self.t - 2)) / (self.M * (self.M - 1)))
        for neighbor in neighbors:
            self.tau += eta
            self.tau_local[neighbor] = self.tau_local.get(neighbor, 0) + eta
            self.tau_local[edge[0]] = self.tau_local.get(edge[0], 0) + eta
            self.tau_local[edge[1]] = self.tau_local.get(edge[1], 0) + eta

    def process_sample(self, edge):
        self.t += 1
        self.update_counters(edge)
        if self.sample_edge():
            self.S |= {edge}

    def get_triangle_count(self):
        return self.tau