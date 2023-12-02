import tkinter as tk


class TrafficLight:
    def __init__(self, master):
        self.master = master
        master.title("1")

        self.column_frame = tk.Frame(master)
        self.column_frame.pack()

        self.red_light = tk.Label(self.column_frame, width=10, height=5, bg="white")
        self.yellow_light = tk.Label(self.column_frame, width=10, height=5, bg="white")
        self.green_light = tk.Label(self.column_frame, width=10, height=5, bg="white")

        self.red_light.grid(row=0, column=0, padx=10, pady=10)
        self.yellow_light.grid(row=1, column=0, padx=10, pady=10)
        self.green_light.grid(row=2, column=0, padx=10, pady=10)

        self.button_frame = tk.Frame(master)
        self.button_frame.pack()

        button_width = 10
        button_height = 2

        self.red_button = tk.Button(self.button_frame, text="Красный",
                                    command=lambda: self.change_color("red"),
                                    width=button_width, height=button_height)
        self.yellow_button = tk.Button(self.button_frame, text="Жёлтый",
                                       command=lambda: self.change_color("yellow"),
                                       width=button_width, height=button_height)
        self.green_button = tk.Button(self.button_frame, text="Зелёный",
                                      command=lambda: self.change_color("green"),
                                      width=button_width, height=button_height)

        self.red_button.grid(row=0, column=0, pady=10)
        self.yellow_button.grid(row=1, column=0, pady=10)
        self.green_button.grid(row=2, column=0, pady=10)

    def change_color(self, color):
        self.red_light.config(bg="white")
        self.yellow_light.config(bg="white")
        self.green_light.config(bg="white")

        if color == "red":
            self.red_light.config(bg="red")
        elif color == "yellow":
            self.yellow_light.config(bg="yellow")
        elif color == "green":
            self.green_light.config(bg="green")


root = tk.Tk()
traffic_light_app = TrafficLight(root)
root.mainloop()
