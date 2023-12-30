import pyautogui

import tkinter as tk

import win32gui as win32gui

from PIL import Image, ImageOps

import threading

## tkinter 桌面宠物 https://blog.csdn.net/qq_44924355/article/details/128934280

TRANSCOLOUR = "white"

OPTION_DEBUG = False

OFFSETX = 20
OFFSETY = 137
GRIDX = 42
GRIDY = 42
 
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
        screenshot = pyautogui.screenshot()
        canvas_range = (
            self.canvas.winfo_rootx(),
            self.canvas.winfo_rooty(),
            self.canvas.winfo_width(),
            self.canvas.winfo_height()
            )

        screenshot = screenshot.crop((canvas_range[0], canvas_range[1], canvas_range[0] + canvas_range[2], canvas_range[1] + canvas_range[3]))
        screenshot = ImageOps.grayscale(screenshot)

        screenshot = screenshot.point(lambda x: 0 if x < 10 else 255,'1')

        patternFileObj = open("./res/image_%d.png"%index, 'rb')
        patternImg = Image.open(patternFileObj)
        patternImg = ImageOps.grayscale(patternImg)
        
        patternImg = patternImg.point(lambda x: 0 if x < 10 else 255,'1')
        # patternImg.save("./res/image_%d.png"%index)

        #  matrix 16*10  LT (20,137) RB (398,767)
        pos_matrix = [[0] * 10] * 16

        pos_arr = pyautogui.locateAll(
            needleImage = patternImg,
            haystackImage= screenshot,
            grayscale=True
            )


        if hasattr(self,"debug"):
            for ele in self.debug:
                self.canvas.delete(ele)
        self.debug=[]

        for pos in pos_arr :
            pt = pyautogui.center(pos)
            
            column = round((pt.x  - OFFSETX)/GRIDX + 0.5)
            row = round((pt.y  - OFFSETY)/GRIDY + 0.5)
       
            l,t,w,h = (pos.left,pos.top,pos.width,pos.height)
            self.debug.append(self.canvas.create_rectangle(l,t,l+w,t+h))
            self.debug.append(self.canvas.create_text(l,t, text="%d,%d"%(row,column), anchor='sw',fill='red'))
        pass

    def on_runsolve(self):
        
        screenshot = pyautogui.screenshot()
        error = False
        ## Step1: sample
        canvas_range = (
            self.canvas.winfo_rootx(),
            self.canvas.winfo_rooty(),
            self.canvas.winfo_width(),
            self.canvas.winfo_height()
            )

        screenshot = screenshot.crop((canvas_range[0], canvas_range[1], canvas_range[0] + canvas_range[2], canvas_range[1] + canvas_range[3]))
        screenshot = ImageOps.grayscale(screenshot)

        screenshot = screenshot.point(lambda x: 0 if x < 10 else 255,'1')

        #  matrix 16*10  LT (20,137) RB (398,767)
        pos_matrix = [ [0 for _ in range(10)]  for _ in range(16)]

        if hasattr(self,"debug"):
            for ele in self.debug:
                self.canvas.delete(ele)
        self.debug=[]
        
        for index in range(1,10):
            pos_arr = pyautogui.locateAll(
                needleImage = "./res/image_%d.png"%index,
                haystackImage = screenshot,
                grayscale=True
                )

            for pos in pos_arr :
                pt = pyautogui.center(pos)
                
                column = round((pt.x - OFFSETX)/GRIDX + 0.5)-1
                row = round((pt.y - OFFSETY)/GRIDY + 0.5)-1

                try:
                    pos_matrix[row][column] = index
                except:
                    error = True

                l,t,w,h = (pos.left,pos.top,pos.width,pos.height)
                
                if OPTION_DEBUG:
                    # self.debug.append(self.canvas.create_rectangle(l,t,l+w,t+h))
                    self.debug.append(self.canvas.create_text(l,t, text="%d"%(index), anchor='sw',fill='red'))

        if not(error):

            ## Step2: solve
            self.solution = self.solve(pos_matrix)

            ## Step3: run solution
            self.root.after(50, self.run_solution)

        pass
 
    def solve(self, matrix):
        solution = []

        def find_in_neighbour(row,col,target):
            candi =[]

            r = row ; c = col
            while(r > 0):
                r = r-1
                if not(matrix[r][c] == 0):
                    candi.append((r,c)); break

            r = row ; c = col
            while(r < len(matrix)-1):
                r = r+1
                if not(matrix[r][c] == 0):
                    candi.append((r,c)); break
                      
            r = row ; c = col
            while(c > 0):
                c = c-1
                if not(matrix[r][c] == 0):
                    candi.append((r,c)); break
                    
            r = row ; c = col
            while(c < len(matrix[0])-1):
                c = c+1
                if not(matrix[r][c] == 0):
                    candi.append((r,c)); break

            for (r, c) in candi:
                if (matrix[r][c] == target):
                    solution.append(((row,col),(r,c)))
                    matrix[row][col] = 0
                    matrix[r][c] = 0
                    break
        
        # first 
        for row in range(len(matrix)):
            for col in range(len(matrix[0])):
                val = matrix[row][col]
                if (val >= 5):
                    find_in_neighbour(row,col, 10-val)
        # second
        for row in range(len(matrix)):
            for col in range(len(matrix[0])):
                val = matrix[row][col]
                if (val >= 5):
                    find_in_neighbour(row,col, 10-val)
        return solution


    def run_solution(self):
        # need self.solution
        
        csx = self.canvas.winfo_rootx()
        csy = self.canvas.winfo_rooty()

        try:
            step = self.solution.pop(0)
            x1 = (step[0][1] +0.5) * GRIDX+ OFFSETX +csx
            y1 = (step[0][0] +0.5) * GRIDY+ OFFSETY +csy
            x2 = (step[1][1] +0.5) * GRIDX+ OFFSETX +csx
            y2 = (step[1][0] +0.5) * GRIDY+ OFFSETY +csy

            pyautogui.moveTo(x1,y1)

            pyautogui.mouseDown()

            pyautogui.dragTo(x2,y2,duration=0.1)

            pyautogui.mouseUp()
            
            self.root.after(50, self.run_solution)
        except:
            pass
        pass


if __name__=="__main__":
    mypet = MyPet()



