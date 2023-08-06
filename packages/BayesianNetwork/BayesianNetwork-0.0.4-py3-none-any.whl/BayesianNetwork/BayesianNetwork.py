class Node:
    def __init__(self, name, states, parents=None, cpt=None):
        self.name = name
        self.states = states
        self.parents = parents if parents is not None else []
        self.cpt = cpt if cpt is not None else {}

    def add_parent(self, parent):
        self.parents.append(parent)

    def add_cpt(self, parent_combination, cpt_values):
        self.cpt[parent_combination] = cpt_values

    def __str__(self):
        linea = "Nombre = "+str(self.name) + "CPT = "+ str(self.cpt)
        return linea


class BayesianNetwork:
    def __init__(self, nodes):
        self.nodes = nodes

    def joint_probability(self, event):
        jp = 1
        for node in self.nodes:
            parent_states = tuple([event[parent.name] for parent in node.parents])
            node_state = event[node.name]
            if parent_states in node.cpt:
                jp *= node.cpt[parent_states][node_state]
            else:
                jp *= node.cpt[node_state]
        return jp
