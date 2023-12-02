import tkinter as tk


def change_color(color):
    red_light.config(bg="white")
    yellow_light.config(bg="white")
    green_light.config(bg="white")

    if color == "red":
        red_light.config(bg="red")
    elif color == "yellow":
        yellow_light.config(bg="yellow")
    elif color == "green":
        green_light.config(bg="green")


root = tk.Tk()
root.title("Световая колонна")

column_frame = tk.Frame(root)
column_frame.pack()

red_light = tk.Label(column_frame, width=10, height=5, bg="white")
yellow_light = tk.Label(column_frame, width=10, height=5, bg="white")
green_light = tk.Label(column_frame, width=10, height=5, bg="white")

red_light.grid(row=0, column=0, padx=10)
yellow_light.grid(row=1, column=0, padx=10)
green_light.grid(row=2, column=0, padx=10)

button_frame = tk.Frame(root)
button_frame.pack()

red_button = tk.Button(button_frame, text="Красный", command=lambda: change_color("red"))
yellow_button = tk.Button(button_frame, text="Жёлтый", command=lambda: change_color("yellow"))
green_button = tk.Button(button_frame, text="Зелёный", command=lambda: change_color("green"))

red_button.grid(row=0, column=0, padx=10)
yellow_button.grid(row=0, column=1, padx=10)
green_button.grid(row=0, column=2, padx=10)

root.mainloop()
