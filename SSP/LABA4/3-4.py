import tkinter as tk


class ShapeManager:
    def __init__(self, master):
        self.master = master
        master.title("3-4")

        self.x_position = 100
        self.current_shape = "rectangle"

        self.canvas = tk.Canvas(master, width=400, height=250)
        self.canvas.pack()

        self.shape = self.create_shape(self.x_position, 50, self.current_shape)

        shape_buttons_frame = tk.Frame(master)
        shape_buttons_frame.pack()

        self.rectangle_button = tk.Button(shape_buttons_frame, text="Прямоугольник",
                                          command=lambda: self.change_shape("rectangle"))
        self.oval_button = tk.Button(shape_buttons_frame, text="Овал",
                                     command=lambda: self.change_shape("oval"))
        self.triangle_button = tk.Button(shape_buttons_frame, text="Треугольник",
                                         command=lambda: self.change_shape("triangle"))

        self.rectangle_button.pack(side=tk.LEFT)
        self.oval_button.pack(side=tk.LEFT)
        self.triangle_button.pack(side=tk.LEFT)

        move_buttons_frame = tk.Frame(master)
        move_buttons_frame.pack()

        self.move_left_button = tk.Button(move_buttons_frame, text="Влево",
                                          command=lambda: self.move_shape("left"))
        self.move_right_button = tk.Button(move_buttons_frame, text="Вправо",
                                           command=lambda: self.move_shape("right"))

        self.move_left_button.pack(side=tk.LEFT)
        self.move_right_button.pack(side=tk.LEFT)

    def clear_canvas(self):
        self.canvas.delete("all")

    def create_shape(self, x, y, shape_type):
        if shape_type == "rectangle":
            return self.canvas.create_rectangle(x, y, x + 200, y + 150,
                                                outline="black", fill="", width=2)
        elif shape_type == "oval":
            return self.canvas.create_oval(x, y, x + 200, y + 150,
                                           outline="black", fill="", width=2)
        elif shape_type == "triangle":
            return self.canvas.create_polygon(x + 100, y, x + 200, y + 150, x, y + 150,
                                              outline="black", fill="", width=2)

    def move_shape(self, direction):
        self.clear_canvas()

        if direction == "left":
            self.x_position -= 20
        elif direction == "right":
            self.x_position += 20

        self.shape = self.create_shape(self.x_position, 50, self.current_shape)

    def change_shape(self, new_shape):
        self.clear_canvas()
        self.current_shape = new_shape
        self.shape = self.create_shape(self.x_position, 50, new_shape)


root = tk.Tk()
shape_manager = ShapeManager(root)
root.mainloop()
