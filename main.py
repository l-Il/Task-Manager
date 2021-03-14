from cryptography.fernet import Fernet, InvalidToken
from PIL import ImageTk
from PIL import Image as Img
from tkinter import *


class Main:
    def __init__(self):
        self.A = []
        self.filepath = 'bd.txt'
        self.texture = r'textures.png'
        self.style = ['#202020', '#ffffff', '#6a8759']
        try:
            self.key = open("key.key", "rb").read()
        except FileNotFoundError:
            with open(f'key.key', 'wb') as key_file:
                key_file.write(Fernet.generate_key())
            self.key = open(f'key.key', 'rb').read()
        self.f = Fernet(self.key)

        self.root = Tk()
        self.root.title("Password Manager")
        self.root.configure(bg=self.style[0])

        self.img_add = ImageTk.PhotoImage(Img.open(self.texture).crop((1, 1, 17, 17)))
        self.img_del = ImageTk.PhotoImage(Img.open(self.texture).crop((18, 1, 34, 17)))
        self.img_chng = ImageTk.PhotoImage(Img.open(self.texture).crop((35, 1, 51, 17)))
        self.img_exit = ImageTk.PhotoImage(Img.open(self.texture).crop((52, 1, 68, 17)))
        self.img_ent = ImageTk.PhotoImage(Img.open(self.texture).crop((69, 1, 85, 17)))

        self.taskbar = Frame(bg=self.style[0])
        self.taskbar.pack(side=LEFT, fill=Y)
        Button(self.taskbar, text='Добавить', fg=self.style[1], image=self.img_add, compound="left", relief=FLAT, bg=self.style[0], command=self.add).pack(expand=1, anchor=NW)
        Button(self.taskbar, text='Изменить', fg=self.style[1], image=self.img_chng, compound="left", relief=FLAT, bg=self.style[0], command=self.edit).pack(expand=1, anchor=NW)
        Button(self.taskbar, text='Удалить', fg=self.style[1], image=self.img_del, compound="left", relief=FLAT, bg=self.style[0], command=self.delete).pack(expand=1, anchor=NW)
        Button(self.taskbar, text='Выход', fg=self.style[1], image=self.img_exit, compound="left", relief=FLAT, bg=self.style[0], command=self.close).pack(expand=1, anchor=NW)

        self.toolbar = Frame(bg=self.style[0])
        self.toolbar.pack(side=TOP, fill=X)

        self.top_frame = Frame(self.toolbar, bg=self.style[0])
        self.top_frame.pack(side=TOP, fill=X)
        self.status = Label(self.top_frame, fg=self.style[2], width=63, height=1, bg=self.style[0])
        self.status.pack(side=LEFT, fill=X)
        self.variable = IntVar()
        self.send_btn = Button(self.top_frame, image=self.img_ent, relief=FLAT, bg=self.style[0], command=lambda: self.variable.set(1))
        self.send_btn.pack(side=RIGHT)
        self.entry = Entry(self.top_frame, fg=self.style[1], bg=self.style[0], relief=FLAT)
        self.entry.pack(side=RIGHT)

        self.bottom_frame = Frame(self.toolbar, bg=self.style[0])
        self.bottom_frame.pack(side=TOP, fill=X)
        self.listbox = Listbox(self.bottom_frame, fg=self.style[1], bg=self.style[0], width=96, height=10)
        self.listbox.pack(side=LEFT, fill=X, anchor='s')
        self.scrollbar = Scrollbar(self.bottom_frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.scrollbar.config(command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)

        self.root.mainloop()
        self.load()

    def every(self):
        self.status['text'] = ''
        self.entry.delete(0, END)
        self.root.update()

    def add(self):
        self.status['text'] = '[Добавление] Введите задачу: '
        self.entry.delete(0, END)
        self.root.wait_variable(self.variable)
        if self.entry.get() == '':
            self.status['text'] = 'Ошибка. Пустой ввод. Выхожу в главное меню:'
        else:
            self.listbox.insert(END, self.entry.get())
            self.entry.delete(0, END)
            self.every()

    def edit(self):
        self.status['text'] = '[Изменение] Выберите задачу, введите и нажмите клавишу.'
        self.root.wait_variable(self.variable)
        try:
            i = self.listbox.curselection()[0]
            self.listbox.delete(i)
            self.listbox.insert(i, self.entry.get())
            self.entry.delete(0, END)
            self.every()
        except IndexError:
            self.status['text'] = 'Ошибка. Не выбрана задача. Выхожу в главное меню.'

    def delete(self):
        self.status['text'] = '[Удаление] Выберите задачу и нажмите клавишу.'
        self.entry.delete(0, END)
        self.root.wait_variable(self.variable)
        try:
            i = self.listbox.curselection()[0]
            self.listbox.delete(i)
            self.every()
        except IndexError:
            self.status['text'] = 'Ошибка. Не выбрана задача. Выхожу в главное меню.'

    def load(self):
        try:
            with open(self.filepath, "rb") as file:
                decrypted_data = self.f.decrypt(file.read())
            with open(self.filepath, "wb") as file:
                file.write(decrypted_data)
            with open(self.filepath, 'r', encoding='UTF-8') as file:
                self.listbox.delete(0, END)
                for i in file:
                    i.strip()
                    self.A.append(i.replace('\n', '').replace('▓▓', '▓'))
                self.A = sorted(self.A)
                for i in self.A:
                    self.listbox.insert(END, i)
        except FileNotFoundError:
            self.status['text'] = 'Ошибка. Не могу найти файл. Запуск.'
        except (InvalidToken, TypeError):
            self.save()
            self.load()

    def save(self):
        self.A = list(self.listbox.get(0, self.listbox.size()))
        with open(self.filepath, 'w', encoding='UTF-8') as file:
            for i in range(len(self.A)):
                file.write(str(self.A[i]) + '\n')
        with open(self.filepath, "rb") as file:
            encrypted_data = self.f.encrypt(file.read())
        with open(self.filepath, "wb") as file:
            file.write(encrypted_data)

    def close(self):
        self.save()
        self.every()
        print('Выход...')
        raise SystemExit


_ = Main()
