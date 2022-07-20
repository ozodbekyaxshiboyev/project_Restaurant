from model import Manager,Table,Basemodel,Cook,Product,Drink
import os



from tkinter import *
from menu import makeMenu

window = Tk()
window.title(" RESTORAN  MILLIY TAOMLAR ")
# from styles import style

menubar = makeMenu(window)
window.config(menu=menubar,  bg = "#706c3d")
window.state('zoomed')

label1 = Label(window, text="Restoran   MILLIY TAOMLAR ",  bg="#003723", fg="#DAE6E5",height = 700, width = 800)
label1.config(font=("Arial", 50))
label1.pack()
window.mainloop()

