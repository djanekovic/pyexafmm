
import fmm.octree as octree
import fmm.hilbert as hilbert

class InverseFMM():
    def __init__(self, fmm):
        self.fmm = fmm
        self.maximum_level = self.fmm.octree.maximum_level


    def form_p2p_operators_with_neighbors(self, source_key):
        """
        Form P2P operator for cluster i with its neighbors.

        We shall define P2P_{ij} using M2L operators of children
        P2P^{k}_{i, j} = [[M2L^{k+1}_{i1, j1}, M2L^{k+1}_{i1, j2}, ...],
                          [M2L^{k+1}_{i2, j1}, M2L^{k+1}_{i2, j2}, ...],
                          ...
                          [M2L^{k+1}_{i2^d, j1}, ....]]
        NOTE: this will be tricky since M2L operators are compressed, see section 2.4

        Function returns dictionary indexed as [(source_key, destination_key)]
        """

        # neighbors of source_key on same level
        neigbors_array = fmm.hilbert.get_neighbors(source_key)
        level = fmm.hilbert.get_level(source_key);

        p2p = []
        for neighbor_key in np.nditer(neighbors_array):
            # for each neighbor build operator row by row
            p2p_operator = []
            for i in np.nditer(hilbert.get_children(source_key)):
                p2p_row = []
                for j in np.nditer(hilbert.get_children(neighbor_key)):
                    #FIXME: this won't work since we have no m2l_operators list
                    # I have to reverse action that is done in compress_m2l_operators:114
                    # in order to use this.
                    p2p_row.append(m2l_operators[level][j][i])
                p2p_operator.append(p2p_row)
            p2p[(source_key, neighbor_key)] = np.block(p2p_operator)

        return p2p


    def upward_pass():
        """
        Eliminate cluster by cluster by cluster starting from the bottom of the tree.
            Algorithm 1. From Sivaram Ambikasaran, Eric F. Darve: Inverse Fast Multipole Method
        """

        #TODO: are we going from max_level to the root or not?
        for level in range(self.fmm.octree.maximum_level, -1, -1):
            for key in self.fmm.octree.non_empty_source_nodes_by_level[level]:
                p2p = self._form_p2p_operators_with_neighbors(key)
            for key in self.fmm.octree.non_empty_source_nodes_by_level[level]:
                # elimination of x_i^k and z_i^k using eq 4.7, 4.8
