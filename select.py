from tkinter import *
import os

root = Tk()
root.resizable(False, False)

w = root.winfo_screenwidth()
h = root.winfo_screenheight()

x = w//2 - 350
y = h//2 - 350

root.geometry("677x650+{}+{}".format(x,y))
bg_img = PhotoImage(file="Dashboard.png")
bg_label = Label(image=bg_img)
bg_label.place(x=0, y=0, relheight=1, relwidth=1)

def upload():
    root.destroy()
    os.system("python ./upload_tools.py")

def search():
    root.destroy()
    os.system("python ./search_tools.py")

def rtrn():
    root.destroy()
    os.system("python ./rtn.py")

def logout():
    root.destroy()
    with open("logged_user.txt", "w") as file:
        file.write("")
    os.system("python ./login.py")

Button(text ="Search for tools",command=search, font=("Helvetica",14), width=40).place(relx=0.18, rely=0.605)
Button(text="Upload tools", command=upload, font=("Helvetica",14), width=40).place(relx=0.18, rely=0.695)
Button(text="Return tools", command=rtrn, font=("Helvetica",14), width=40).place(relx=0.18, rely=0.787)
Button(text="Logout",fg="brown",font=("Helvetica",14), command=logout, width=40).place(relx=0.18, rely=0.87)

root.mainloop()