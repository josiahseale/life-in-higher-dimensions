import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd

# Load the provided CSV into a DataFrame
df_2d = pd.read_csv(f'C:\\Users\\User\\Downloads\\Output - Data.csv')

unique_iters = df_2d['Iter'].unique()
fig, ax = plt.subplots(figsize=(10, 10))
class AnimationControl:
    def __init__(self, ani):
        self.ani = ani
        self.paused = False
        fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def on_key_press(self, event):
        if event.key == ' ':
            if self.paused:
                self.ani.event_source.start()
                self.paused = False
            else:
                self.ani.event_source.stop()
                self.paused = True

# Create an initial scatter plot and title
scat = ax.scatter([], [], color='black', marker='s', edgecolors='face')

title = ax.set_title('')

def init():
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')  # Ensure square plot

buffer = 1  # Adjust this value as needed
def update(num):
    iter_data = df_2d[df_2d['Iter'] == unique_iters[num]]

    # Determine plot limits
    min_x, max_x = iter_data['X'].min() - buffer, iter_data['X'].max() + buffer
    min_y, max_y = iter_data['Y'].min() - buffer, iter_data['Y'].max() + buffer

    # Calculate diagonal distance of bounding box for current iteration
    diagonal_distance = ((max_x - min_x) ** 2 + (max_y - min_y) ** 2) ** 0.5

    # Set marker size (adjust the multiplier as needed)
    marker_size = 5000 / (diagonal_distance ** 1.25)  # The power of 1.5 ensures more aggressive shrinking of the marker size

    # Set plot limits
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)

    # Calculate distances from the origin
    distances = (iter_data['X'] ** 2 + iter_data['Y'] ** 2) ** 0.5

    # Center the color palette based on the maximum distance from the origin
    max_distance = distances.max()

    # Use a colormap that is centered on the top-right corner
    colormap = plt.get_cmap('viridis')

    # Normalize distances to be between 0 and 1 based on the maximum distance
    normalized_distances = distances / max_distance

    # Use the normalized distances to determine the colors
    colors = colormap(normalized_distances)

    scat.set_sizes([marker_size])
    scat.set_offsets(iter_data[['X', 'Y']].values)
    scat.set_facecolor(colors)
    title.set_text(f"Iteration: {unique_iters[num]}")

interval_between_frames = 400
corresponding_fps = 1000 / interval_between_frames
ani = animation.FuncAnimation(fig, update, frames=len(unique_iters), init_func=init, repeat=False, interval=interval_between_frames)
control = AnimationControl(ani)  # This will enable pausing and playing the animation with the space bar
ani.save(f'C:\\Users\\User\\Downloads\\Output - Image.gif', writer='pillow', fps=corresponding_fps)

plt.show()
