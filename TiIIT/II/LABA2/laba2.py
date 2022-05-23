import random
import numpy as np

global_epsilon = 0.000000001
epsilon = 0.0001

def function(x, y, z):
    return x * y + (z ** 2) * np.sin(x) + (2 * (x ** 2) + 3) * (y ** 2)

def derivative_x(x, y, z):
    return (function(x + global_epsilon, y, z) -
            function(x, y, z)) / global_epsilon

def derivative_y(x, y, z):
    return (function(x, y + global_epsilon, z) -
            function(x, y, z)) / global_epsilon

def derivative_z(x, y, z):
    return (function(x, y + global_epsilon, z) -
            function(x, y, z)) / global_epsilon

def abs_gradient(x, y, z): 
    return (derivative_x(x, y, z) ** 2 + derivative_y(x, y, z) ** 2 + derivative_z(x, y, z) ** 2) ** 0.5

if __name__=="__main__":
    
    xmin, xmax = map(int, input("Введите xmin, xmax: ").split(' '))
    ymin, ymax = map(int, input("Введите ymin, ymax: ").split(' '))
    zmin, zmax = map(int, input("Введите zmin, zmax: ").split(' '))
    print("Введите 1 для поиска максимума,\n0 - для поиска минимума: ")
     
    choice=int(input())
    
    x = random.uniform(xmin,xmax)
    y = random.uniform(ymin,ymax)
    z = random.uniform(zmax,zmin)

    iter = 100
    alf = 0.1
    if(choice == 1):
        for i in range(iter):

            if (x < xmin or x > xmax or y < ymin or \
                 y > ymax or z < zmin or z > zmax):
                break
            if(abs_gradient(x, y, z) < epsilon):
                break

            x_next = x + alf * derivative_x(x, y, z)
            y_next = y + alf * derivative_y(x, y, z)
            z_next = z + alf * derivative_z(x, y, z)

            if (x_next < xmin or x_next > xmax or y_next < ymin or \
                 y_next > ymax or z_next < zmin or z_next > zmax):
                break
            if(abs_gradient(x_next, y_next, z_next) < epsilon):
                break

            x = x_next
            y = y_next
            z = z_next
    
        print(f"Максимум: x = {x}, y = {y}, z = {z}; \nfunction = {function(x, y, z)}")
    elif(choice == 0):
        for i in range(iter):
            if (x < xmin or x > xmax or y < ymin or \
                 y > ymax or z < zmin or z > zmax):
                break
            if(abs_gradient(x, y, z) < epsilon):
                break

            x_next = x - alf * derivative_x(x, y, z)
            y_next = y - alf * derivative_y(x, y, z)
            z_next = z - alf * derivative_z(x, y, z)

            if (x_next < xmin or x_next > xmax or y_next < ymin or \
                 y_next > ymax or z_next < zmin or z_next > zmax):
                break
            if(abs_gradient(x_next, y_next, z_next) < epsilon):
                break

            x = x_next
            y = y_next
            z = z_next

        print(f"Минимум: x = {x}, y = {y}, z = {z}; \nfunction = {function(x, y, z)}")



