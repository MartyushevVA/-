from tkinter import *

def clicked():
    global RULE
    global NUM_OF_COND
    RULE = pravilo.get()
    NUM_OF_COND = int(sost.get())


window = Tk()
window.title("Настройка конфигурации")
window.geometry('320x100')
vopros = Label(window, text="Заполнить поле в случайном порядке?", font=("Arial Bold", 10))
vopros.grid(column=0, row=0)
chk_state = BooleanVar()
chk_state.set(True)
chk = Checkbutton(window, text='', var=chk_state)
chk.grid(column=1, row=0)
vvodpravila = Label(window, text="Введите правило:", font=("Arial Bold", 10))
vvodpravila.grid(column=0, row=2)
pravilo = Entry(window, width=10)
pravilo.grid(column=1, row=2)
vvodsost = Label(window, text="Введите количество состояний:", font=("Arial Bold", 10))
vvodsost.grid(column=0, row=1)
sost = Entry(window, width=10)
sost.grid(column=1, row=1)
btn = Button(window, text="Подтвердить", command=clicked)
btn.grid(column=0, row=3)
window.mainloop()
RANDOM = chk_state.get()