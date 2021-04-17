from tkinter import *
from tkinter import ttk
from tkinter.tix import Tk, Control, ComboBox  #升级的组合控件包
import cv2 as cv
from PIL import Image,ImageTk
import main
import threading#多线程
from tkinter.messagebox import showinfo, showwarning, showerror #各种类型的提示框

#---------------打开摄像头获取图片
def video_demo():
    cv.destroyAllWindows()
    main.work(comboExample.current()+1)
    video_show()

def video_show():
    def cc():
        capture = cv.VideoCapture(0)
        while True:
            ret, frame = capture.read()#从摄像头读取照片
            frame = cv.flip(frame, 1)#翻转 0:上下颠倒 大于0水平颠倒
            cv2image = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            image_file=ImageTk.PhotoImage(img)
            canvas.create_image(0,0,anchor="nw",image=image_file)
    t=threading.Thread(target=cc)
    t.start()

root = Tk() # 初始化Tk()
root.title("服创开发图片集标记工具-Made by Sensorjang")    # 设置窗口标题
root.geometry("1000x800")    # 设置窗口大小 注意：是x 不是*
root.resizable(width=True, height=True) # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True
root.tk.eval('package require Tix')  #引入升级包，这样才能使用升级的组合控件

lable = Label(root, text="program for deviding vedio made by QP", bg="gray",bd=10, font=("Arial",24), width=40, height=3)
lable.pack(side=TOP)

canvas=Canvas(root,width=800,height=600)
canvas.pack(side=LEFT)

button=Button(root,text='Ref Cap',command=video_show,activeforeground="black",activebackground='blue',bg='green',fg='white')
button.pack(side=LEFT)

button=Button(root,text='START',command=video_demo,activeforeground="black",activebackground='blue',bg='red',fg='white')
button.pack(side=RIGHT)

comboExample = ttk.Combobox(root,
                            values=[
                                "点击1",
                                "平移2",
                                "缩放3",
                                "抓取4",
                                "旋转5"])
comboExample.pack(side=RIGHT)
comboExample.current(0)

video_show()

root.mainloop()

