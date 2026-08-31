#!/usr/bin/env python3
"""Convert ISARA logo JPEG to PNG with transparent background."""

from PIL import Image
import numpy as np

# Load the JPEG image
img = Image.open('isara-logo.jpeg').convert('RGBA')
data = np.array(img)

# Create mask for white/near-white pixels
# RGB values close to white (above threshold)
r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
white_threshold = 240
white_mask = (r > white_threshold) & (g > white_threshold) & (b > white_threshold)

# Set alpha to 0 for white pixels (make transparent)
data[white_mask, 3] = 0

# Create new image and save
result = Image.fromarray(data)
result.save('isara-logo.png', 'PNG')
print("Successfully converted isara-logo.jpeg to isara-logo.png with transparent background")
