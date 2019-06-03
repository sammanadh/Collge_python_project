from tkinter import *
import datetime
import csv
from datetime import timedelta
import shutil
import os

class Invoice():

    def __init__(self, master):
        self.master = master
        self.toolsinfo ={}

        path = r".\dump"
        files = os.listdir(path)

        yesterday = datetime.date.today()-datetime.timedelta(days=1)

        yr = yesterday.year
        mth = yesterday.month

        if "hired_tools,year{},month{}.csv".format(yr, mth) not in files:
            shutil.copy("hired_tools.csv", r".\dump")
            os.rename(".\dump\hired_tools.csv", ".\dump\hired_tools,year{},month{}.csv".format(yr, mth))


        self.frame1 = Frame(self.master, width=850, height = 200)
        self.frame1.pack()
        self.canvas = Canvas(self.master, width=850, height=300)
        self.canvas.pack()


        self.innerframe1 = Frame(self.canvas,width=90,height = 200)
        self.innerframe2 = Frame(self.canvas,width=90,height = 200)
        self.innerframe3 = Frame(self.canvas,width=90,height = 200)
        self.innerframe4 = Frame(self.canvas,width=90,height = 200)
        self.innerframe5 = Frame(self.canvas,width=90,height = 200)
        self.innerframe6 = Frame(self.canvas, width=90, height=200)
        self.innerframe7 = Frame(self.canvas, width=90, height=200)
        self.innerframe8 = Frame(self.canvas, width=90, height=200)
        self.innerframe9 = Frame(self.canvas, width=90, height=200)

        self.innerframe1.pack(side=LEFT)
        self.innerframe1.pack_propagate(False)
        self.innerframe2.pack(side=LEFT)
        self.innerframe2.pack_propagate(False)
        self.innerframe3.pack(side=LEFT)
        self.innerframe3.pack_propagate(False)
        self.innerframe4.pack(side=LEFT)
        self.innerframe4.pack_propagate(False)
        self.innerframe5.pack(side=LEFT)
        self.innerframe5.pack_propagate(False)
        self.innerframe6.pack(side=LEFT)
        self.innerframe6.pack_propagate(False)
        self.innerframe7.pack(side=LEFT)
        self.innerframe7.pack_propagate(False)
        self.innerframe8.pack(side=LEFT)
        self.innerframe8.pack_propagate(False)
        self.innerframe9.pack(side=LEFT)
        self.innerframe9.pack_propagate(False)

        Label(self.frame1, text="- INVOICE -", font=("Helvetica", 20)).place(relx=0.37, rely=0.01)
        Label(self.frame1, text="Billed To:", fg="gray", font=("Helvetica", 8, "bold")).place(relx=0.03, rely=0.3)
        Label(self.frame1, text="First name:",font=("Helvetica", 10)).place(relx=0.05, rely=0.4)

        Label(self.frame1, text="Last name:", font=("Helvetica", 10)).place(relx=0.05, rely=0.5)

        Label(self.frame1, text="Username:", font=("Helvetica", 10)).place(relx=0.05, rely=0.6)

        Label(self.frame1, text="Invoice Total:", fg="gray", font=("Helvetica", 8, "bold")).place(relx=0.8, rely=0.3)

        with open("logged_user.txt") as file:
            user = file.read()

        with open("users.csv", "r") as csv_file:
            read = csv.reader(csv_file)
            for row in read:
                if row:
                    if row[2] == user:
                        first = row[0]
                        last = row[1]

        Label(self.frame1, text=first, font=("Helvetica", 10)).place(relx=0.15, rely=0.4)
        Label(self.frame1, text=last, font=("Helvetica", 10)).place(relx=0.15, rely=0.5)
        Label(self.frame1, text=user, font=("Helvetica", 10)).place(relx=0.15, rely=0.6)

        with open(".\dump\hired_tools,year{},month{}.csv".format(yr, mth), "r") as file:
            read = csv.reader(file)
            for row in read:
                if row:
                    if row[0] == user and len(row) == 8:
                        used_for = datetime.datetime.strptime(row[7], "%Y-%m-%d %H:%M") - datetime.datetime.strptime(row[4], "%Y-%m-%d")
                        self.toolsinfo[row[3]] = {"tool":row[2], "owner":row[1], "used for":used_for}

        with open("tools.csv", "r") as file:
            read = csv.reader(file)
            for row in read:
                if row:
                    if row[4] in self.toolsinfo.keys():
                        print(self.toolsinfo.keys())
                        for k,v in self.toolsinfo[row[4]].items():
                            if k == "used for":
                                used_time = v

                        if used_time > datetime.timedelta(days=3):
                            total = int(row[2]) * 3
                            extra_time = used_time - datetime.timedelta(days=3)
                            extra_days = extra_time // datetime.timedelta(days=1)
                            extra_halfday = (extra_time - timedelta(extra_days)) // datetime.timedelta(days=0.5)
                            fine = (int(row[2]) * 2 * extra_days) + (int(row[3])* 2 * extra_halfday)
                            self.toolsinfo[row[4]].update({"fullday price": row[2], "halfday price": row[3], "fee":total, "fine":fine})

                        else:
                            fullday = used_time // datetime.timedelta(days=1)
                            halfday = (used_time - datetime.timedelta(fullday)) // datetime.timedelta(days=0.5)
                            total = (int(row[2]) * fullday) + (int(row[3]) * halfday)
                            self.toolsinfo[row[4]].update({"fullday price": row[2], "halfday price": row[3], "fee":total})

        n=1
        totals = []
        for v in self.toolsinfo.values():
            if "fine" in v.keys():
                total = int(v["fee"]) + int(v["fine"]) + 5
            else:
                total = int(v["fee"]) + 5

            label1 = Label(self.innerframe1, text="Tools",bg="aquamarine", width=10)
            label1.grid(row=0)
            label1.grid_propagate(False)
            label2 = Label(self.innerframe2, text="Owners",bg="aquamarine", width=10)
            label2.grid(row=0)
            label2.grid_propagate(False)
            label3 = Label(self.innerframe3, text ="Usage",bg="aquamarine", width=15)
            label3.grid(row=0)
            label3.grid_propagate(False)
            label4 = Label(self.innerframe4, text="Perday/Halfday Rate", bg="aquamarine", width=15)
            label4.grid(row=0)
            label4.grid_propagate(False)
            label5 = Label(self.innerframe5, text="Charge", bg="aquamarine", width=10)
            label5.grid(row=0)
            label5.grid_propagate(False)
            label5 = Label(self.innerframe6, text="Fine", bg="aquamarine", width = 10)
            label5.grid(row=0)
            label5.grid_propagate(False)
            label5 = Label(self.innerframe7, text="Insurance", bg="aquamarine", width = 10)
            label5.grid(row=0)
            label5.grid_propagate(False)
            label5 = Label(self.innerframe8, text="Total", bg="aquamarine", width = 10)
            label5.grid(row=0)
            label5.grid_propagate(False)


            label1 = Label(self.innerframe1, text=v["tool"], width=10)
            label1.grid(row=n)
            label1.grid_propagate(False)
            label2 = Label(self.innerframe2, text=v["owner"], width=10)
            label2.grid(row=n)
            label2.grid_propagate(False)
            label3 = Label(self.innerframe3, text=v["used for"], width=15)
            label3.grid(row=n)
            label3.grid_propagate(False)
            label4 = Label(self.innerframe4, text="£"+v["fullday price"]+"/£"+v["halfday price"], width=10)
            label4.grid(row=n)
            label4.grid_propagate(False)
            label5 = Label(self.innerframe5, text="£"+str(v["fee"]), width=10)
            label5.grid(row=n)
            label5.grid_propagate(False)
            if "fine" in v.keys():
                label6 = Label(self.innerframe6, text="£"+str(v["fine"]), width=10)
                label6.grid(row=n)
                label6.grid_propagate(False)
            else:
                label6 = Label(self.innerframe6, text="", width=10)
                label6.grid(row=n)
                label6.grid_propagate(False)
            label7 = Label(self.innerframe7, text="£5", width=10)
            label7.grid(row=n)
            label7.grid_propagate(False)
            label8 = Label(self.innerframe8, text="£{}".format(total), width=10)
            label8.grid(row=n)
            label8.grid_propagate(False)
            totals.append(total)
            n += 1

        invoice_total = 0
        for total in totals:
            invoice_total += total
        Label(self.frame1, text=invoice_total, font=("Helvetica", 24)).place(relx=0.85, rely=0.4)


root = Tk()
root.resizable(False,False)

w = root.winfo_screenwidth()
h = root.winfo_screenheight()

x = w//2 - 400
y = h//2 - 300

root.geometry("680x500+{}+{}".format(x, y))
Invoice(root)
root.mainloop()