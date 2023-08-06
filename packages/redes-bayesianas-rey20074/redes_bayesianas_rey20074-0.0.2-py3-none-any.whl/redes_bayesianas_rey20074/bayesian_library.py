# bayesian_library.py

class Node:
    def __init__(self, name, values):
        self.name = name
        self.values = values
        self.probabilities = {}
        self.parents = []
        self.children = []
        self.message = {}

    def set_probability(self, value, probability):
        self.probabilities[value] = probability


class BayesianNetwork:
    def __init__(self):
        self.nodes = []

    def add_node(self, name, values):
        node = Node(name, values)
        self.nodes.append(node)
        return node

    def set_relation(self, parent, child):
        parent.children.append(child)
        child.parents.append(parent)

    def set_probability(self, node, value, probability):
        node.set_probability(value, probability)

    def inference(self, target, evidence):
        for node in self.nodes:
            node.message = {}

        for node in self.nodes:
            if node.name in evidence:
                node.message[node.name] = node.probabilities[evidence[node.name]]
            else:
                node.message[node.name] = 1.0

        for node in self.nodes:
            for child in node.children:
                message = 1.0
                for parent in child.parents:
                    message *= parent.message[parent.name]
                child.message[node.name] = message

        result = 1.0
        for node in target.parents:
            result *= node.message[node.name]

        probability = result * \
            target.probabilities[evidence.get(target.name, target.values[0])]
        return probability
