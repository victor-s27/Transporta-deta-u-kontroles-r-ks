import tkinter as tk
from tkinter import ttk, messagebox
from sqlite3 import *
import tkinter as tk
from tkinter import Image
from PIL import Image, ImageTk
import os 

connection = connect('DB/my-test.db')

HEIGHT = 900
WIDTH = 500

class MainPage(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        pages = LoadingPage, StartPage, RegisterPage, AuthorizePage

        window = tk.Frame(self, width = 900, height = 500)
        window.pack()
        window.place(anchor='center', relx=0.5, rely=0.5)
        self.title("Transporta detaļu kontroles rīks ")
        
        self.geometry("500x900")    

        self.frames = {}
        for page in pages:
            name = page.__name__
            frame = page(parent=window, controller=self)
            self.frames[name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, name):

        frame = self.frames[name]
        frame.tkraise()

class LoadingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        ttk.Label(self, text="Lūdzu uzgaidiet...").grid(column=1, row=0)


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        canvas = tk.Canvas(self, height=HEIGHT, width=WIDTH)
        canvas.pack()

        image = Image.open("Pictures/backGround.png")
        resize_image = image.resize((WIDTH, HEIGHT))
        img = ImageTk.PhotoImage(resize_image)
        labelBG = tk.Label(self, image=img)
        labelBG.image = img
        labelBG.place(relheight=1, relwidth=1)
        
        btn1 = tk.Button(self, text="Pierakstīties", command=lambda: controller.show_frame("AuthorizePage"))
        btn1.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.35)

        btn2 = tk.Button(self, text="Izveidot lietotāja profilu", command=lambda: controller.show_frame("RegisterPage"))
        btn2.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.45)

def confirmClicked():
    window.destroy()
    os.system('python App/lietotneLD.py')

class RegisterPage(tk.Frame):

    ERROR = 'Error.TLabel'
    SUCCESS = 'Success.TLabel'

    def __init__(self, parent, controller):
        super().__init__()
        tk.Frame.__init__(self, parent)
        self.controller = controller


        
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()

        self.confirm_password_var.trace('w', self.compare_passwords)

        self.style = ttk.Style(self)
        self.style.configure('Error.TLabel', foreground='red')
        self.style.configure('Success.TLabel', foreground='green')


        canvas = tk.Canvas(self, height=HEIGHT, width=WIDTH)
        canvas.pack()

        image = Image.open("Pictures/backGround.png")
        resize_image = image.resize((WIDTH, HEIGHT))
        img = ImageTk.PhotoImage(resize_image)
        labelBG = tk.Label(self, image=img)
        labelBG.image = img
        labelBG.place(relheight=1, relwidth=1)


        ttk.Label(self, text="Jūsu e-pasts").place(relheight=0.05, relwidth=0.2, relx=0.25, rely=0.25)
        self.email_entry = ttk.Entry(self, textvariable=self.email_var)
        self.email_entry.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.30)
        self.email_entry.focus()

        ttk.Label(self, text="Jūsu parole").place(relheight=0.05, relwidth=0.2, relx=0.25, rely=0.37)
        self.password_entry = ttk.Entry(self, textvariable=self.password_var, show="*")
        self.password_entry.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.42)
        self.password_entry.focus()

        ttk.Label(self, text="Atkārtojiet paroli").place(relheight=0.05, relwidth=0.2, relx=0.25, rely=0.49)
        self.confirm_password_entry = ttk.Entry(self, textvariable=self.confirm_password_var, show="*")
        self.confirm_password_entry.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.54)
        self.confirm_password_entry.focus()
        self.message_label = ttk.Label(self)
        self.message_label.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.61)

        btn1 = ttk.Button(self, text="Reģistrēties", command=self.create_user)
        btn1.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.65)



    def get_update(self, message, type=None):

        self.message_label['text'] = message
        if type:
            self.message_label['style'] = type

    def compare_passwords(self, *args):

        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()

        if confirm_password == password:
            self.get_update("Paroles sakrīt!", self.SUCCESS)
            return

        self.get_update("Paroles nesakrīt!", self.ERROR)

    def create_user(self, *args):

        email = self.email_var.get()
        password = self.password_var.get()
        confirm_password = self.confirm_password_var.get()

        email_copy = ""
        with connection:
            query = connection.execute("SELECT user_email FROM Users WHERE user_email = '%s'" % email)
            for row in query:
                result = row[0]
                if email in result:
                    email_copy = email
                else:
                    pass

        if confirm_password == password and email_copy != email:
            with connection:
                connection.execute("INSERT INTO Users (user_email, user_password) VALUES('%s', '%s')" % (email, password))
            
            sql = 'INSERT INTO Cars (id_user, nosaukums, nobraukums, datums) values(?, ?, ?, ?)'
            getUserID = connection.execute("SELECT user_id FROM Users WHERE user_email = '%s'" % email)
            for row in getUserID:
                data = [
                ('%d' % row[0], 'Odometrs', 0, "2022-05-26" ),
                ('%d' % row[0], 'Ella', 0, "2021-05-13"),
                ('%d' % row[0], 'Filtri', 0, "2022-01-22"),
                ('%d' % row[0], 'Suporti', 0, "2022-02-22"),
                ('%d' % row[0], 'Kluci', 0, "2022-03-22"),
                ('%d' % row[0], 'Skidrums', 0, "2021-09-22")
                ]
                connection.execute("INSERT INTO Connection (id_user_connection) VALUES('%d')" % (row[0]))
            with connection:
               connection.executemany(sql, data)
            messagebox.showinfo("Reģistrācija", "Lietotājs tika reģistrēts!", icon = 'info')
            confirmClicked()
            
