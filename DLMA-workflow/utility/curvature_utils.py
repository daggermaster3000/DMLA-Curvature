"""
Script Name: curvature.py
Description: 
This script performs a curvature analysis on binary masks
Usage: 
- Change the the path to the path to your binary mask and execute the script.
- Additionally you can set the minimum contour length, the window size ratio and the min/max values of the colormap according to your specific requirements
reference: https://medium.com/@stefan.herdy/compute-the-curvature-of-a-binary-mask-in-python-5087a88c6288
"""
import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage import measure
from matplotlib.collections import LineCollection



def generate_plot_edges_with_curvature(mask, edge_pixels, curvature_values):
    fig, (ax1, ax2) = plt.subplots(nrows=2, gridspec_kw={'height_ratios': [3, 1]})

    # Plot the mask on the upper subplot
    ax1.imshow(mask, cmap='gray')

    # We set the min and max of the colorbar, so that 90% of the curvature values are shown.
    # This is to have a nice visualization. You can change this threshold according to your specific task.
    threshold = np.percentile(np.abs(curvature_values), 100)

    # Scatter plot for edge pixels with color representing curvature values on the upper subplot
    sc = ax1.scatter(edge_pixels[:, 1], edge_pixels[:, 0], c=curvature_values, cmap='jet', s=5, vmin=-threshold, vmax=threshold)

    # Colorbar for the upper subplot
    cbar = fig.colorbar(sc, ax=ax1, label='Curvature')
    ax1.set_title("Curvature of Edge Pixels")
    ax2.plot(curvature_values, label='Curvature Line Plot', color='red')
    plt.close()
    """ # Line plot of curvature values on the lower subplot
    x = np.array(range(0,len(curvature_values)))
    y = curvature_values
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)
    # Create a continuous norm to map from data points to colors
    norm = plt.Normalize(curvature_values.min(), curvature_values.max())
    lc = LineCollection(segments, cmap='jet', norm=norm)
    # Set the values used for colormapping
    lc.set_array(curvature_values)
    lc.set_linewidth(2)
    line = ax2.add_collection(lc)
    ax2.set_xlim(x.min(), x.max())
    ax2.set_ylim(y.min(), y.max()) """
    # Return the figure and axis objects
    return fig

def compute_curvature_profile(mask, min_contour_length, window_size_ratio):
    # Compute the contours of the mask to be able to analyze each part individually
    contours = measure.find_contours(mask, 0.5)

    # Initialize arrays to store the curvature information for each edge pixel
    curvature_values = []
    edge_pixels = []

    # Iterate over each contour
    for contour in contours:
        # Iterate over each point in the contour
        for i, point in enumerate(contour):
            # We set the minimum contour length to 20
            # You can change this minimum-value according to your specific requirements
            if contour.shape[0] > min_contour_length:
                # Compute the curvature for the point
                # We set the window size to 1/5 of the whole contour edge. Adjust this value according to your specific task
                window_size = int(contour.shape[0]/window_size_ratio)
                curvature = compute_curvature(point, i, contour, window_size)
                # We compute, whether a point is convex or concave.
                # If you want to have the 2nd derivative shown you can comment this part
                #if curvature > 0:
                #    curvature = 1
                #if curvature <= 0:
                #    curvature = -1
                # Store curvature information and corresponding edge pixel
                
                curvature_values.append(curvature)
                edge_pixels.append(point)

    # Convert lists to numpy arrays for further processing
    curvature_values = np.array(curvature_values)
    edge_pixels = np.array(edge_pixels)

    return edge_pixels, curvature_values

def compute_curvature(point, i, contour, window_size):
    # Compute the curvature using polynomial fitting in a local coordinate system

    # Extract neighboring edge points
    start = max(0, i - window_size // 2)
    end = min(len(contour), i + window_size // 2 + 1)
    neighborhood = contour[start:end]

    # Extract x and y coordinates from the neighborhood
    x_neighborhood = neighborhood[:, 1]
    y_neighborhood = neighborhood[:, 0]
    

    # Compute the tangent direction over the entire neighborhood and rotate the points
    tangent_direction_original = np.arctan2(np.gradient(y_neighborhood), np.gradient(x_neighborhood))
    tangent_direction_original.fill(tangent_direction_original[len(tangent_direction_original)//2])

    # Translate the neighborhood points to the central point
    translated_x = x_neighborhood - point[1]
    translated_y = y_neighborhood - point[0]


    # Apply rotation to the translated neighborhood points
    # We have to rotate the points to be able to compute the curvature independent of the local orientation of the curve
    rotated_x = translated_x * np.cos(-tangent_direction_original) - translated_y * np.sin(-tangent_direction_original)
    rotated_y = translated_x * np.sin(-tangent_direction_original) + translated_y * np.cos(-tangent_direction_original)

    # Fit a polynomial of degree 2 to the rotated coordinates
    coeffs = np.polyfit(rotated_x, rotated_y, 2)


    # You can compute the curvature using the formula: curvature = |d2y/dx2| / (1 + (dy/dx)^2)^(3/2)
    dy_dx = np.polyval(np.polyder(coeffs), rotated_x)
    d2y_dx2 = np.polyval(np.polyder(coeffs, 2), rotated_x)
    curvature = np.abs(d2y_dx2) / np.power(1 + np.power(dy_dx, 2), 1.5)

    # We compute the 2nd derivative in order to determine whether the curve at the certain point is convex or concave
    # curvature = np.polyval(np.polyder(coeffs, 2), rotated_x)

    # Return the mean curvature for the central point
    return np.mean(curvature)

""" # Set minimum length of the contours that should be analyzed
min_contour_length = 20
# Set the ratio of the window size (contour length / window_size_ratio) for local polynomial approximation
window_size_ratio = 5
mask = cv2.imread('/Users/quillan/Documents/Lab/Thesis/Curvature_phenotyping/DLMA/DLMA-workflow/skeleton.png', cv2.IMREAD_GRAYSCALE)
plot_edges_with_curvature(mask, min_contour_length, window_size_ratio) """