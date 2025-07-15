"""
Voronoi Diagram Generator

This project generates an interactive 2D Voronoi diagram with random points, using Python.
The diagram supports customizable numbers of points (2–100) and colors (2–20, capped at the number of points),
with regions colored to match their corresponding points. The interface includes toggles for point and boundary
visibility, sliders for adjusting the number of points and colors, and a button to regenerate the diagram. Evenly
distributes colors (black, white, and random unique colors) with randomized remainder assignment are guaranteed.

License
This project is licensed under the MIT License. See the `LICENSE` file for details.

Copyright (c) 2025 Vento Christian Huerlimann <box12@openspace.ch>

Changelog:
250715 v1.0.0   Initial Commit                                  Vento Christian Huerlimann <box12@openspace.ch>
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.widgets import CheckButtons, Button, Slider
import random

# Set matplotlib backend for interactive GUI
import matplotlib
matplotlib.use('Qt5Agg')

# Global variables to store current plot state
points = None
colors = None
index_grid = None
color_grid = None

# Function to calculate axes width in normalized coordinates for fixed pixel width
def get_fixed_width_axes(fig, pixel_width=222):
    fig_width_pixels = fig.get_size_inches()[0] * fig.get_dpi()
    return pixel_width / fig_width_pixels

# Function to calculate x-position to stick UI elements to right border
def get_right_aligned_x(fig, pixel_width=222, pixel_margin=70):
    fig_width_pixels = fig.get_size_inches()[0] * fig.get_dpi()
    ui_width = pixel_width / fig_width_pixels
    margin = pixel_margin / fig_width_pixels
    return 1 - ui_width - margin  # Align to right border with 70-pixel margin

# Function to generate a random color distinct from existing colors
def generate_unique_color(existing_colors):
    threshold = 0.1  # Minimum distance in normalized RGB space
    max_attempts = 100  # Prevent infinite loops

    for _ in range(max_attempts):
        rgb = np.random.rand(3)  # Random RGB values [0, 1]
        hex_color = '#{:02x}{:02x}{:02x}'.format(
            int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255)
        )
        # Check if color is distinct from existing colors
        too_close = False
        for existing in existing_colors:
            existing_rgb = np.array(mcolors.to_rgb(existing))
            dist = np.sqrt(np.sum((rgb - existing_rgb) ** 2))
            if dist < threshold:
                too_close = True
                break
        if not too_close:
            return hex_color
    # Fallback: return a distinct gray
    return '#808080'

# Function to generate and plot Voronoi diagram
def generate_voronoi(ax, point_plots, boundary_lines, check_points, check_boundaries, num_points, num_colors):
    global points, colors, index_grid, color_grid

    # Clear previous points and boundary lines
    for plot in point_plots:
        plot.remove()
    point_plots.clear()
    for line in boundary_lines:
        line.remove()
    boundary_lines.clear()

    # Generate random points in a 10x10 area
    np.random.seed()  # Remove seed for true randomness
    points = np.random.rand(int(num_points), 2) * 10

    # Cap num_colors at num_points to avoid unused colors
    num_points = int(num_points)
    num_colors = min(int(num_colors), num_points)

    # Generate color pool: black and white first, then unique random colors
    color_pool = ['#000000', '#FFFFFF']  # Black and white always included
    for _ in range(num_colors - 2):  # Add unique random colors if num_colors > 2
        color_pool.append(generate_unique_color(color_pool))
    
    # Assign colors evenly to points with random remainder distribution
    colors_per_point = num_points // num_colors  # Base number of points per color
    remainder = num_points % num_colors  # Extra points to distribute
    colors = []
    # Add base number of points for each color
    for i in range(num_colors):
        colors.extend([color_pool[i]] * colors_per_point)
    # Randomly assign remainder points to colors
    if remainder > 0:
        extra_colors = random.sample(range(num_colors), remainder)  # Randomly select colors for extra points
        for i in extra_colors:
            colors.append(color_pool[i])
    random.shuffle(colors)  # Randomize order while keeping distribution

    # Debug: Verify color assignments
    print(f"Num colors: {num_colors}, Color pool: {color_pool[:num_colors]}")
    print(f"Point colors: {[(i, c) for i, c in enumerate(colors)]}")
    print(f"Color counts: {[(c, colors.count(c)) for c in set(colors)]}")

    # Create a mapping from colors to their indices in color_pool
    color_to_index = {color: i for i, color in enumerate(color_pool[:num_colors])}
    print(f"Color to index: {color_to_index}")

    # Create a grid for computing Voronoi diagram
    grid_size = 300  # Optimized for performance
    x = np.linspace(0, 10, grid_size)
    y = np.linspace(0, 10, grid_size)
    X, Y = np.meshgrid(x, y)
    grid_points = np.vstack([X.ravel(), Y.ravel()]).T

    # Compute the nearest point index and color for each grid point
    color_grid = np.zeros((grid_size, grid_size), dtype=int)
    index_grid = np.zeros((grid_size, grid_size), dtype=int)
    for i, grid_point in enumerate(grid_points):
        distances = np.sum((points - grid_point) ** 2, axis=1)
        closest_point_idx = np.argmin(distances)
        index_grid[i // grid_size, i % grid_size] = closest_point_idx
        color_grid[i // grid_size, i % grid_size] = color_to_index[colors[closest_point_idx]]

    # Debug: Verify color_grid values
    print(f"Sample color_grid values: {color_grid[:5, :5]}")

    # Update Voronoi plot with explicit colormap bounds
    if hasattr(ax, 'voronoi_plot'):
        ax.voronoi_plot.set_data(color_grid)
        ax.voronoi_plot.set_cmap(mcolors.ListedColormap(color_pool[:num_colors]))
        ax.voronoi_plot.set_clim(vmin=0, vmax=num_colors-1)
    else:
        cmap = mcolors.ListedColormap(color_pool[:num_colors])
        ax.voronoi_plot = ax.imshow(color_grid, extent=(0, 10, 0, 10), origin='lower', cmap=cmap, interpolation='nearest', rasterized=True, vmin=0, vmax=num_colors-1)

    # Plot points (visibility controlled by Show Points checkbox)
    for i, point in enumerate(points):
        point_plot, = ax.plot(point[0], point[1], 'o', color=colors[i], markersize=8, markeredgecolor='red', markeredgewidth=2)
        point_plot.set_visible(check_points.get_status()[0])
        point_plots.append(point_plot)

    # Pre-calculate boundaries
    dx = 10 / grid_size
    dy = 10 / grid_size
    for i in range(grid_size - 1):
        for j in range(grid_size - 1):
            # Check horizontal boundaries (different closest points)
            if index_grid[i, j] != index_grid[i, j + 1]:
                x1, y1 = j * dx, i * dy
                x2, y2 = (j + 1) * dx, i * dy
                line, = ax.plot([x1, x2], [y1, y2], color='grey', linewidth=1)
                line.set_visible(check_boundaries.get_status()[0])
                boundary_lines.append(line)
            # Check vertical boundaries (different closest points)
            if index_grid[i, j] != index_grid[i + 1, j]:
                x1, y1 = j * dx, i * dy
                x2, y2 = j * dx, (i + 1) * dy
                line, = ax.plot([x1, x2], [y1, y2], color='grey', linewidth=1)
                line.set_visible(check_boundaries.get_status()[0])
                boundary_lines.append(line)

    plt.draw()

# Set up the plot with adjusted figure size
fig = plt.figure(figsize=(12, 6.4))  # Width: 12 inches, Height: 6.4 inches
ax = fig.add_subplot(111)

# Calculate fixed width and x-position for UI elements
ui_width = get_fixed_width_axes(fig)
x_start = get_right_aligned_x(fig)

# Define y-positions for UI elements with adjusted spacing
y_start = 0.05
y_boundaries = y_start + 0.075 + 0.025
y_button = y_boundaries + 0.075 + 0.025
y_points_slider = y_button + 0.075 + 0.025
y_colors_slider = y_points_slider + 0.075 + 0.025

# Add toggle switch for points visibility
ax_check_points = plt.axes([x_start, y_start, ui_width, 0.075])
check_points = CheckButtons(ax_check_points, ['Show Points'], [True])

# Add toggle switch for boundaries visibility
ax_check_boundaries = plt.axes([x_start, y_boundaries, ui_width, 0.075])
check_boundaries = CheckButtons(ax_check_boundaries, ['Show Boundaries'], [False])

# Add button to regenerate image
ax_button = plt.axes([x_start, y_button, ui_width, 0.075])
button = Button(ax_button, 'Regenerate Image')

# Add slider for number of points
ax_points_slider = plt.axes([x_start, y_points_slider, ui_width, 0.075])
points_slider = Slider(ax_points_slider, 'Num Points', 2, 100, valinit=20, valstep=1)
points_slider.label.set_position((0.5, 1.0))  # Center label above slider
points_slider.label.set_horizontalalignment('center')  # Ensure text is centered

# Add slider for number of colors
ax_colors_slider = plt.axes([x_start, y_colors_slider, ui_width, 0.075])
colors_slider = Slider(ax_colors_slider, 'Num Colors', 2, 20, valinit=2, valstep=1)
colors_slider.label.set_position((0.5, 1.0))  # Center label above slider
colors_slider.label.set_horizontalalignment('center')  # Ensure text is centered

# Initialize point and boundary plots
point_plots = []
boundary_lines = []

# Initial Voronoi generation
generate_voronoi(ax, point_plots, boundary_lines, check_points, check_boundaries, points_slider.val, colors_slider.val)

# Disable grid lines
ax.grid(False)

# Set plot limits and labels
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Voronoi Diagram with Random Points')

# Define functions for interactivity
def toggle_points(label):
    for point_plot in point_plots:
        point_plot.set_visible(check_points.get_status()[0])
    plt.draw()

check_points.on_clicked(toggle_points)

def toggle_boundaries(label):
    for line in boundary_lines:
        line.set_visible(check_boundaries.get_status()[0])
    plt.draw()

check_boundaries.on_clicked(toggle_boundaries)

def regenerate(event):
    generate_voronoi(ax, point_plots, boundary_lines, check_points, check_boundaries, points_slider.val, colors_slider.val)

button.on_clicked(regenerate)

# Handle window resize to maintain fixed UI width and right alignment
def on_resize(event):
    ui_width_new = get_fixed_width_axes(fig)
    x_start_new = get_right_aligned_x(fig)
    ax_check_points.set_position([x_start_new, y_start, ui_width_new, 0.075])
    ax_check_boundaries.set_position([x_start_new, y_boundaries, ui_width_new, 0.075])
    ax_button.set_position([x_start_new, y_button, ui_width_new, 0.075])
    ax_points_slider.set_position([x_start_new, y_points_slider, ui_width_new, 0.075])
    ax_colors_slider.set_position([x_start_new, y_colors_slider, ui_width_new, 0.075])
    plt.draw()

fig.canvas.mpl_connect('resize_event', on_resize)

# Show plot
plt.show()