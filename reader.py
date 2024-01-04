import math
import pygame
# pylint: disable=no-member

# Initialize Pygame
pygame.init()


def dms_to_decimal(coord):
    d = float(coord[1:4])
    m = float(coord[5:7])
    s = float(coord[8:])

    return d + m / 60 + s / 3600


def scale(value, min_value, range_value, screen_size):
    return ((value - min_value) / range_value) * screen_size


class Reader:
    def __init__(self, width, height, screen):
        self.width, self.height = width, height
        self.screen = screen
        self.coords = []
        self.regions = []
        self.geo = []

        self.parse_lables("lables.txt")
        self.parse_regions("regions.txt")
        self.parse_runway("runway.txt")
        self.parse_geo("geo.txt")

        self.scale_coords()
        self.draw_screen()

    def parse_regions(self, filename):
        with open(filename, "r") as in_file:
            data = in_file.read().splitlines()
        data = [d for d in data if d]
        region = []
        for d in data:
            if d[0] == ";":  # new region
                self.regions.append(region)
                region = []

            elif d[-1].isnumeric():  # line contains a coord string
                d = d.split(" ")
                if len(d) == 3:
                    region.append(
                        (dms_to_decimal(d[1]), dms_to_decimal(d[2])))
                    self.coords.append(
                        (dms_to_decimal(d[1]), dms_to_decimal(d[2])))
                else:
                    region.append(
                        (dms_to_decimal(d[0]), dms_to_decimal(d[1])))
                    self.coords.append(
                        (dms_to_decimal(d[0]), dms_to_decimal(d[1])))
        self.regions.append(region)
        # return self.regions

    def parse_lables(self, filename):
        self.labels = {}
        with open(filename, "r")as file:
            lines = file.read().splitlines()
        lines = [line.split(" ") for line in lines if line[0] != ";"]

        for line in lines:
            self.labels[line[0][1:-1]] = (dms_to_decimal(line[1]),
                                          dms_to_decimal(line[2]))
            self.coords.append((dms_to_decimal(line[1]),
                                dms_to_decimal(line[2])))

    def parse_runway(self, filename):
        with open(filename, "r")as in_file:
            runway = in_file.readline().strip().split(" ")
        runway = [r for r in runway if r]
        self.runway_heading = runway[2]
        start = (dms_to_decimal(runway[4]), dms_to_decimal(runway[5]))
        end = (dms_to_decimal(runway[6]), dms_to_decimal(runway[7]))
        self.runway_def = (start, end)

    def parse_geo(self, filename):
        with open(filename, "r")as in_file:
            lines = in_file.read().splitlines()
        lines = [line for line in lines if line and line[0] == "N"]
        for line in lines:
            line = line.split(" ")
            start = (dms_to_decimal(line[0]), dms_to_decimal(line[1]))
            self.coords.append(start)
            end = (dms_to_decimal(line[2]), dms_to_decimal(line[3]))
            self.coords.append(end)
            self.geo.append((start, end))

    def scale_coords(self):
        min_x = min(coord[0] for coord in self.coords)
        max_x = max(coord[0] for coord in self.coords)
        min_y = min(coord[1] for coord in self.coords)
        max_y = max(coord[1] for coord in self.coords)

        range_x = max_x - min_x
        range_y = max_y - min_y

        print(range_x, range_y)

    def draw_screen(self):
        theta = math.radians(47)  # change to proc
        min_lat = min_lon = float('inf')
        max_lat = max_lon = float('-inf')

        for lat, lon in self.coords:
            min_lat = min(min_lat, lat)
            min_lon = min(min_lon, lon)
            max_lat = max(max_lat, lat)
            max_lon = max(max_lon, lon)

        rotated_coordinates = []
        for lat, lon in self.coords:
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


# Set the dimensions of the window
width, height = 1920/2, 1080/2
pad = 0
screen = pygame.display.set_mode((width+pad, height+pad))
font = pygame.font.Font(None, 15)

reader = Reader(width, height, screen)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
