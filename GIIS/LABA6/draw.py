import pygame
import random
import numpy as np
import subprocess

pygame.init()

WIDTH, HEIGHT = 180, 180
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation")
SAND = (194, 178, 128)
T = 1

id_positions = {}
with open('positions.txt', 'r') as file:
    lines = file.readlines()
for line in lines:
    parts = line.strip().split(':')
    key = int(parts[0])
    values = tuple(map(int, parts[1].strip('()').split(',')))
    id_positions[key] = values

positions_colors = {}
with open('pixel_data.txt', 'r') as file:
    lines = file.readlines()
for line in lines:
    key_str, value_str = line.strip().split(':')
    key = tuple(map(int, key_str.strip('()').split(',')))
    value = tuple(map(int, value_str.strip('()').split(',')))
    positions_colors[key] = value



class Grid:
    def __init__(self):
        self.grid = np.zeros((WIDTH * 2, HEIGHT + T))
        self.position = []
        self.sand_id = 0

    def addSand(self, pointX, pointY):
        if 0 <= pointX <= WIDTH and 0 <= pointY <= HEIGHT:
            if self.grid[pointX][pointY] == 0:
                self.grid[pointX][pointY] = 1
                self.position.append((pointX, pointY, positions_colors[id_positions[self.sand_id]]))
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
            pygame.draw.rect(win, points[2], (points[0], points[1], T, T), 0)


def main():
    random.seed(0)
    run = True
    clock = pygame.time.Clock()
    sandbox = Grid()
    pointX = 0

    ffmpeg_cmd = ['ffmpeg', '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo', '-s', f'{WIDTH}x{HEIGHT}', '-pix_fmt',
                  'rgb24', '-r', '720', '-i', '-', '-c:v', 'libx264', '-preset', 'ultrafast', 'output.mp4']
    ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

    while run:
        clock.tick(10000)
        pygame.display.set_caption("Falling Sand - FPS: {}".format(int(clock.get_fps())))
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        def find_nearest_zero(arr, point):
            zeros_indices = [i for i, val in enumerate(arr) if val == 0]

            if not zeros_indices:
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

        img_str = pygame.image.tostring(WIN, 'RGB')
        ffmpeg_process.stdin.write(img_str)

        pygame.display.update()

    pygame.quit()
    ffmpeg_process.stdin.close()
    ffmpeg_process.wait()


if __name__ == "__main__":
    main()
