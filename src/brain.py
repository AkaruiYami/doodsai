'''
    testtank/doodbrain.py
'''
import random
from node import Node

class Brain():
    '''Brain class contains Nodes that work like brain cells. The purpose of
    the Brain is to send information into the nodes and deal with the
    information coming out of the nodes, sending results back into the parent
    class.'''
    def __init__(self, inputs:list[callable]=None, outputs:list[callable]=None,
                 threshold:float=0.9, connections:int=10, new:bool=True):
        self._threshold = threshold
        self._in_nodes = []
        self._out_nodes = []
        self._hid_nodes = []

        # input nodes need to callback to get data from parent
        # output nodes need to callback to state behaviors
        if inputs:
            for ins in inputs:
                self.addInput(ins)
        if outputs:
            for outs in outputs:
                self.addOutput(outs)

        #TODO This does not currently check for existing connections between nodes before assigning
        if new and self._in_nodes and self._out_nodes: # generate the neuron connections between nodes
            if connections <= 0:
                raise ValueError("connections attr on Brain.init() must be positive int.")

            for _ in range(connections):
                # get a random output node
                out_node = random.choice(self._out_nodes)
                # get a random input node
                in_node = random.choice(self._in_nodes)
                # Create new connection
                out_node.newConnection(in_node,
                                        random.uniform(-0.1, 0.1))
                # Assign random bais to node
                out_node.bias = random.uniform(-0.1, 0.1)

    def addInput(self, parent_callback):
        '''Add an input node with a parent callback so node can get information.'''
        self._in_nodes.append(Node(node_type=0, parent_callback=parent_callback))

    def addOutput(self, parent_callback):
        '''Add an output node with a parent callback so node can effect, 
        parent class behavior.'''
        self._out_nodes.append(Node(node_type=1, parent_callback=parent_callback))

    def process(self):
        '''
        Iterate through each output node and determin the output. Node callback
        to parent if threshold reached.
        '''
        for outNode in self._out_nodes:
            dothething = False
            if outNode.calc() > self._threshold:
                dothething = True
            outNode.parent_callback(dothething)
            #print(f"impulse is {outNode.calc()} so do {outNode.parent_callback} is {dothething}")
