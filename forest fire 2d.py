import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, IntSlider
from matplotlib.colors import Colormap, ListedColormap


# Initialize the forest
def initialize_forest(length):
    forest = np.random.choice(['e', 't'], p = [0.1, 0.9], size=(length, length))   # Random lattice of forests and empty sites with probabilities controlling density.
    return forest

# Character grid for vectorizing the forest
char_to_int = {'e': 0, 't': 1, 'b': 2}

# Custom colormap
burncolors = ListedColormap(['white', 'green', 'red'])


# Forest update
def update_forest(forest, p, f, g):
    new_forest = forest.copy()
    size = forest.shape[0]

    for i in range(size):
        for j in range(size):
            if forest[i,j]=='b':
                new_forest[i,j] = 'e'
            if forest[i,j] == 'e':
                 if np.random.binomial(1,p)==1:
                     new_forest[i,j]='t'
            if forest[i,j]=='t':
                if np.random.binomial(1, f) == 1:
                    new_forest[i, j] = 'b'
                if forest[max(i-1,0),j]=='b' or forest[min(i+1,size-1),j]=='b' or forest[i,max(j-1,0)]=='b' or forest[i,min(j+1,size-1)]=='b':
                    if np.random.binomial(1, 1-g)==1:
                        new_forest[i,j]='b'

    return new_forest


# Run simulation
#@interact(length=IntSlider(min = 100, max = 1000, step = 100, value = 100), p=IntSlider(min=0.1, max=1.0, step=0.1, value=0.2), f=IntSlider(min=0.1, max=1.0, step=0.1, value=0.1),  g=IntSlider(min=0.1, max=1.0, step=0.1, value=0.1), steps=IntSlider(min = 100, max = 1000, step = 100, value = 100))
def run_simulation(length, p, f, g, steps):
    forest = initialize_forest(length)
    plt.figure(figsize=(10,10))

    for step in range(steps):
        vec_forest = np.vectorize(char_to_int.get)(forest)
        plt.imshow(vec_forest, cmap=burncolors, interpolation = 'none', vmin = 0, vmax = 2)
        plt.title(f"Step {step}")
        plt.pause(0.5)
        forest = update_forest(forest, p, f, g)
    plt.show()


run_simulation(200, 0.01, 0.0001, 0.25, 100)   # Dense trees and then forest burn, then slow regrowth


#interact(run_simulation(100, 0.2, 0.1, 0.1, 100),
#         p=IntSlider(min=0.1, max=1, step=0.1, value=0.2),
#         f=IntSlider(min=0.1, max=1, step=0.1, value=0.1),
#         g=IntSlider(min=0.1, max=1, step=0.1, value=0.1))