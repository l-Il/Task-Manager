from cryptography.fernet import Fernet, InvalidToken
from PIL import ImageTk
from PIL import Image as Img
from tkinter import *

A = []
filepath = 'bd.txt'
texture = r'textures.png'
try:
    key = open("key.key", "rb").read()
except FileNotFoundError:
    with open(f'key.key', 'wb') as key_file:
        key_file.write(Fernet.generate_key())
    key = open(f'key.key', 'rb').read()

f = Fernet(key)
style = ['#202020', '#ffffff', '#6a8759']


def every():
    status['text'] = ''
    entry.delete(0, END)
    root.update()


def add():
    status['text'] = '[Добавление] Введите задачу: '
    entry.delete(0, END)
    root.wait_variable(variable)
    if entry.get() == '':
        status['text'] = 'Ошибка. Пустой ввод. Выхожу в главное меню:'
    else:
        listbox.insert(END, entry.get())
        entry.delete(0, END)
        every()


def edit():
    status['text'] = '[Изменение] Выберите задачу, введите и нажмите клавишу.'
    root.wait_variable(variable)
    try:
        i = listbox.curselection()[0]
        listbox.delete(i)
        listbox.insert(i, entry.get())
        entry.delete(0, END)
        every()
    except IndexError:
        status['text'] = 'Ошибка. Не выбрана задача. Выхожу в главное меню.'


def delete():
    status['text'] = '[Удаление] Выберите задачу и нажмите клавишу.'
    entry.delete(0, END)
    root.wait_variable(variable)
    try:
        i = listbox.curselection()[0]
        listbox.delete(i)
        every()
    except IndexError:
        status['text'] = 'Ошибка. Не выбрана задача. Выхожу в главное меню.'


def load():
    global A
    try:
        with open(filepath, "rb") as file:
            decrypted_data = f.decrypt(file.read())
        with open(filepath, "wb") as file:
            file.write(decrypted_data)
        with open(filepath, 'r', encoding='UTF-8') as file:
            listbox.delete(0, END)
            for i in file:
                i.strip()
                A.append(i.replace('\n', '').replace('▓▓', '▓'))
            A = sorted(A)
            for i in A:
                listbox.insert(END, i)
    except FileNotFoundError:
        status['text'] = 'Ошибка. Не могу найти файл. Запуск.'
    except (InvalidToken, TypeError):
        save()
        load()



def save():
    global A
    A = list(listbox.get(0, listbox.size()))
    with open(filepath, 'w', encoding='UTF-8') as file:
        for i in range(len(A)):
            file.write(str(A[i]) + '\n')
    with open(filepath, "rb") as file:
        encrypted_data = f.encrypt(file.read())
    with open(filepath, "wb") as file:
        file.write(encrypted_data)


def close():
    save()
    every()
    print('Выход...')
    raise SystemExit


class Main(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.icons()
        self.taskbar()
        self.data()

    def icons(self):
        self.img_add = ImageTk.PhotoImage(Img.open(texture).crop((1, 1, 17, 17)))
        self.img_chng = ImageTk.PhotoImage(Img.open(texture).crop((18, 1, 34, 17)))
        self.img_del = ImageTk.PhotoImage(Img.open(texture).crop((35, 1, 51, 17)))
        self.img_exit = ImageTk.PhotoImage(Img.open(texture).crop((52, 1, 68, 17)))
        self.img_ent = ImageTk.PhotoImage(Img.open(texture).crop((69, 1, 85, 17)))

    def taskbar(self):
        taskbar = Frame(bg=style[0])
        taskbar.pack(side=LEFT, fill=Y)
        Button(taskbar, text='Добавить', fg=style[1], image=self.img_add, compound="left", relief=FLAT, bg=style[0],
               command=add).pack(expand=1, anchor=NW)
        Button(taskbar, text='Изменить', fg=style[1], image=self.img_chng, compound="left", relief=FLAT, bg=style[0],
               command=edit).pack(expand=1, anchor=NW)
        Button(taskbar, text='Удалить', fg=style[1], image=self.img_del, compound="left", relief=FLAT, bg=style[0],
               command=delete).pack(expand=1, anchor=NW)
        Button(taskbar, text='Выход', fg=style[1], image=self.img_exit, compound="left", relief=FLAT, bg=style[0],
               command=close).pack(expand=1, anchor=NW)

    def data(self):
        global status
        global entry
        global listbox
        global variable
        toolbar = Frame(bg=style[0])
        toolbar.pack(side=TOP, fill=X)

        top_frame = Frame(toolbar, bg=style[0])
        top_frame.pack(side=TOP, fill=X)
        status = Label(top_frame, fg=style[2], width=63, height=1, bg=style[0])
        status.pack(side=LEFT, fill=X)
        variable = IntVar()
        send_btn = Button(top_frame, image=self.img_ent, relief=FLAT, bg=style[0], command=lambda: variable.set(1))
        send_btn.pack(side=RIGHT)
        entry = Entry(top_frame, fg=style[1], bg=style[0], relief=FLAT)
        entry.pack(side=RIGHT)

        bottom_frame = Frame(toolbar, bg=style[0])
        bottom_frame.pack(side=TOP, fill=X)
        listbox = Listbox(bottom_frame, fg=style[1], bg=style[0], width=96, height=10)
        listbox.pack(side=LEFT, fill=X, anchor='s')
        scrollbar = Scrollbar(bottom_frame)
        scrollbar.pack(side=RIGHT, fill=Y)
        scrollbar.config(command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)


root = Tk()
root.title("Password Manager")
root.configure(bg=style[0])
app = Main(root)
load()
root.mainloop()
