# from tensorflow.python.framework import ops
from tensorflow.python.framework import ops

def init():
    # Loading graph
    graph = ops.get_default_graph()
    return graph