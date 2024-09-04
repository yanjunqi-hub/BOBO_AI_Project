import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Function to draw a single carton
def draw_single_carton(ax, x, y, z, length, width, height):
    points = np.array([[x, y, z],
                       [x + length, y, z],
                       [x + length, y + width, z],
                       [x, y + width, z],
                       [x, y, z + height],
                       [x + length, y, z + height],
                       [x + length, y + width, z + height],
                       [x, y + width, z + height]])
    edges = [[points[j] for j in [0, 1, 5, 4]],
             [points[j] for j in [1, 2, 6, 5]],
             [points[j] for j in [2, 3, 7, 6]],
             [points[j] for j in [3, 0, 4, 7]],
             [points[j] for j in [0, 1, 2, 3]],
             [points[j] for j in [4, 5, 6, 7]]]
    poly = Poly3DCollection(edges, edgecolors='black', linewidths=1, facecolors='lightblue')
    ax.add_collection3d(poly)

# Calculation and 3D stacking generation function
def calculate_and_generate_3d_stack(carton_length, carton_width, carton_height, pallet_length, pallet_width, max_length_with_margin, max_width_with_margin, max_height):
    actual_max_length = min(pallet_length, max_length_with_margin)
    actual_max_width = min(pallet_width, max_width_with_margin)

    max_cartons_length = actual_max_length // carton_length
    max_cartons_width = actual_max_width // carton_width
    cartons_per_layer = max_cartons_length * max_cartons_width
    max_layers = max_height // carton_height
    total_cartons_per_pallet = cartons_per_layer * max_layers

    # Return the calculation results for use in the layout
    return max_cartons_length, max_cartons_width, cartons_per_layer, max_layers, total_cartons_per_pallet

# Function to generate 3D plot
def generate_3d_plot(max_cartons_length, max_cartons_width, max_layers, carton_length, carton_width, carton_height):
    # Plot the 3D stacking
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Draw the cartons arranged in layers
    for layer in range(max_layers):
        for i in range(max_cartons_length):
            for j in range(max_cartons_width):
                draw_single_carton(ax, i * carton_length, j * carton_width, layer * carton_height, 
                                   carton_length, carton_width, carton_height)

    # Set the limits for the axes with a margin (1.1 factor)
    ax.set_xlim([0, max_cartons_length * carton_length * 1.1])
    ax.set_ylim([0, max_cartons_width * carton_width * 1.1])
    ax.set_zlim([0, max_layers * carton_height * 1.1])

    # Label the axes
    ax.set_xlabel('X (Length, mm)')
    ax.set_ylabel('Y (Width, mm)')
    ax.set_zlabel('Z (Height, mm)')

    # Title of the plot
    plt.title('3D Carton Stacking on a Pallet')

    # Return the figure for display in Streamlit
    return fig
