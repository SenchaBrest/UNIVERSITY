import tkinter as tk


class LEDApp:
    def __init__(self, master):
        self.master = master
        master.title("2")

        self.led_status = tk.IntVar()
        self.led_status.set(0)

        self.led_canvas = tk.Canvas(master, width=50, height=50)
        self.led_canvas.pack()

        self.led = self.led_canvas.create_oval(10, 10, 40, 40, fill="gray")

        self.toggle_button = tk.Button(master, text="Вкл/Выкл", command=self.toggle_led)
        self.toggle_button.pack()

    def toggle_led(self):
        if self.led_status.get() == 0:
            self.led_canvas.itemconfig(self.led, fill="blue")
            self.led_status.set(1)
        else:
            self.led_canvas.itemconfig(self.led, fill="gray")
            self.led_status.set(0)


root = tk.Tk()
led_app = LEDApp(root)
root.mainloop()
