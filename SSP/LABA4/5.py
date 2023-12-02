import tkinter as tk

def inflate_ball():
    global radius, ball, centerY, shadow
    if radius < 50:  # Ограничение максимального размера шара
        radius += 1
        centerY -= 1  # Поднимаем центр шара вверх на 1
        canvas.delete(ball)  # Удаляем предыдущий шар
        canvas.delete(shadow)  # Удаляем предыдущую тень
        ball = canvas.create_oval(100 - radius, centerY - radius, 100 + radius, centerY + radius, fill="#4B0082", outline="")  # Удаление обводки
        shadow = canvas.create_oval(100 - radius, centerY + radius, 100 + radius, centerY + radius + 5, fill="lightgray", outline="")  # Удаление обводки
        canvas.update()  # Обновляем холст
        canvas.after(100, inflate_ball)

# Создание основного окна
window = tk.Tk()
window.title("Надувание шарика")

# Создание холста для отрисовки шара
canvas = tk.Canvas(window, width=200, height=400)
canvas.pack()

radius = 10  # Начальный размер шара
centerY = 200  # Начальное положение центра шара
ball = canvas.create_oval(100 - radius, centerY - radius, 100 + radius, centerY + radius, fill="#4B0082", outline="")  # Удаление обводки
shadow = canvas.create_oval(100 - radius, centerY + radius, 100 + radius, centerY + radius + 5, fill="lightgray", outline="")  # Удаление обводки

# Кнопка для начала надувания
inflate_button = tk.Button(window, text="Надуть шарик", command=inflate_ball)
inflate_button.pack()

window.mainloop()
