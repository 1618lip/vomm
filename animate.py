# # import cv2
# import sys
# # import numpy as np

# # # Load the background image
# # image = cv2.imread(r"" + sys.argv[1])  # Replace with your image path

# import cv2
# import numpy as np

# # Load the score image
# image = cv2.imread('musicxml.png')  # Path to your generated image

# # Get dimensions of the image
# height, width, _ = image.shape

# # Assuming the number of staves (rows) is known, for example, 5 rows
# num_staves = 5

# # Calculate the height of each row (staff line)
# staff_height = height // num_staves

# # Rectangle parameters
# rect_width = int(width / len(measures) * 2)  # Covering 2 bars
# initial_x = 0
# speed = width / (len(measures) * beats_per_measure)  # Speed to move 1 beat per second
# opacity = 0.4  # Transparency level

# # Create a window to display the animation
# cv2.namedWindow('Music Score', cv2.WINDOW_NORMAL)

# # Animate for each row
# for staff_idx in range(num_staves):
#     initial_y = staff_idx * staff_height  # Set the starting y position for the row
    
#     while initial_x + rect_width < width:
#         frame = image.copy()

#         # Create overlay
#         overlay = frame.copy()
#         cv2.rectangle(overlay, (int(initial_x), int(initial_y)), (int(initial_x + rect_width), int(initial_y + staff_height)), (0, 0, 255), -1)

#         # Apply the overlay with transparency
#         cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)

#         # Display the image
#         cv2.imshow('Music Score', frame)

#         # Move the rectangle
#         initial_x += speed

#         # Wait for 1 second (1000 milliseconds)
#         if cv2.waitKey(1000) & 0xFF == ord('q'):
#             break

#     # Reset the x position for the next staff and loop
#     initial_x = 0

# # Close the display window
# cv2.destroyAllWindows()



# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import numpy as np
# from matplotlib.patches import Rectangle

# # Load the background image
# img = plt.imread(r"" + sys.argv[1])  # Replace with your image path

# # Set up the figure and axis
# fig, ax = plt.subplots()
# ax.imshow(img)

# # Initial rectangle setup
# rect_width = 100  # Width of the rectangle
# rect_height = 50  # Height of the rectangle
# initial_position = (0, 0)  # Starting position of the rectangle
# rect = Rectangle(initial_position, rect_width, rect_height, edgecolor='red', facecolor='none')
# ax.add_patch(rect)

# # Animation function
# def animate(frame):
#     # Update the position of the rectangle
#     new_x = frame * 5  # Move the rectangle to the right (increase this value to move faster)
#     new_y = 50         # Keep the y position constant (you can modify this to move vertically)
#     rect.set_xy((new_x, new_y))
#     return rect,

# # Create animation
# ani = animation.FuncAnimation(fig, animate, frames=np.arange(0, 200), interval=30, blit=True)

# # Display the animation
# plt.show()

import cv2
import numpy as np
from music21 import converter

# Step 1: Parse the MusicXML with music21
# Load the MusicXML file
score = converter.parse('Control5.mxl')

# Get the number of measures and beats per measure
measures = list(score.parts[0].getElementsByClass('Measure'))
beats_per_measure = score.parts[0].recurse().getElementsByClass('TimeSignature')[0].numerator

# Optional: Export the score to an image if not already available
# score.write('musicxml.png', fmt='musicxml.png')  # Requires MuseScore

# Step 2: Load the score image
image = cv2.imread('Control5_sheet.png')  # Path to your generated image

# Get dimensions of the image
height, width, _ = image.shape

# Assuming the number of staves (rows) is known, for example, 5 rows
num_staves = 7  # Adjust this based on the number of staves in your score

# Calculate the height of each row (staff line)
staff_height = height // num_staves

# Rectangle parameters
rect_width = int(width / len(measures) * 2)  # Covering 2 bars
speed = width / (len(measures) * beats_per_measure)  # Speed to move 1 beat per second
opacity = 0.4  # Transparency level

# Create a window to display the animation
cv2.namedWindow('Music Score', cv2.WINDOW_NORMAL)

# Animate for each row (staff line)
for staff_idx in range(num_staves):
    initial_x = 0
    initial_y = staff_idx * staff_height  # Set the starting y position for the row
    
    while initial_x + rect_width < width:
        frame = image.copy()

        # Create overlay
        overlay = frame.copy()
        cv2.rectangle(overlay, (int(initial_x), int(initial_y)), (int(initial_x + rect_width), int(initial_y + staff_height)), (0, 0, 255), -1)

        # Apply the overlay with transparency
        cv2.addWeighted(overlay, opacity, frame, 1 - opacity, 0, frame)

        # Display the image
        cv2.imshow('Music Score', frame)

        # Move the rectangle
        initial_x += speed

        # Wait for 1 second (1000 milliseconds)
        if cv2.waitKey(1000) & 0xFF == ord('q'):
            break

    # Reset the x position for the next staff and loop
    initial_x = 0

# Close the display window
cv2.destroyAllWindows()
