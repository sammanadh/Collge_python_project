from tkinter import *
from tkinter import messagebox
import csv
import datetime
import os

class Login():

    def __init__(self, master):
        self.master = master
        self.lst = []
        self.frame = Frame(self.master, width=677, height=700)
        self.frame.pack()

        self.bg_img = PhotoImage(file="Login.png")
        self.bg_label = Label(self.frame, image=self.bg_img)
        self.bg_label.place(x=0, y=0, relheight=1, relwidth=1)

        label = Label(self.frame, text="Username", fg="orange", font=("Helvitica", 20, "")).place(relx=0.16, rely=0.27)
        Entry(self.frame, font=("Aerial", 18), bg="light yellow", ).place(relx=0.38, rely=0.28)

        Label(self.frame, text="Password", fg="orange", font=("Helvitica", 20, "")).place(relx=0.17, rely=0.37)
        Entry(self.frame, font=("Aerial", 18), bg="light yellow", show="*").place(relx=0.38, rely=0.38)

        Checkbutton(self.frame, text="Keep me logged in").place(relx=0.38, rely=0.47)

        Button(self.frame, text="Login", command=self.check_credentials, font=("Helvitica", 18)).place(relx=0.47,
                                                                                                       rely=0.56)

        Button(self.frame, text="Create new account", fg="Brown", font=("Helvitica", 20), command=self.double_command,
               bg="aquamarine").place(relx=0.38, rely=0.72)

    #Used so that two functions can be activated with 'Create new account' button
    def double_command(self):
        self.master.destroy()
        self.create()

    #Runs a Register page in new window
    def create(self):
        os.system("python ./new_account.py")

    #Checks the username and password
    def check_credentials(self):
        self.lst = []
        for etr in self.frame.winfo_children():
            if type(etr) == type(Entry()):
                self.lst.append(etr.get())

        condition = False

        if "" in self.lst:
            messagebox.showerror(message="Please completely fill the entries")

        else:
            with open("users.csv", "r") as csv_file:
                read_file = csv.reader(csv_file)
                for row in read_file:
                    if row:
                        if self.lst[0] == row[2] and self.lst[1] == row[4]:
                            messagebox.showinfo(message="You are successfully loged in ")
                            with open("logged_user.txt", "w") as file:
                                file.write(self.lst[0])
                            condition = True
                            self.checkHiredTools()

                if condition == False:
                    messagebox.showerror(message="Your username or password doesn't exist")


    #Checks whether the logged in user has some tools with expired date
    def checkHiredTools(self):
        with open("hired_tools.csv", "r") as csv_file:
            csvreader = csv.reader(csv_file)
            for row in csvreader:
                if row:
                    if row[0] == self.lst[0]:
                        str = "{}".format(datetime.date.today())
                        if str == row[4]:
                            messagebox.showinfo(message = "You need to return {}'s {} today.".format(row[1], row[2]))
        self.checkInvoice()

    def checkInvoice(self):
        if datetime.date.today().day == 1:
            self.master.destroy()
            self.master.destroy()
            os.system("python ./select.py")

        else:
            self.master.destroy()
            os.system("python ./select.py")

root = Tk()
root.resizable(False,False)

w = root.winfo_screenwidth()
h = root.winfo_screenheight()

x = w//2 - 350
y = h//2 - 350

root.geometry("677x650+{}+{}".format(x, y))
root.rowconfigure(4)
root.columnconfigure(4)
root.title("Login")

Login(root)

root.mainloop()