from tkinter import *
from tkinter import ttk
import csv
import datetime
from tkinter import messagebox
import os

class Search():

    def __init__(self, master):
        self.master = master

        topframe = Frame(self.master, width=700, height=120)
        topframe.pack(side=TOP)

        self.bottomframe = Frame(self.master, width=700, height=280)
        self.bottomframe.pack()

        self.canvas = Canvas(self.bottomframe, width=700, height=280)
        self.canvas.pack()

        Label(topframe, text="- SEARCH TOOLS -", font=("Helvetica", 20)).place(relx=0.35, rely=0.01)

        self.entry = Entry(topframe)
        self.entry.place(relx=0.43, rely=0.55)
        Button(topframe, text="Search", command=self.search, bg="aquamarine").place(relx=0.48, rely=0.75)
        Button(self.bottomframe, text="Back", command=self.back, bg="red").place(relx=0.95, rely=0.91)

    def search(self):
        self.search_val = self.entry.get()

        self.treev = ttk.Treeview(self.canvas,columns=('Owner', 'Tools', 'Rate per day', 'Rate per half day', 'Book'))
        self.treev.heading('#0', text='S.N.')
        self.treev.column('#0', width=30, stretch=NO, anchor="center")
        self.treev.heading('#1', text='Owner')
        self.treev.column('#1', width=100, stretch=NO, anchor="center")
        self.treev.heading('#2', text='Tools')
        self.treev.column('#2', width=100, stretch=NO, anchor="center")
        self.treev.heading('#3', text='Rate per day')
        self.treev.column('#3', width=100, stretch=NO, anchor="center")
        self.treev.heading('#4', text='Rate per half day')
        self.treev.column('#4', width=115, stretch=NO, anchor="center")
        self.treev.heading('#5', text="")
        self.treev.column('#5', width=0, stretch=NO, anchor="center")

        self.treev.bind("<ButtonRelease-1>", self.book)
        self.treev.grid(row=0, column=2, sticky="nsew")
        self.treevies = self.treev

        with open("logged_user.txt") as file:
            self.user = file.read()

        self.ids = []
        with open("tools.csv") as csv_file:
            rows = csv.reader(csv_file)
            i = 0
            condition = True
            for row in rows:
                if row:
                    if row[0] != self.user:
                        if row[1] == self.search_val.lower() or row[1].startswith(self.search_val.lower()):
                                self.treev.insert('', 'end', text=str(i + 1), values=(row[0],row[1],row[2],row[3]))
                                self.ids.append(row[4])
                                i += 1
                                condition = False

            if condition == True:
                messagebox.showerror(message = "Tool not found")


    def book(self, event):
        self.lst = []

        row = self.treev.item(self.treev.selection())

        self.lst.append(self.user)
        with open("logged_user.txt") as file:
            user = file.read()

        vals = row["values"]
        self.lst.append(vals[0])
        self.lst.append(vals[1])

        index = row["text"]
        index = int(index) - 1

        self.id = self.ids[index]
        self.lst.append(self.id)
        self.topwindow()

    def topwindow(self):
        self.top = Toplevel()
        wi = root.winfo_screenwidth()
        hi = root.winfo_screenheight()

        a = wi // 2 - 75

        b = hi // 2 - 100
        self.top.geometry("150x200+{}+{}".format(a, b))
        self.top.title("Booking")

        msg = Message(self.top, text="Please select for when you want to hire the tool and how you want to receive it")
        msg.pack()
        var = IntVar()

        rb1 = Radiobutton(self.top, text="Self pickup", value=1, variable=var)
        rb2 = Radiobutton(self.top, text="Home delivery", value=2, variable=var)
        rb1.pack()
        rb2.pack()

        self.datelst = []
        today = datetime.date.today()

        for a in range(0, 42):
            self.datelst.append(today + datetime.timedelta(a))

        with open("hired_tools.csv", "r") as file:
            readr = csv.reader(file)
            for row in readr:
                if row:
                    if row[3] == self.id and len(row) == 6:
                        dt1 = datetime.datetime.strptime(row[4], "%Y-%m-%d").date()
                        dt2 = dt1 + datetime.timedelta(days=1)
                        dt3 = dt2 + datetime.timedelta(days=1)
                        try:
                            self.datelst.remove(dt1)
                            self.datelst.remove(dt2)
                            self.datelst.remove(dt3)
                        except ValueError:
                            pass

        del self.datelst[0]
        self.datelst.insert(0, "today")
        self.datelst.insert(0, "Please select the date")

        self.cb = ttk.Combobox(self.top, state="readonly", values=self.datelst)
        self.cb.current(0)
        self.cb.pack()
        Button(self.top, text="Conform", command=self.msgbox).pack()

    def msgbox(self):
        val = self.cb.get()
        try:
            if self.datelst.index(val) == 0:
                messagebox.showerror(message="Please select for which day you want to book the tool")

            elif self.datelst.index(val) == 1:
                bookingDate = datetime.date.today()
                expireDate = bookingDate + datetime.timedelta(days=3)
                self.lst.append("{}".format(bookingDate))
                self.lst.append("{}".format(expireDate))
                self.save()

        except:
            bookingDate = datetime.datetime.strptime(val, "%Y-%m-%d").date()
            expireDate = bookingDate + datetime.timedelta(days=3)
            self.lst.append("{}".format(bookingDate))
            self.lst.append("{}".format(expireDate))
            self.save()


    def save(self):
        with open("hired_tools.csv", "a") as file:
            wrt = csv.writer(file)
            wrt.writerow(self.lst)
        messagebox.showinfo(message="You have successfully hired the tool.")
        self.master.destroy()
        os.system("python ./select.py")

    def back(self):
        self.master.destroy()
        os.system("python ./select.py")

root = Tk()
root.resizable(False, False)
root.title("Search Tools")

w = root.winfo_screenwidth()
h = root.winfo_screenheight()

x = w//2 - 350
y = h//2 - 200

root.geometry("700x400+{}+{}".format(x, y))

Search(root)

root.mainloop()