from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage

names = set()


class MainUI(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        with open("nameslist.txt", "r") as f:
            x = f.read()
            z = x.rstrip().split(" ")
            for i in z:
                names.add(i)
        self.title_font = tkfont.Font(family='Courier New', size=16, weight="bold")
        self.title("Student Recognition System")
        self.resizable(False,False )
        self.geometry("800x450")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
            frame = self.frames[page_name]
            frame.tkraise()

    def on_closing(self):

        if messagebox.askokcancel("Quit", "Are you sure?"):
            global names
            f =  open("nameslist.txt", "a+")
            for i in names:
                    f.write(i+" ")
            self.destroy()


class StartPage(tk.Frame):

        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent)
            self.controller = controller
            self.configure(bg='black')
            render = PhotoImage(file='homepagepic.png')
            img = tk.Label(self, image=render)
            img.image = render
            img.configure(bg='black')
            img.grid(row=3, column=0, rowspan=9, sticky="w") 
            label = tk.Label(self, text="          S.R.S Bio-Metric Authentication", font=self.controller.title_font,fg="red")
            label.grid(row=2, sticky="n")
            label.configure(bg='black')
            button1 = tk.Button(self, text="   Add Student  ", fg="red", bg='cyan',command=lambda: self.controller.show_frame("PageOne"))
            button2 = tk.Button(self, text="   Check Student  ", fg="red", bg="cyan",command=lambda: self.controller.show_frame("PageTwo"))
            button3 = tk.Button(self, text="Quit", bg="grey", fg="black", command=self.on_closing)
            button1.grid(row=4, column=1, ipady=15, ipadx=40)
            button2.grid(row=6, column=1, ipady=15, ipadx=40)
            button3.grid(row=8, column=1, ipady=8, ipadx=20)


        def on_closing(self):
            if messagebox.askokcancel("Quit", "Are you sure?"):
                global names
                with open("nameslist.txt", "w") as f:
                    for i in names:
                        f.write(i + " ")
                self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='black')
        tk.Label(self, text="Enter the name", fg='red',bg='black', font='Helvetica 16 bold').grid(row=1, column=0, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="cyan", font='Helvetica 11')
        self.user_name.grid(row=1, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Cancel", fg="red", bg='cyan', command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Next", fg="red", bg='cyan', command=self.start_training)
        self.buttoncanc.grid(row=2, column=0, pady=30, ipadx=15, ipady=12)
        self.buttonext.grid(row=2, column=1,  pady=30, ipadx=15, ipady=12)
    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Name cannot be 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "Student already exists!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Name cannot be empty!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        self.configure(bg='black')
        tk.Label(self, text="Select user", fg='red',bg='black', font='Helvetica 16 bold').grid(row=0, column=0, padx=10, pady=10)
        self.buttoncanc = tk.Button(self, text="Cancel", command=lambda: controller.show_frame("StartPage"),fg="red", bg='cyan')
        self.menuvar = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.menuvar, *names)
        self.dropdown.config(bg="grey")
        self.dropdown["menu"].config(bg="grey")
        self.buttonext = tk.Button(self, text="Next", command=self.nextfoo,fg="red", bg='cyan')
        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)

    def nextfoo(self):
        if self.menuvar.get() == "None":
            messagebox.showerror("ERROR", "Name cannot be 'None'")
            return
        self.controller.active_name = self.menuvar.get()
        self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.menuvar.set('')
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name, command=tk._setit(self.menuvar, name))

class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='black')
        self.numimglabel = tk.Label(self, text="Number of images captured = 0", font='Helvetica 16 bold', fg='red',bg='black')
        self.numimglabel.grid(row=1, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Capture", fg="red", bg='cyan', command=self.capimg)
        self.trainbutton = tk.Button(self, text="Train The Model", fg="red", bg='cyan',command=self.trainmodel)
        self.capturebutton.grid(row=2, column=0, ipadx=10, ipady=8, padx=20, pady=40)
        self.trainbutton.grid(row=2, column=1, ipadx=10, ipady=8, padx=20, pady=40)

    def capimg(self):
        self.numimglabel.config(text=str("Captured Images = 0 "))
        messagebox.showinfo("INSTRUCTIONS", "We will Capture 300 pic of your Face.")
        x = start_capture(self.controller.active_name)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Number of images captured = "+str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < 300:
            messagebox.showerror("ERROR", "No enough Data, Capture at least 300 images!")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("SUCCESS", "The model has been successfully trained!")
        self.controller.show_frame("PageFour")


class PageFour(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.configure(bg='black')
        label = tk.Label(self, text="Face Recognition", font='Helvetica 20 bold',fg='red',bg='black')
        label.grid(row=1,column=0, sticky="ew")
        button1 = tk.Button(self, text="Face Recognition", command=self.openwebcam, fg="red", bg='cyan')
        button4 = tk.Button(self, text="Go to Home Page", command=lambda: self.controller.show_frame("StartPage"), fg="red", bg='cyan')
        button1.grid(row=2,column=0, sticky="ew", ipadx=10, ipady=8, padx=20, pady=20)
        button4.grid(row=2,column=1, sticky="ew", ipadx=10, ipady=8, padx=20, pady=20)

    def openwebcam(self):
        main_app(self.controller.active_name)
   


app = MainUI()
app.configure(bg='black')
app.iconphoto(False, tk.PhotoImage(file='icon.ico'))
app.mainloop()

