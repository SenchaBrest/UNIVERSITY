import tkinter as tk

def clear_canvas():
    canvas.delete("all")

def create_shape(x, y, shape_type):
    if shape_type == "rectangle":
        return canvas.create_rectangle(x, y, x + 200, y + 150, outline="black", fill="", width=2)
    elif shape_type == "oval":
        return canvas.create_oval(x, y, x + 200, y + 150, outline="black", fill="", width=2)
    elif shape_type == "triangle":
        return canvas.create_polygon(x + 100, y, x + 200, y + 150, x, y + 150, outline="black", fill="", width=2)

def move_shape(direction):
    clear_canvas()
    global x_position

    if direction == "left":
        x_position -= 20
    elif direction == "right":
        x_position += 50

    shape = create_shape(x_position, 50, current_shape)

def change_shape(new_shape):
    clear_canvas()
    global current_shape
    current_shape = new_shape
    shape = create_shape(x_position, 50, new_shape)

x_position = 50
current_shape = "rectangle"

root = tk.Tk()
root.title("Смена формы фигуры и движение")

canvas = tk.Canvas(root, width=400, height=250)
canvas.pack()

shape = create_shape(x_position, 50, current_shape)

rectangle_button = tk.Button(root, text="Прямоугольник", command=lambda: change_shape("rectangle"))
oval_button = tk.Button(root, text="Овал", command=lambda: change_shape("oval"))
triangle_button = tk.Button(root, text="Треугольник", command=lambda: change_shape("triangle"))
move_left_button = tk.Button(root, text="Влево", command=lambda: move_shape("left"))
move_right_button = tk.Button(root, text="Вправо", command=lambda: move_shape("right"))

rectangle_button.pack()
oval_button.pack()
triangle_button.pack()
move_left_button.pack()
move_right_button.pack()

root.mainloop()
