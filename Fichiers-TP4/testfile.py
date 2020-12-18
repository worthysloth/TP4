from tkinter import *
from winsound import *

root = Tk() # create tkinter window

play = lambda: PlaySound('sf_laser_15.wav', SND_FILENAME)
button = Button(root, text = 'Play', command = play)

button.pack()
root.mainloop()