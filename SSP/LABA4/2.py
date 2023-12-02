import tkinter as tk

# Функция для включения или выключения светодиода
def toggle_led():
    if led_status.get() == 0:
        led_canvas.itemconfig(led, fill="gray")
        led_status.set(1)
    else:
        led_canvas.itemconfig(led, fill="blue")
        led_status.set(0)

# Создаем основное окно
root = tk.Tk()
root.title("Светодиод")

# Создаем переменную для хранения состояния светодиода (0 - выключен, 1 - включен)
led_status = tk.IntVar()
led_status.set(0)

# Создаем Canvas для светодиода
led_canvas = tk.Canvas(root, width=50, height=50)
led_canvas.pack()

# Создаем светодиод
led = led_canvas.create_oval(10, 10, 40, 40, fill="gray")

# Создаем кнопку "Вкл/Выкл"
toggle_button = tk.Button(root, text="Вкл/Выкл", command=toggle_led)
toggle_button.pack()

# Запускаем приложение
root.mainloop()
