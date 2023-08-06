#Inteligencia Artificial Laboratorio 2

#Chrisopher Garcia 20541
#Gabriel Vicente 20498

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
        return "P("+str(self.name)+")"+": "+ str(self.cpt)+"\nParents: "+str([node.name for node in self.parents])+"\n"


class BayesianNetwork:
    def __init__(self, nodes):
        self.nodes = nodes

    def isFullyDescribed(self):
        for node in self.nodes:
            for parent_states in node.cpt:
                for state in node.states:
                    if state not in node.cpt[parent_states]:
                        return False
        return True
        
    def compactForm(self):
        StringResult = "\n"
        for node in self.nodes:
            StringResult += str(node)+"\n"
            
        return StringResult
        
    def elementsNetwork(self):
        result = {}
        for node in self.nodes:
            result[node.name] = node.cpt
            
        return result

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

