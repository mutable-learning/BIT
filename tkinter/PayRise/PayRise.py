# This file creates a prank window to amuse the user
# as they try to click the 'yes' button
# Watch the video at https://youtu.be/F7QXmviNBF4

import tkinter as tk
from tkinter import ttk, messagebox
from random import randint


class PayRise(ttk.Frame):
    def __init__(self, master):
        self.master = master
        super().__init__(self.master)
        self.configure_ui()
        self.create_interface()

    def configure_ui(self):
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.style = ttk.Style(self)
        self.style.configure("TLabel", font=("Sans-serif", 24))
        self.style.configure("TButton", font=("Sans-serif", 14))

    def create_interface(self):
        self.heading = ttk.Label(
            self,
            text="Do you want a pay rise?",
            anchor=tk.CENTER
        )
        self.heading.grid(row=0, column=0, columnspan=2, sticky=tk.NSEW)

        self.yes = ttk.Button(self, text="Yes")
        self.yes.grid(row=1, column=0)
        self.yes.bind("<Enter>", self.move)

        self.no = ttk.Button(self, text="No", command=self.message)
        self.no.grid(row=1, column=1)

        self.yes.tkraise()

    def message(self):
        messagebox.showinfo("Good choice!", "You are right.")
        self.quit()

    def move(self, event):
        max_w = self.winfo_width() - self.yes.winfo_width()
        max_h = self.winfo_height() - self.yes.winfo_height()

        button_x = self.yes.winfo_x()
        button_y = self.yes.winfo_y()

        pos_x, pos_y = button_x, button_y

        while pos_x in range(button_x - self.yes.winfo_width(), button_x + self.yes.winfo_width()):
            pos_x = randint(1, max_w)
        while pos_y in range(button_y - self.yes.winfo_width(), button_y + self.yes.winfo_width()):
            pos_y = randint(1, max_h)

        self.yes.place(x=pos_x, y=pos_y)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Need a pay rise?")
    root.geometry("500x500")
    root.frame = PayRise(root)
    root.frame.pack(fill=tk.BOTH, expand=1)
    root.mainloop()
