from tkinter import *
import time

class StopWatch(Frame):
    msec = 50
    def __init__(self,parent=None,**kw):
        Frame.__init__(self, parent, **kw)
        self._start = 0.0
        self._elapsedtime = 0.0
        self._running = False
        self.timestr = StringVar()
        self.makeWidgets()
    
    def makeWidgets(self):
        l = Label(self, textvariable=self.timestr)
        self._setTime(self._elapsedtime)
        l.pack(fill=X,expand=NO, pady=2, padx=2)
    
    def _update(self):
        self._elapsedtime = time.time() - self._start
        self._setTime(self._elapsedtime)
        self._timer = self.after(self.msec, self._update)
        
    def _setTime(self,elap):
        minutes = int(elap/60)
        seconds = int(elap - minutes*60.0)
        hseconds = int((elap - minutes*60.0 -seconds)*100)
        self.timestr.set('%02d:%02d:%02d' % (minutes, seconds, hseconds))
        
    def Start(self):
        if not self._running:
            self._start = time.time() - self._elapsedtime
            self._update()
            self._running = True
            
    def Stop(self):
        if self._running:
            self.after_cancel(self._timer)
            self._elapsedtime = time.time() - self._start
            self._setTime(self._elapsedtime)
            self._running = False
    
    def Reset(self):
        self._start = time.time()
        self._elapsedtime = 0.0
        self._setTime(self._elapsedtime)

if __name__ == '__main__':
    def main():
        root = Tk()
        sw = StopWatch(root)
        sw.pack(side=TOP)
        Button(root,text='Start',command=sw.Start).pack(side=LEFT)
        Button(root,text='Stop',command=sw.Stop).pack(side=LEFT)
        Button(root,text='Reset',command=sw.Reset).pack(side=LEFT)
        Button(root,text='Quit',command=root.quit).pack(side=LEFT)
        root.mainloop()
    main()