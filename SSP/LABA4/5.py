import tkinter as tk


class InflatableBallApp:
    def __init__(self, master):
        self.master = master
        master.title("5")

        self.radius = 10
        self.centerY = 100

        self.canvas = tk.Canvas(master, width=200, height=150)
        self.canvas.pack()

        self.ball = self.canvas.create_oval(100 - self.radius, self.centerY - self.radius,
                                            100 + self.radius, self.centerY + self.radius,
                                            fill="#FFC0CB", outline="")

        self.inflate_button = tk.Button(master, text="Надуть шарик", command=self.inflate_ball)
        self.inflate_button.pack()

    def inflate_ball(self):
        if self.radius < 50:
            self.radius += 1
            self.centerY -= 1
            self.canvas.delete(self.ball)
            self.ball = self.canvas.create_oval(100 - self.radius, self.centerY - self.radius,
                                                100 + self.radius, self.centerY + self.radius,
                                                fill="#FFC0CB", outline="")
            self.canvas.update()
            self.canvas.after(100, self.inflate_ball)


root = tk.Tk()
app = InflatableBallApp(root)
root.mainloop()
