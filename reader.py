import pygame
# pylint: disable=no-member

# Initialize Pygame
pygame.init()


def dms_to_decimal(coord):
    d = float(coord[1:4])
    m = float(coord[5:7])
    s = float(coord[8:])

    return d + m / 60 + s / 3600


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
            print(line)
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

    def draw_screen(self):
        min_coord = min(self.coords, key=lambda coord: (coord[0], coord[1]))
        max_coord = max(self.coords, key=lambda coord: (coord[0], coord[1]))

        # Calculate the scale
        x_range = max_coord[0] - min_coord[0]
        y_range = max_coord[1] - min_coord[1]

        # Assuming width and height are the dimensions of your screen
        x_scale = (self.width - 2*pad) / x_range
        y_scale = (self.height - 2*pad) / y_range

        for label, coord in self.labels.items():
            lab = font.render(label, True, (255, 255, 255))
            # Subtract the minimum and multiply by the scale factor
            x, y = (coord[0] - min_coord[0]) * x_scale + \
                pad, (coord[1] - min_coord[1]) * y_scale + pad
            screen.blit(lab, (x, y))


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
