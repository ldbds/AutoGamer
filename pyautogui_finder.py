
import pyautogui

import tkinter as tk

import win32gui as win32gui

import time as time
## tkinter 桌面宠物 https://blog.csdn.net/qq_44924355/article/details/128934280

TRANSCOLOUR = "white"

class MyPet():
    def __init__(self):
        self.IDLE = 0
        self.LOCATE = 1
        self.RUNNING = 2

        self.root = tk.Tk()

        self.root.attributes("-topmost",1)
        self.root.wm_attributes("-transparentcolor",TRANSCOLOUR)
        self.root.overrideredirect(True)
        self.root.geometry("200x200+{}+{}".format(100,100))
        self.root.config(background="red")

        
        label1 = tk.Label(
            text="拖动鼠标选择目标窗口,ALt+F4 关闭"
            )
        label1.pack()
        button1 = tk.Button(
            text="开始运行",
            command=self.run_solve
            )
        button1.pack()
        
        self.label1 = label1
        self.button1 = button1

        self.canvas = tk.Canvas(self.root, borderwidth=5,highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH,expand=tk.Y)
        self.canvas.config(background="red")

        self.last_rect = self.canvas.create_rectangle(0,0,200,200,fill=TRANSCOLOUR)

        
        self.on_statetrans(self.IDLE)
        self.root.mainloop()


    def on_mouseDown(self,event):

        self.on_statetrans(self.LOCATE)

    def on_motion(self,event):
        if (self.state == self.LOCATE):
            handle = win32gui.WindowFromPoint((event.x_root,event.y_root))
            self.button1.config(state="active")

            [left, top, right, bottom] = win32gui.GetWindowRect(handle);
            width = right-left
            height = bottom-top
            

            self.canvas.delete(self.last_rect);
            self.root.geometry("%sx%s+%s+%s" % (width, height+self.TOOLBAR_HEIGHT, left, top-self.TOOLBAR_HEIGHT))
            self.last_rect = self.canvas.create_rectangle(0,0,width,height,fill=TRANSCOLOUR)

        pass
        
    def on_mouseUp(self,event):
        
        self.on_statetrans(self.IDLE)
        pass

    def on_statetrans(self,newstate):
        self.state = newstate
        self.label1.bind("<ButtonPress-1>",self.on_mouseDown)
        self.label1.bind("<B1-Motion>",self.on_motion)
        self.label1.bind("<ButtonRelease-1>",self.on_mouseUp)

        if   (self.state == self.IDLE):

            self.button1.config(state="active")
            self.label1.config(cursor="hand2")

            pass
        elif (self.state == self.LOCATE):
            self.TOOLBAR_HEIGHT= self.label1.winfo_height() + self.button1.winfo_height()

            self.label1.config(cursor="cross")

            pass
        elif (self.state == self.RUNNING):

            self.button1.config(state="disabled")
            pass

    def run_solve(self):

        self.on_statetrans(self.RUNNING)
        self.on_imagesearch()

        pass

    def on_imagesearch(self):
        self.targetpx = pyautogui.screenshot()
        ptx , pty = pyautogui.position() 

        csx = self.canvas.winfo_rootx()
        csy = self.canvas.winfo_rooty()

        cx = ptx-csx
        cy = pty-csy

        color = self.targetpx.getpixel((ptx,pty))

        if hasattr(self,"debugtxt"):
            self.canvas.delete(self.debugtxt)
        self.debugtxt = self.canvas.create_text(100,100,text='x:%d y:%d color:(%3d,%3d,%3d)'%(cx,cy,color[0],color[1],color[2]))
        self.root.after(100, self.on_imagesearch)

        pass

if __name__=="__main__":
    mypet = MyPet()
