from tkinter import *
from tkinter import messagebox
import csv
from tkinter import filedialog
from PIL import Image
import shutil
import uuid
import os

class UploadTools():

    def __init__(self, master):
        self.master = master
        self.imglocation = ""

        self.bg_img = PhotoImage(file="upload.png")
        self.bg_label = Label(self.master, image=self.bg_img)
        self.bg_label.place(relheight=1, relwidth=1)

        Label(self.master, text = "Tool's name", bg="gray",font=("Helvetica", 16)).place(relx=0.2, rely=0.35)
        self.entry1 = Entry(self.master, font=("Aerial", 16))
        self.entry1.place(relx=0.48, rely=0.35)

        Label(self.master, text = "Per day rate(£)", bg="gray",font=("Helvetica", 16)).place(relx=0.2, rely=0.4)
        self.entry2 = Entry(self.master, font=("Aerial", 16))
        self.entry2.place(relx=0.48, rely=0.4)


        Label(self.master, text = "Half day rate(£)", bg="gray",font=("Helvetica", 16)).place(relx=0.2, rely=0.45)
        self.entry3 = Entry(self.master, font=("Aerial", 16))
        self.entry3.place(relx=0.48, rely=0.45)

        Button(text="upload tool's image", command=self.imageDialog, bg="aquamarine", font=("Helvetica", 20)).place(relx=0.315, rely=0.55)

        Label(self.master, text="Note (say something about tools condition):", bg="gray",font=("Helvetica", 14)).place(relx=0.24, rely=0.65)

        self.text = Text(self.master, undo=True, maxundo=20, width=35, height=5)
        self.text.place(relx=0.3, rely=0.7)

        Button(text="Upload", command = self.savetool, bg="aquamarine", font=("Helvetica", 16)).place(relx=0.45, rely=0.86)
        Button(text="Back", command=self.back, bg="red", font=("Helvetica", 16)).place(relx=0.91, rely=0.94)

    # creates an file dialog for uploading image
    def imageDialog(self):
        self.imglocation = filedialog.askopenfilename(initialdir="...", title="Upload tool's image",
                                   filetypes=(("Image files", "*.jpg"), ("Image files", "*.png"), ("Image files", "*.jpeg")))

    #saves the entries into tools.csv and also checks if the image has been uploaded or not
    def savetool(self):
        self.id = uuid.uuid4()

        lst = []
        lst.append(self.entry1.get())
        lst.append(self.entry2.get())
        lst.append(self.entry3.get())

        while True:
            str = ""
            if str in lst:
                messagebox.showerror(message="Please completely fill the entries")
                break

            if lst[1].isdigit() == False or lst[2].isdigit() == False:
                messagebox.showerror(message="Please enter numbers as halfdayday or fullday price.")
                break

            if self.imglocation == "":
                messagebox.showerror(message="Please upload the tool's image")
                break

            lst.append(self.id)

            with open("logged_user.txt", "r") as file:
                loggedUser = file.read()
                lst.insert(0, loggedUser)

            with open("tools.csv", "a") as csv_file:
                write_file = csv.writer(csv_file)
                write_file.writerow(lst)
            self.saveimg()
            break

    #Saves the image in 'upload tools' directory
    def saveimg(self):
            img = Image.open(self.imglocation)
            resized_img = img.resize((400, 400))
            resized_img.save('{}.png'.format(self.id))
            path = r'.\upload_tools'
            shutil.move('{}.png'.format(self.id), path)
            self.savenote()

    # Saves tool's notes in return_tools directory.
    def savenote(self):
            with open("{}.txt".format(self.id), "w") as file:
                file.write(self.text.get("1.0", END))
            shutil.move('{}.txt'.format(self.id), r'.\upload_tools')
            messagebox.showinfo(message="Tool successfully uploaded")
            self.master.destroy()
            os.system("python ./select.py")

    #Returns to the select page
    def back(self):
        self.master.destroy()
        os.system("python ./select.py")

root = Tk()
root.title("Upload Tools")
root.resizable(False,False)

w = root.winfo_screenwidth()
h = root.winfo_screenheight()

x = w//2 - 350
y = h//2 - 350

root.geometry("677x650+{}+{}".format(x,y))
UploadTools(root)
root.mainloop()






