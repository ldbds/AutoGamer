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
        frame = tk.Frame(self.root)
        frame.pack()

        for i in range(10):
            tk.Button(
                frame,
                text="%d"%i,
                command=lambda index=i: self.on_imagesearch(index)
            ).pack(side="left")
            
        tk.Button(
            frame,
            text="RUN",
            command=self.on_runsolve
        ).pack(side="left")

        self.label1 = label1
        self.frame = frame

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

            [left, top, right, bottom] = win32gui.GetWindowRect(handle);
            width = right-left
            height = bottom-top
            

            self.canvas.delete(self.last_rect);
            self.root.geometry("%sx%s+%s+%s" % (width, height+self.TOOLBAR_HEIGHT, left, top-self.TOOLBAR_HEIGHT))
            self.last_rect = self.canvas.create_rectangle(0,0,width,height,fill=TRANSCOLOUR,outline="blue")

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

            self.label1.config(cursor="hand2")

            pass
        elif (self.state == self.LOCATE):
            self.TOOLBAR_HEIGHT= self.label1.winfo_height() + self.frame.winfo_height()

            self.label1.config(cursor="cross")

            pass
        elif (self.state == self.RUNNING):

            pass
    
        pass

    def on_imagesearch(self,index):
        canvas_range = (
            self.canvas.winfo_rootx(),
            self.canvas.winfo_rooty(),
            self.canvas.winfo_width(),
            self.canvas.winfo_height()
            )

        #  matrix 16*10  LT (20,137) RB (398,767)
        pos_matrix = [[0] * 16] * 10

        OFFSETX = 20
        OFFSETY = 137
        GRIDX = 42
        GRIDY = 42

        pos_arr = pyautogui.locateAllOnScreen(
            "./res/image_%d.png"%index, 
            grayscale=True,
            region=canvas_range
            )


        if hasattr(self,"debug"):
            for ele in self.debug:
                self.canvas.delete(ele)
        self.debug=[]

        for pos in pos_arr :
            pt = pyautogui.center(pos)
            
            csx = self.canvas.winfo_rootx()
            csy = self.canvas.winfo_rooty()

            column = round((pt.x - csx - OFFSETX)/GRIDX + 0.5)
            row = round((pt.y - csy - OFFSETY)/GRIDY + 0.5)
       
            l,t,w,h = (pos.left-csx,pos.top-csy,pos.width,pos.height)
            self.debug.append(self.canvas.create_rectangle(l,t,l+w,t+h))
            self.debug.append(self.canvas.create_text(l,t, text="%d,%d"%(row,column), anchor='sw',fill='red'))
        pass

    def on_runsolve(self):
        pass
        

        

if __name__=="__main__":
    mypet = MyPet()
