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
        self.labels = {}

        self.parse_lables("lables.txt")
        self.parse_regions("regions.txt")

    def parse_regions(self, filename):
        with open(filename, "r") as in_file:
            data = in_file.read().splitlines()
        data = [d for d in data if d]
        region = []
        for d in data:
            print("try", d)
            if d[0] == ";":  # new region
                self.regions.append(region)
                region = []

            elif d[-1].isnumeric():  # line contains a coord string
                d = d.split(" ")
                print(len(d))
                if len(d) == 3:
                    region.append(
                        (dms_to_decimal(d[1]), dms_to_decimal(d[2])))
                    self.coords.append(
                        (dms_to_decimal(d[1]), dms_to_decimal(d[2])))
                else:
                    print(d)
                    region.append(
                        (dms_to_decimal(d[0]), dms_to_decimal(d[1])))

        return self.regions

    def parse_lables(self, filename):
        self.lables = {}
        with open(filename, "r")as file:
            lables = file.read().splitlines()
        lables = [label.split(" ") for label in lables if label[0] != ";"]

        for label in lables:
            self.lables[label[0][1:-1]] = (dms_to_decimal(label[1]),
                                           dms_to_decimal(label[2]))


# Set the dimensions of the window
width, height = 1920/2, 1080/2
pad = 100
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
