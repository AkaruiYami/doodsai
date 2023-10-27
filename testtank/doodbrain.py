###
#   testtank/doodbrain.py
#
import math # math.e for Eular's number
from node import Node
import random
                                                                       
class Brain():
    def __init__(self, inputs:list[callable]=None, outputs:list[callable]=None, threshold:float=0.8, new:bool=True, connections:int=10):    
        self._threshold = threshold
        self._input = None
        self._output = None
        self._hidden = None
        
        # input nodes need to callback to get data from parent
        # output nodes need to callback to state behaviors
        if inputs:
            for ins in inputs:
                self.addInput(ins)
        if outputs:
            for outs in outputs:
                self.addOutput(outs)

        #TODO This does not currently check for existing connections between nodes before assigning
        if new and self._input and self._output: # generate the neuron connections between nodes
            if connections <= 0:
                raise Exception("connections attr on Brain.init() must be positive int.")
            else:
                for i in range(connections):
                    out_node = random.choice(self._output) # get a random output node
                    in_node = random.choice(self._input) # get a random input node
                    out_node.newConnection(in_node, random.randrange(-0.1, 0.1)) # Create new connection
                    out_node.bias = random.randrange(-0.1, 0.1)

    def addInput(self, parent_callback):
        self._input.append(Node(node_type=0, data_from=parent_callback))
        
    def addOutput(self, parent_callback):
        self._output.append(Node(node_type=1, data_to=parent_callback))
        
    def process(self):
        pass