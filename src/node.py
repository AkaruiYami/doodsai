'''
    testtank/node.py
'''
import math # math.e for Eular's number

class Node():
    '''
        Braincell within the brain, calculates information and passes it along.
    '''
    def __init__(self, node_type:int=0, parent_callback=None):
        self.parent_callback = parent_callback
        self._node_type = node_type
        self._inputs = [] # list of dicts: {"node": Node(), "weight": float}
        self._bias = 0.0

    @property
    def inputs(self):
        '''Get inputs '''
        return self._inputs

    @property
    def bias(self):
        '''Get bias value of the Node()
        Returns float'''
        return self._bias

    @bias.setter
    def bias(self, var:float):
        '''Set Node() bias value.
        @value: float - recommended -0.1 to 0.1 not enforced.'''
        self._bias = var

    def newConnection(self, node, weight:float):
        '''Create a new connection/input data node, given the node referece,
        and weight of the connection.
        @node: Node() - reference Node()
        @weight: float - weight of the connection input. recommeded -0.1 to .1
            but not enforced.'''
        self._inputs.append({"node": node, "weight": weight})

    def calc(self) -> float:
        '''Gather all available connection node data and return a sum of all
        data with added weight connections. Then add its own bias and calculates
        output based on type of node.
        Input nodes only return themselves.
        Output nodes always calculate as sigmoid.
        Hidden layer nodes can be any of the 11 different types.
        Returns float -- final calculation'''
        calc_sum = 0
        if self._node_type == 0:
            return self.parent_callback()

        for node in self._inputs:
            calc_sum += node["node"].calc() + node["weight"]
        calc_sum += self._bias

        # Node Types
        #   0 = input node (no back tracing)
        #   1 = ouput node (final data)
        match self._node_type:
            case 1: # Output node, always sigmoid
                return 1 / (1 + math.exp(-calc_sum))
            case 2: # Hidden node -- sigmoid
                return 1 / (1 + math.exp(-calc_sum))
            case 3: # Hidden node -- stable sigmoid
                if calc_sum >= 0:
                    return 1 / (1 + math.exp(-calc_sum))
                return 1 / (1 + math.exp(calc_sum))
            case 4: # Hidden node -- linear
                 return calc_sum
            case 5: # Hidden node -- square
                return calc_sum ** 2
            case 6: # Hidden node -- sinus
                return math.sin(calc_sum)
            case 7: # Hidden Node -- absolute
                return abs(calc_sum)
            case 8: # Hidden Node -- Reluctant
                return max(0, calc_sum)
            case 9: # Hidden Node -- Gaussian
                return math.exp(-calc_sum ** 2)
            case 10: # Hidden Node -- Sinc
                if calc_sum == 0:
                    return 0
                return math.sin(calc_sum) / calc_sum
            case 11: # Hidden Node -- Swish
                return calc_sum * (1 / (1 + math.exp(-calc_sum)))
            case 12: # Hidden Node -- Tanh
                return math.tanh(calc_sum)
            case _: pass
            
                                                                       