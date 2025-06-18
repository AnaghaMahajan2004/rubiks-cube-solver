import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

LETTER_TO_COLOR = {
    'U': 'blue',     # Changed from 'yellow'
    'D': 'green',    # Changed from 'white'
    'F': 'white',    # Changed from 'green'
    'B': 'yellow',   # Changed from 'blue'
    'L': 'orange',   # Same
    'R': 'red',      # Same
}




def draw_face(ax, face_colors, start_x, start_y):
    size = 1
    for i in range(3):
        for j in range(3):
            idx = i * 3 + j
            color = LETTER_TO_COLOR.get(face_colors[idx], 'gray')
            rect = patches.Rectangle((start_x + j * size, start_y - i * size),
                                     size, size, facecolor=color, edgecolor='black')
            ax.add_patch(rect)

def plot_cube_face(cube_string, save_path):
    # Split cube string into 6 faces
    U = cube_string[0:9]
    R = cube_string[9:18]
    F = cube_string[18:27]
    D = cube_string[27:36]
    L = cube_string[36:45]
    B = cube_string[45:54]

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')

    # Layout (U on top, L-F-R-B in middle, D at bottom)
    draw_face(ax, U, 3, 9)
    draw_face(ax, L, 0, 6)
    draw_face(ax, F, 3, 6)
    draw_face(ax, R, 6, 6)
    draw_face(ax, B, 9, 6)
    draw_face(ax, D, 3, 3)

    # Set limits
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 12)

    plt.savefig(save_path, bbox_inches='tight')
    plt.close()