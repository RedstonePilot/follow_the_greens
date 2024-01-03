import pygame
import re
import math

# Initialize Pygame
pygame.init()

# Set the dimensions of the window
width, height = 1920/2, 1080/2
pad = 100
screen = pygame.display.set_mode((width+pad, height+pad))

# Function to parse coordinates from the file
# COORD:N051.53.43.067:E000.15.58.583


def dms_to_decimal(degrees, minutes, seconds):
    degrees, minutes, seconds = float(degrees), float(minutes), float(seconds)
    return degrees + minutes / 60 + seconds / 3600


def parse_coordinates(file_path, width, height, rotation_angle):
    theta = math.radians(rotation_angle)
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    coordinates = []
    min_lat = min_lon = float('inf')
    max_lat = max_lon = float('-inf')
    for line in lines:
        if line[0] == "C":
            print(line[22:25], line[26:28], line[29:35])

            lat, lon = (dms_to_decimal(line[7:10], line[11:13], line[14:20]), dms_to_decimal(
                line[22:25], line[26:28], line[29:35]))

            min_lat = min(min_lat, lat)
            min_lon = min(min_lon, lon)
            max_lat = max(max_lat, lat)
            max_lon = max(max_lon, lon)

            coordinates.append((lat, lon))

    rotated_coordinates = []
    for lat, lon in coordinates:
        x = ((lon - min_lon) / (max_lon - min_lon)) * width
        # Subtract from height because Pygame's y increases downwards
        y = height - ((lat - min_lat) / (max_lat - min_lat)) * height

        # Calculate the center of the coordinate system
        cx, cy = width / 2, height / 2

        # Translate coordinates to origin
        x, y = x - cx, y - cy

        # Rotate coordinates
        x_rot = x * math.cos(theta) - y * math.sin(theta)
        y_rot = x * math.sin(theta) + y * math.cos(theta)

        # Translate coordinates back
        x_rot, y_rot = x_rot + cx, y_rot + cy

        rotated_coordinates.append((x_rot, y_rot))

    return rotated_coordinates


def parse_runway(file_path):
    with open(file_path, 'r') as file:
        line = file.readline()

    heading = int(line[8:11])
    angle = -(heading - 90)

    return angle


runway_angle = parse_runway("runway.txt")

# Rotate all coordinates by the runway angle
coordinates = parse_coordinates(
    'ground_networks.txt', width, height, math.degrees(runway_angle))

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw each coordinate as a point
    for coord in coordinates:
        pygame.draw.circle(screen, (255, 255, 255), coord, 2)

    # Update the display
    pygame.display.update()

pygame.quit()
