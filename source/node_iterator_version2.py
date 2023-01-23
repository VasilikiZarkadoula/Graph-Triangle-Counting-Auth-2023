from itertools import combinations
from tqdm import tqdm


class NodeIterator:

    def __init__(self, graph):
        """
        :param graph: αντικείμενο της Graph
        """
        """
        graph dict {node v : set με τους γειτονες u ετσι ωστε v < u}
        Αποθηκευουμε δλδ μονο τη μια κατευθυνση (v, u). Γλιτωνουμε σε χωρο 
        αφου δεν αποθηκευουμε και την (u, v) και σε iterations στο loop του combinations
        
        Ειναι dict με sets (αρα πιανει περισσοτερο χωρο απο το dict απο lists)
        αλλα κερδιζεις χωρο σε σχεση με την αλλη υλοποιηση επειδη
        εκει ειχες το γραφημα αποθηκευμενο δυο φορες, μια ως graph (dict  απο lists)
        και μια ως graph_edges (set με ολες τις ακμες οπου ειχε και (v,u) και (u,v))
        """
        self.graph = {v : set(u for u in neighbors_list if v < u)
                      for v, neighbors_list in graph.graph.items()}


    def node_iterator(self):

        count_triangles = 0
        # Για κάθε κορυφη v και σετ απο γειτονες nbrs_v τετοιο ωστε το v < απο ολους τους γειτονες
        for v, nbrs_v in tqdm(self.graph.items()):
            # Για κάθε συνδιασμό γειτονων (compination, οχι permutation,
            # δλδ για γειτονες {1,2} -> combinations = [(1,2)], οχι και (2,1)
            for u1, u2 in combinations(nbrs_v, 2):
                # Αν ο u1 είναι και γειτονας του u2 (όταν u2 > u1)
                # ή αν u2 είναι και γειτονας του u1 (όταν u1 > u2) -> κοιταω και τα δύο λόγω
                # του τροπου που αποθηκευτηκαν στο graph.
                if u1 in self.graph[u2] or u2 in self.graph[u1]:
                    # τριγωνο v, u1, u2
                    count_triangles += 1

        return count_triangles

