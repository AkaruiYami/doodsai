###
#   testtank/node.py
#
import math # math.e for Eular's number

class Node():
    def __init__(self, node_type:int=0, parent_callback=None):
        self._parent_callback = parent_callback
        self._node_type = node_type
        self._inputs = [] # list of dicts: {"node": Node(), "weight": float}
        self._bias = 0.0
        self._sum = 0
        
    @property
    def inputs(self):
        return self._inputs
    
    @property
    def bias(self):
        return self._bias
    
    @bias.setter
    def bias(self, var:float):
        self._bias = var
    
    def newConnection(self, node, weight:float):
        self._inputs.append({"node": node, "weight": weight})
    
    def calc(self) -> float:
        sum = self._sum
        if self._node_type == 0:
            return sum
        else:
            for node in self._input_nodes:
                sum += node["node"].calc() + node["weight"]
        sum += self._bias

        # Node Types
        #   0 = input node (no back tracing)
        #   1 = ouput node (final data)
        if self._node_type == 1: # Output node, always sigmoid
            return 1 / (1 + math.pow(math.e, -sum))
        if self._node_type == 2: # Hidden node -- sigmoid
            return 1 / (1 + math.pow(math.e, -sum))
        if self._node_type == 3: # Hidden node -- stable sigmoid
            return ((1 / (1 + math.pow(math.e, -sum)))) if sum >= 0 else (1 / (1 + math.pow(math.e, sum)))
        if self._node_type == 4: # Hidden node -- linear
            return sum
        if self._node_type == 5: # Hidden node -- square
            return math.pow(sum, 2)
        if self._node_type == 6: # Hidden node -- sinus
            return math.sin(sum)
        if self._node_type == 7: # Hidden Node -- absolute
            return abs(sum)
        if self._node_type == 8: # Hidden Node -- Reluctant
            return 0 if sum < 0 else sum
        if self._node_type == 9: # Hidden Node -- Gaussian
            return math.pow(math.e, math.pow(-sum, 2))
        if self._node_type == 10: # Hidden Node -- Sinc
            return 0 if sum == 0 else (math.sin(sum) / sum)
        if self._node_type == 11: # Hidden Node -- Swish
            return sum * (1 / (1 + math.pow(math.e, -sum)))
        if self._node_type == 12: # Hidden Node -- Tanh
            return (math.pow(math.e, sum) - math.pow(math.e, -sum)) / (math.pow(math.e, sum) + math.pow(math.e, -sum))
                                                                       