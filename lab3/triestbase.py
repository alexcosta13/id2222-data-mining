import random


class TriestBase:
    def __init__(self, M):
        """
        :param M: reservoir sample size
        """
        assert M >= 6, "M has to be >= 6"
        self.t = 0
        self.S = set()
        self.M = M
        self.tau = 0
        self.tau_local = {}

    def sample_edge(self):
        """
        Decides whether to include an incoming edge to the reservoir sample S. If and
        old sample is removed from S, the counters are updated accordingly.
        :return: boolean indicating whether S has been modified
        """
        if self.t <= self.M:
            return True
        elif random.uniform(0, 1) < (self.M / self.t):
            edge = random.choice(tuple(self.S))
            self.S -= {edge}
            self.update_counters(-1, edge)
            return True
        return False

    def get_common_neighbors(self, edge):
        """
        Helper function to update the counters.
        :param edge: new edge to be added in S
        :return: the number of common neighbors in S between the two vertices of the input edge
        """
        neigh_u, neigh_v = set(), set()
        u, v = edge
        for elem in self.S:
            if u in elem:
                neigh_u |= set(elem) - {u}
            if v in elem:
                neigh_v |= set(elem) - {v}
        return neigh_u & neigh_v

    def update_counters(self, sign, edge):
        """
        If the reservoir sample (S) is modified, triangle counts get updated.
        :param sign: +1/-1, tells whether an edge is added to or removed from S
        :param edge: the added or removed edge
        :return: None
        """
        neighbors = self.get_common_neighbors(edge)
        for neighbor in neighbors:
            self.tau += sign
            self.tau_local[neighbor] = self.tau_local.get(neighbor, 0) + sign
            self.tau_local[edge[0]] = self.tau_local.get(edge[0], 0) + sign
            self.tau_local[edge[1]] = self.tau_local.get(edge[1], 0) + sign

    def process_sample(self, edge):
        """
        Processes one sample (edge) from an incoming stream.
        :param edge: new incoming edge
        :return: None
        """
        self.t += 1
        if self.sample_edge():
            self.S |= {edge}
            self.update_counters(1, edge)

    def get_triangle_count(self):
        """
        Escales the triangle count (tau), following the formula in the paper.
        :return: estimated triangle count
        """
        xi = max(
            1,
            (self.t * (self.t - 1) * (self.t - 2))
            / (self.M * (self.M - 1) * (self.M - 2)),
        )
        return xi * self.tau
