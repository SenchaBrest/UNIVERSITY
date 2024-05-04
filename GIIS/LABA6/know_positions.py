import pygame
import random
import numpy as np

pygame.init()

WIDTH, HEIGHT = 180, 180
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation")
SAND = (194, 178, 128)
T = 1


class Grid:
    def __init__(self):
        self.grid = np.zeros((WIDTH * 2, HEIGHT + T))
        self.position = []
        self.sand_id = 0

    def addSand(self, pointX, pointY):
        if 0 <= pointX <= WIDTH and 0 <= pointY <= HEIGHT:
            if self.grid[pointX][pointY] == 0:
                self.grid[pointX][pointY] = 1
                self.position.append((pointX, pointY, self.sand_id))
                self.sand_id += 1

    def update_position(self):
        for points in self.position.copy():
            listpoints = list(points)

            if points[1] >= HEIGHT - T:
                continue

            elif self.grid[points[0]][points[1] + T] == 0:
                self.grid[points[0]][points[1]] = 0
                self.grid[points[0]][points[1] + T] = 1
                listpoints[1] += T

            elif self.grid[points[0]][points[1] + T] == 1:
                if (self.grid[points[0] + T][points[1] + T] == 1) and (self.grid[points[0] - T][points[1] + T] == 1):
                    continue

                elif (self.grid[points[0] + T][points[1] + T] == 1) and (self.grid[points[0] - T][points[1] + T] == 0):
                    self.grid[points[0]][points[1]] = 0
                    self.grid[points[0] - T][points[1] + T] = 1
                    listpoints[0] -= T
                    listpoints[1] += T

                elif (self.grid[points[0] + T][points[1] + T] == 0) and (self.grid[points[0] - T][points[1] + T] == 1):
                    self.grid[points[0]][points[1]] = 0
                    self.grid[points[0] + T][points[1] + T] = 1
                    listpoints[0] += T
                    listpoints[1] += T

                else:
                    a = random.choice([-1, 1])
                    self.grid[points[0]][points[1]] = 0
                    self.grid[points[0] + a * T][points[1] + T] = 1
                    listpoints[0] += a * T
                    listpoints[1] += T

            listpoints[0] = max(0, min(listpoints[0], WIDTH - T))
            listpoints[1] = max(0, min(listpoints[1], HEIGHT - T))

            self.position.remove(points)
            self.position.append(tuple(listpoints))

    def draw(self, win):
        for points in self.position:
            pygame.draw.rect(win, SAND, (points[0], points[1], T, T), 0)


def write_sand_positions(sand_positions, filename):
    with open(filename, 'w') as f:
        for pos in sand_positions:
            f.write(f"{pos[2]}:({int(pos[0] / T)}, {int(pos[1] / T)})\n")


def main():
    random.seed(0)
    run = True
    clock = pygame.time.Clock()
    sandbox = Grid()
    pointX = 0

    while run:
        clock.tick(1000000)
        pygame.display.set_caption("Falling Sand - FPS: {}".format(int(clock.get_fps())))
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        def find_nearest_zero(arr, point):
            zeros_indices = [i for i, val in enumerate(arr) if val == 0]

            if not zeros_indices:
                write_sand_positions(sandbox.position, 'positions.txt')
                exit(0)

            return min(zeros_indices, key=lambda x: abs(x - point))

        if sandbox.grid[pointX][0]:
            pointX = find_nearest_zero(sandbox.grid.T[0][0:WIDTH:T], pointX) * T
        else:
            pointX += random.randrange(-2, 3) * T

        if pointX > WIDTH:
            pointX = WIDTH
        elif pointX < 0:
            pointX = 0

        sandbox.addSand(pointX, 0)

        sandbox.update_position()
        sandbox.draw(WIN)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
