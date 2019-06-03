from tkinter import *
from tkinter import messagebox
import csv
import os

class NewAccount():

    def __init__(self, master):
        self.master = master
        val = IntVar()

        self.bg_img = PhotoImage(file="Register.png")
        self.bg_label = Label(self.master, image=self.bg_img)
        self.bg_label.place(x=0, y=0, relheight=1, relwidth=1)

        Label(self.master, text="First name", bg="light yellow", font=("Helvetica", 18)).place(relx=0.2, rely=0.17)
        Entry(self.master, bg="light yellow", font=("Times New Roman", 18)).place(relx=0.51, rely=0.17)

        Label(self.master, text="Last name", bg="light yellow", font=("Helvetica", 18)).place(relx=0.2, rely=0.24)
        Entry(self.master, bg="light yellow", font=("Times New Roman", 18)).place(relx=0.51, rely=0.24)

        Label(self.master, text="Username", bg="light yellow", font=("Helvetica", 18)).place(relx=0.2, rely=0.31)
        Entry(self.master, bg="light yellow", font=("Times New Roman", 18)).place(relx=0.51, rely=0.31)

        Label(self.master, text="Email", bg="light yellow", font=("Helvetica", 18)).place(relx=0.2, rely=0.39)
        Entry(self.master, bg="light yellow", font=("Times New Roman", 18)).place(relx=0.51, rely=0.39)

        Label(self.master, text="Password", bg="light yellow", font=("Helvetica", 18)).place(relx=0.2, rely=0.47)
        Entry(self.master, show="*", bg="light yellow", font=("Times New Roman", 18)).place(relx=0.51, rely=0.47)

        Label(self.master, text="Confirm password", bg="light yellow", font=("Helvetica", 18)).place(relx=0.2,rely=0.54)
        Entry(self.master, show="*", bg="light yellow", font=("Times New Roman", 18)).place(relx=0.51, rely=0.54)

        Label(self.master, text="Contact number", bg="light yellow", font=("Helvetica", 18)).place(relx=0.2, rely=0.61)
        self.ety = Entry(self.master, bg="light yellow", font=("Times New Roman", 18), textvariable=val)
        self.ety.place(relx=0.51, rely=0.61)

        Button(self.master, text="Submit", command=self.check_pw, bg="light yellow", font=("Helvetica", 18)).place(relx=0.45, rely=0.72)
        Button(self.master, text="Back", command=self.previous_page, bg="light yellow", font=("Helvetica", 18)).place(relx=0.465, rely=0.85)

    # Checks if the credentials are valid
    def check_pw(self):
        while True:
            para = []
            for etr in self.master.winfo_children():
                if type(etr) == type(Entry()):
                    para.append(etr.get())

            if len(para) > 7:
                del para[7:]

            if "" in para:
                messagebox.showerror(title="Error", message="Please completely fill the entries.")
                para.clear()
                break

            if para[6].isdigit() == False:
                messagebox.showerror(title="Error", message="Please enter digits as your contact number.")
                para.clear()
                break

            elif para[4] != para[5]:
                messagebox.showerror(title="Error", message="Please re-conform your password")
                para.clear()
                break

            else:
                lst = para[0:5]
                lst.append(para[6])
                self.final_check(lst)
                break

    # Checks if the credentials already exists
    def final_check(self, param):
        with open("users.csv", "r") as csv_file:
            r_file = csv.reader(csv_file)
            check = True
            for row in r_file:
                if row:
                    if param[2] == row[2]:
                        print (param[2])
                        print (row[2])
                        messagebox.showerror(title="Error", message="Username already exists")
                        check=False
                        break

                    elif param[3] == row[3]:
                        messagebox.showerror(title="Error", message="An account has already been created with this email")
                        check = False
                        break

                    elif param[4] == row[4]:
                        messagebox.showerror(title="Error", message="Password already exists")
                        check = False
                        break
        if check == True:
            self.save(param)


    # Saves the user information into 'users.csv'
    def save(self, pmt):
        with open("users.csv", "a+") as csv_file:
            w_file = csv.writer(csv_file)
            w_file.writerow(pmt)
        messagebox.showinfo(title = "Successful", message = "Your new account has been created")
        with open("logged_user.txt", "w") as file:
            file.write(pmt[2])

        self.master.destroy()
        os.system("python ./select.py")



    #Returns to login page
    def previous_page(self):
        self.master.destroy()
        os.system("python ./login.py")

root = Tk()
root.title("Register")
root.resizable(False, False)

w = root.winfo_screenwidth()
h = root.winfo_screenheight()

x = w//2 - 350
y = h//2 - 350

root.geometry("677x650+{}+{}".format(x, y))

NewAccount(root)


root.mainloop()
