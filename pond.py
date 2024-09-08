import numpy as np
from PIL import Image, ImageDraw
from pylsd import lsd
import random
import math

# Function to calculate the Euclidean distance between two points
def distance_between_points(p1, p2):
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)

# Function to calculate the midpoint of a line
def midpoint(x1, y1, x2, y2):
    return ((x1 + x2) / 2, (y1 + y2) / 2)

# Function to cluster lines based on proximity (using simple distance threshold)
def cluster_lines(segments, distance_threshold=50):
    clusters = []

    for segment in segments:
        x1, y1, x2, y2 = segment[0], segment[1], segment[2], segment[3]
        line_midpoint = midpoint(x1, y1, x2, y2)
        
        # Try to add the line to an existing cluster based on distance
        added_to_cluster = False
        for cluster in clusters:
            for other_line in cluster:
                other_midpoint = midpoint(other_line[0], other_line[1], other_line[2], other_line[3])
                if distance_between_points(line_midpoint, other_midpoint) < distance_threshold:
                    cluster.append(segment)
                    added_to_cluster = True
                    break
            if added_to_cluster:
                break
        
        # If no suitable cluster was found, create a new cluster
        if not added_to_cluster:
            clusters.append([segment])

    return clusters

# Load the image
full_name = 'milim.jpeg'
img = Image.open(full_name)
img_gray = np.asarray(img.convert('L'))

# Detect line segments using LSD
segments = lsd(img_gray, scale=0.5)

# Cluster lines based on proximity
clusters = cluster_lines(segments, distance_threshold=50)

# Choose the largest (densest) cluster, which is likely to be part of the subject
largest_cluster = max(clusters, key=len)

# Randomly select 4 lines from the largest cluster
if len(largest_cluster) >= 4:
    selected_lines = random.sample(largest_cluster, 4)
else:
    selected_lines = largest_cluster  # If fewer than 4 lines, take all available

# Draw the selected lines on the image
draw = ImageDraw.Draw(img)
for line in selected_lines:
    x1, y1, x2, y2 = line[:4]
    draw.line((x1, y1, x2, y2), fill=(0, 255, 0), width=3)

# Save the image with the drawn lines
img.save('output_random_4_lines_from_subject.jpg')