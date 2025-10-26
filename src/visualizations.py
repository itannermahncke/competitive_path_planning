"""Generate different visualizations throughout game."""

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import random
from sklearn import tree

from utils import Occupancy


def gamestate_visual(graph, size, filename="../images/graph"):
    """
    Show plot of environment containing obstacles, pursuer, evader.
    
    Args:
        graph: an np array with initalized obstacles and agents
        size: the size n by n graph
    """   
    # Convert Enums to integers if needed
    if graph.dtype == object:
        graph = np.vectorize(lambda x: x.value if isinstance(x, Occupancy) else x)(graph)


    cmap = colors.ListedColormap([
        'white',    # Occupancy.EMPTY
        'black',    # Occupancy.OBSTACLE
        'green',    # Occupancy.PURSUANT
        'red',      # Occupancy.EVADER
        ])
    bounds = [0,1,2,3,4]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()
    ax.imshow(graph, cmap=cmap, norm=norm)

    # Draw gridlines
    ax.grid(which='major', axis='both', linestyle='-', color='k', linewidth=0.1)
    
    # Make sure each cell center is 0.5 above value
    ax.set_xticks(np.arange(0.5, size, 1))
    ax.set_yticks(np.arange(0.5, size, 1))

    # Hide tick values
    plt.tick_params(axis='both', which='both', bottom=False,   
                    left=False, labelbottom=False, labelleft=False) 
    
    plt.show()

def minimax():
    """Show graph tree of decisions populated with values."""
    pass


