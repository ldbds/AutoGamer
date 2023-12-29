import pyautogui

import tkinter as tk

import win32gui as win32gui


## tkinter 桌面宠物 https://blog.csdn.net/qq_44924355/article/details/128934280

TRANSCOLOUR = "white"

class MyPet():
    def __init__(self):
        self.IDLE = 0
        self.LOCATE = 1
        self.RUNNING = 2

        self.state = self.IDLE

        self.root = tk.Tk()

        self.root.attributes("-topmost",1)
        self.root.wm_attributes("-transparentcolor",TRANSCOLOUR)
        self.root.overrideredirect(True)
        self.root.geometry("200x200+{}+{}".format(100,100))
        self.root.config(background="red")

        #self.root.bind("<ButtonPress-1>",self.on_motion)
        self.root.bind("<B1-Motion>",self.on_motion)
        self.root.bind("<ButtonRelease-1>",self.on_mouseUp)
        self.root.bind("<ButtonPress-1>",self.on_mouseDown)
        
        label1 = tk.Label(
            text="拖动鼠标选择目标窗口,ALt+F4 关闭"
            )
        label1.pack()
        button1 = tk.Button(
            text="开始运行",
            default='disabled'
            )
        button1.config(state="disabled")
        button1.pack()
        
        self.label1 = label1
        self.button1 = button1

        self.canvas = tk.Canvas(self.root, borderwidth=5,highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH,expand=tk.Y)
        self.canvas.config(background="red")

        self.last_rect = self.canvas.create_rectangle(0,0,200,200,fill=TRANSCOLOUR)

        self.root.config(cursor="hand2")
        self.root.mainloop()

    def on_mouseDown(self,event):
        self.TOOLBAR_HEIGHT= self.label1.winfo_height() + self.button1.winfo_height()
        self.root.config(cursor="cross")
        self.state = self.LOCATE

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
        self.root.config(cursor="hand2")
        
        self.state == self.IDLE
        pass
        
        
if __name__=="__main__":
    mypet = MyPet()

## tkinter 窗口
# root = tk.Tk()
# root.title("作弊器")

# def popup_window():
#     popup = tk.Toplevel()
#     popup.title("完成")
#     label = tk.Label(popup, text="完成")
#     label.pack()

# tk.Label(root, text="移动下方准心到目标窗口").pack()
# popup_button = tk.Button(root,text="运行",command=popup_window)
# popup_button.pack()

# root.mainloop()

## PYAUTOGUI

# pyautogui.moveTo(100,200)

# pyautogui.mouseDown()

# pyautogui.dragTo(300,400,duration=5)

# pyautogui.mouseUp()
