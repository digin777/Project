from tkinter import *
from urllib.request import urlopen
import pygame
from PIL import ImageTk,Image
window=Tk()
window.overrideredirect(True)
#window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
window.configure(background='#283747')
#render=ImageTk.PhotoImage(file="E:\IMAGES\Logo.png")
canvas=Canvas(window,width=1000,height=1000)
canvas.pack()
b=Button(text='Ok')
b.place()
#canvas.create_image(0,0,anchor=NW,image=render)
pygame.init()
#pygame.mixer.music.load("E:\MUSIC\Kaashithumba_Kaavayi_Neelavaanam.mp3")
#pygame.mixer.music.play()
#window.destroy()
window.mainloop()
