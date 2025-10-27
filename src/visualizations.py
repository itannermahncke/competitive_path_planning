"""Generate different visualizations throughout game."""

import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import random
from sklearn import tree

# from graphviz import Digraph

from PIL import Image
import glob

from utils import Occupancy, Node, Role


def gamestate_visual(graph, size, n):
    """
    Show plot of environment containing obstacles, pursuer, evader.

    Args:
        graph: an np array with initalized obstacles and agents
        size: the size n by n graph
        n: image id
        filename: path to file
    """
    # Convert Enums to integers if needed
    if graph.dtype == object:
        graph = np.vectorize(lambda x: x.value if isinstance(x, Occupancy) else x)(
            graph
        )

    cmap = colors.ListedColormap(
        [
            "white",  # Occupancy.EMPTY
            "black",  # Occupancy.OBSTACLE
            "green",  # Occupancy.PURSUANT
            "red",  # Occupancy.EVADER
        ]
    )
    bounds = [0, 1, 2, 3, 4]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig, ax = plt.subplots()
    ax.imshow(graph, cmap=cmap, norm=norm)

    # Draw gridlines
    ax.grid(which="major", axis="both", linestyle="-", color="k", linewidth=0.1)

    # Make sure each cell center is 0.5 above value
    ax.set_xticks(np.arange(0.5, size, 1))
    ax.set_yticks(np.arange(0.5, size, 1))

    # Hide tick values
    plt.tick_params(
        axis="both",
        which="both",
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False,
    )
    plt.savefig(f"images/graph_state_{n}")


def gamestate_gif(
    img_folder="images/",
    output_gif_path="images/gamestate_gifs/gamestate1.gif",
    duration=500,
    loop=0,
):
    """
    Creates an animated GIF from a folder of images.

    Args:
        image_folder (str): Path to the folder containing the images.
        output_gif_path (str): Path and filename for the output GIF.
        duration (int): Duration of each frame in milliseconds.
        loop (int): Number of times the GIF should loop (0 for infinite loop).
    """
    image_files = sorted(
        glob.glob(f"{img_folder}/*.png")
    )  # Adjust extension as needed (e.g., *.jpg)
    if not image_files:
        print(f"No image files found in {img_folder}")
        return

    images = [Image.open(file) for file in image_files]

    # Save the first image, appending subsequent images to create the GIF
    images[0].save(
        output_gif_path,
        save_all=True,
        append_images=images[1:],
        duration=duration,
        loop=loop,
        optimize=False,
    )
    print(f"GIF successfully created at: {output_gif_path}")


def visualize_game_tree(root: Node, n):
    """
    Visualize the game tree using Graphviz, labeling each node with its distance.
    """
    dot = Digraph(comment="Game Tree")
    dot.attr(rankdir="TB")  # top to bottom layout

    def add_node(node: Node):
        if node is None:
            return

        # label: just the distance value
        node_label = f"{node.distance}"
        if node.agent_role == Role.PURSUANT:
            node_color = "red"
        else:
            node_color = "green"

        # add node to graph with unique identifier
        dot.node(str(node.id), node_label, color=node_color)

        # add children edges
        if node.children:
            for child in node.children:
                if child is not None:
                    # Recursively build subtree
                    add_node(child)
                    dot.edge(str(node.id), str(child.id))

    # Build from root
    add_node(root)

    # Save and render
    dot.render(f"images/game_tree_{0}", format="png", cleanup=True)
    return dot
