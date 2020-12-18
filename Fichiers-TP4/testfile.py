import tkinter as tk
import winsound

mywindow = tk.Tk()

def buttonPress():
    winsound.PlaySound('sf_laser_15.wav', winsound.SND_FILENAME)
    print("Button Pressed!!")

# Button
button = tk.Button(mywindow,text='Press',command=buttonPress)
button.grid(row=1,column=1)

# Title Bar Icon
#mywindow.iconbitmap('birdy_icon.ico')
mywindow.mainloop()