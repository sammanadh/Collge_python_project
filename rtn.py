from tkinter import *
import csv
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import datetime
from PIL import Image
import shutil
import os

class Return():

    def __init__(self, master):
        self.master = master
        self.dic = {}
        self.filename = ""
        self.bg_img = PhotoImage(file="return.png")
        self.bg_label = Label(self.master, image=self.bg_img)
        self.bg_label.place(x=0, y=0, relheight=1, relwidth=1)

        Label(self.master, text="Return Tool", font=("Helvetica", 18), bg="orange").place(relx=0.39, rely=0.04)

        with open("logged_user.txt", "r") as file:
            self.user = file.read()

        with open("hired_tools.csv", "r") as file:
            read = csv.reader(file)
            lst = []
            for row in read:
                if row:
                    if row[0] == self.user:
                        str = "{}'s: {}".format(row[1], row[2])
                        lst.append(str)

        lst.insert(0, "Please select the tool")

        self.cb = ttk.Combobox(self.master, state="readonly", value=lst, font=("Helvetica", 18))
        self.cb.current(0)
        self.cb.place(relx=0.3, rely=0.4)

        Button(self.master, text="Upload tool's image",bg="aquamarine", font=("Helvetica", 16) , command=self.fileDialog).place(relx=0.36, rely=0.5)

        Label(self.master, text="Note (say something about tools condition):", bg="gray", font=("Helvetica", 14)).place(relx=0.24, rely=0.6)

        self.text = Text(self.master, undo=True, maxundo=20, width=35, height=5)
        self.text.place(relx=0.3, rely=0.65)

        Button(self.master, text="Return", command=self.saveimage, bg="aquamarine", font=("Helvetica", 16)).place(relx=0.45, rely=0.86)

        Button(text="Back", command=self.back, bg="red", font=("Helvetica", 16)).place(relx=0.91, rely=0.94)

    #Creates a file dialog for uploading tool's image
    def fileDialog(self):
        self.filename = filedialog.askopenfilename(initialdir="...", title="Open Picture File",
                                   filetypes=(("Image files", "*.jpg"),("Image files", "*.png"),("Image files", "*.jpeg"),("All Files", "*.*")))

    #Saves the image and notes in 'returned_tools' directory
    def saveimage(self):
        val = self.cb.get()
        if val == "Please select the tool":
            messagebox.showerror(message="Please select the tool")

        else:
            lt = val.split("'s: ")
            if self.filename == "":
                messagebox.showerror(message="You need to add an image of the tool.")
            else:
                try:
                    with open("hired_tools.csv", "r") as file:
                        read = csv.reader(file)
                        for row in read:
                            if row:
                                if row[0] == self.user and row[1] == lt[0] and row[2] == lt[1]:
                                    self.toolid = row[3]

                    img = Image.open(self.filename)
                    resized_img = img.resize((400, 400))
                    resized_img.save('{}.png'.format(self.toolid))
                    path = r'.\returned_tools'
                    shutil.move('{}.png'.format(self.toolid), path)
                    self.savenote()

                except shutil.Error:
                    messagebox.showerror(message="The tool has already been returned")
                    os.remove('{}.png'.format(self.toolid))

    #Saves tool's notes in return_tools directory.
    def savenote(self):
        with open("{}.txt".format(self.toolid), "w") as file:
            file.write(self.text.get("1.0", END))
        shutil.move('{}.txt'.format(self.toolid), r'.\returned_tools')
        self.rtn()

    #Marks the hired tool as returned(yes) and also saves the time of return
    def rtn(self):
        val = self.cb.get()
        lt = val.split("'s: ")
        with open("hired_tools.csv", "r") as file:
            lst = []
            read = csv.reader(file)
            for row in read:
                if row:
                    if row[3] == self.toolid :
                        str = "yes"
                        dt = datetime.datetime.today().strftime("%Y-%m-%d %H:%M")
                        row.append(str)
                        row.append(dt)
                        lst.append(row)
                    else:
                        lst.append(row)
            messagebox.showinfo(message = "You have succefully returned the tool")
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
y = h//2 - 350

root.geometry("677x650+{}+{}".format(x, y))


Return(root)

root.mainloop()