class AuthorizePage(tk.Frame):

    ERROR = 'Error.TLabel'
    SUCCESS = 'Success.TLabel'

    def __init__(self, parent, controller):
        super().__init__()
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.style = ttk.Style(self)
        self.style.configure('Error.TLabel', foreground='red')
        self.style.configure('Success.TLabel', foreground='green')

        canvas = tk.Canvas(self, height=HEIGHT, width=WIDTH)
        canvas.pack()

        image = Image.open("Pictures/backGround.png")
        resize_image = image.resize((WIDTH, HEIGHT))
        img = ImageTk.PhotoImage(resize_image)
        labelBG = tk.Label(self, image=img)
        labelBG.image = img
        labelBG.place(relheight=1, relwidth=1)

        ttk.Label(self, text="Jūsu e-pasts").place(relheight=0.05, relwidth=0.2, relx=0.25, rely=0.25)
        self.email_entry = ttk.Entry(self, textvariable=self.email_var)
        self.email_entry.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.30)
        self.email_entry.focus()

        ttk.Label(self, text="Jūsu parole").place(relheight=0.05, relwidth=0.2, relx=0.25, rely=0.37)
        self.password_entry = ttk.Entry(self, textvariable=self.password_var, show="*")
        self.password_entry.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.42)
        self.password_entry.focus()

        self.message_label = ttk.Label(self)
        self.message_label.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.61)

        btn1 = ttk.Button(self, text="Pierakstīties", command=self.check_user)
        btn1.place(relheight=0.05, relwidth=0.5, relx=0.25, rely=0.65)




    def get_update(self, message, type=None):

        self.message_label['text'] = message
        if type:
            self.message_label['style'] = type

    def check_user(self, *args):

        email = self.email_var.get()
        password = self.password_var.get()
        email_copy = ""
        password_copy = ""
        with connection:
            query = connection.execute("SELECT user_email FROM Users WHERE user_email = '%s'" % email)
            for row in query:
                result = row[0]
                if email in result:
                    email_copy = email
                else:
                    pass

        with connection:
            query = connection.execute("SELECT user_password FROM Users WHERE user_email = '%s'" % email_copy)
            for row in query:
                result = row[0]
                password_copy = result

        if not password or not email:
            self.get_update("Pārbaudiet ievadīto e-pastu un/vai paroli!", self.ERROR)
        elif password_copy == password and email_copy == email:
            with connection:
                query = connection.execute("SELECT user_id FROM Users WHERE user_email = '%s'" % email_copy)
                for row in query:
                    result = row[0]
                    user_num = result
            self.get_update("Lietotājs atrasts!", self.SUCCESS)
            with connection:
                connection.execute("INSERT INTO Connection (id_user_connection) VALUES('%d')" % (user_num))
            messagebox.showinfo("Autorizācija", "Laipni lūdzam, %s!" % email)
            confirmClicked()
        elif email_copy != email:
            self.get_update("Lietotājs ar tādu e-pastu nav atrasts!", self.ERROR)
        else:
            self.get_update("Pārbaudiet ievadīto e-pastu un/vai paroli!", self.ERROR)


if __name__ == "__main__":
    window = MainPage()
    window.mainloop()
