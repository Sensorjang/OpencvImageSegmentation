import cv2
import time
import numpy as np
import os
from tkinter import *
from tkinter import ttk
import hashlib
from tkinter.tix import Tk, Control, ComboBox  #升级的组合控件包
from PIL import Image,ImageTk

n = 1 #帧图像计数
imgname = 1 #间隔timeF帧图像计数
imgfinname = 0 #拼合图像计数
timeF = 5  #视频帧计数间隔频率
mergeNum = 6  #拼接图片数
typeS = 999 #type寄存器

def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print(path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')
        return False

def del_file(path_data):
    for i in os.listdir(path_data) :# os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = path_data + "\\" + i#当前文件夹的下面的所有东西的绝对路径
        if os.path.isfile(file_data) == True:#os.path.isfile判断是否为文件,如果是文件,就删除.如果是文件夹.递归给del_file.
            os.remove(file_data)
        else:
            del_file(file_data)

mkdirpath = "./RsOutput/IMG"
mkdir(mkdirpath)
mkdirpath = "./RsOutput/IMGFIN"
mkdir(mkdirpath)
mkdirpath = "./RsOutput/IMGFINSPE"
mkdir(mkdirpath)
mkdirpath = "./RsOutput/IMGFINNML"
mkdir(mkdirpath)
mkdirpath = "./RsOutput/ImgResults"
mkdir(mkdirpath)

def cr_otsu(img):
    global imgfinname
    """YCrCb颜色空间的Cr分量+Otsu阈值分割
    :param image: 图片路径
    :return: None
    """
    #img = cv2.imread(image, cv2.IMREAD_COLOR)
    ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCR_CB)

    (y, cr, cb) = cv2.split(ycrcb)
    cr1 = cv2.GaussianBlur(cr, (5, 5), 0)
    _, skin = cv2.threshold(cr1,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    dst = cv2.bitwise_and(img, img, mask=skin)

    # cv2.namedWindow("image raw", cv2.WINDOW_NORMAL)
    # cv2.imshow("image raw", img)
    # cv2.namedWindow("image CR", cv2.WINDOW_NORMAL)
    # cv2.imshow("image CR", cr1)
    # cv2.namedWindow("Skin Cr+OTSU", cv2.WINDOW_NORMAL)
    # cv2.imshow("Skin Cr+OTSU", skin)
    # cv2.namedWindow("seperate", cv2.WINDOW_NORMAL)
    # cv2.imshow("seperate", dst)

    cv2.imwrite('./RsOutput/IMGFIN/'+ str(imgfinname) + '.jpg',skin) #存储为图像
    cv2.imwrite('./RsOutput/IMGFINSPE/'+ str(imgfinname) + '.jpg',dst) #存储为图像
    cv2.imwrite('./RsOutput/IMGFINNML/'+ str(imgfinname) + '.jpg',img) #存储为图像

    makesure(dst)

def makesure(skin):
    def delt():
        cv2.destroyWindow("frame")
        cv2.destroyWindow("RESULT")
        root2.destroy()
    def suss():
        save()
        cv2.destroyWindow("frame")
        cv2.destroyWindow("RESULT")
        root2.destroy()
    root2 = Tk() # 初始化Tk()
    root2.title("INDEX")    # 设置窗口标题
    root2.geometry("400x400")    # 设置窗口大小 注意：是x 不是*
    root2.resizable(width=True, height=True) # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True
    root2.tk.eval('package require Tix')  #引入升级包，这样才能使用升级的组合控件

    lable = Label(root2, text="Do u want to save the result pic?", bg="blue",bd=10, font=("Arial",12), width=30, height=3)
    lable.pack(side=TOP)

    button=Button(root2,text='Confirm',command=suss,activeforeground="black",activebackground='blue',bg='green',fg='white')
    button.pack(side=BOTTOM)

    button=Button(root2,text='Delete',command=delt,activeforeground="black",activebackground='blue',bg='red',fg='white')
    button.pack(side=BOTTOM)

    cv2.namedWindow("RESULT", cv2.WINDOW_GUI_EXPANDED)
    cv2.imshow("RESULT",skin)

    root2.mainloop()


def hash_code(*args, **kwargs):
    """
    Generate 64-strings(in hashlib.sha256()) hash code.
    :param args: for any other position args packing.
    :param kwargs: for any other key-word args packing.
    :return: 64-strings long hash code.
    """
    text = ''
    if not args and not kwargs:
        text += time.strftime('%Y-%m-%d %H:%M:%S')
    if args:
        for arg in args:
            text += str(arg)
    if kwargs:
        for kwarg in kwargs:
            text += str(kwargs[kwarg])
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def makefile(path,content):
    if os.path.exists(path):
        if os.path.isdir(path):
            f = open('./RsOutput/ImgResults/results.txt','a+')
            f.write(content)
            f.seek(0)
            read = f.readline()
            f.close()
            print(read)
        else:
            print('please input the dir name')
    else:
        print('the path is not exists')

def save():
    hash = hash_code()
    print(hash)
    img = cv2.imread('./RsOutput/IMGFINSPE/1.jpg')
    cv2.imwrite('./RsOutput/ImgResults/'+ hash +                              '.jpg',img) #存储为图像
    path = "./RsOutput/ImgResults"
    makefile(path,hash+".jpg "+str(typeS)+"\n")


def work(type):
    global imgname
    global imgfinname
    global n
    global timeF
    global mergeNum
    global typeS
    n = 1 #帧图像计数
    imgname = 1 #间隔timeF帧图像计数
    imgfinname = 0 #拼合图像计数
    timeF = 5  #视频帧计数间隔频率
    mergeNum = 6  #拼接图片数
    typeS = type

    print(type)

    cap = cv2.VideoCapture(0)  # 默认参数0，为本机摄像头——即计算机摄像头/也可以传入非零数据，置换其它多媒体端口
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    if not cap.isOpened():
        print("正在打开（初始化）摄像头!")
    else:
        while imgname < mergeNum +1:
            ret, frame = cap.read()
            if not ret:  # 如果没获取了帧图像就退出
                print("帧无法获取（the end of video stream ），正在退出")
                break
            else:
                #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 获取灰度图像——cvtColor颜色控制，返回一个图像
                cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
                cv2.imshow('frame', frame)
                if(n % timeF == 0): #每隔timeF帧进行存储操作
                    cv2.imwrite('./RsOutput/IMG/'+ str(imgname) + '.jpg',frame) #存储为图像
                    imgname = imgname + 1
                    if(imgname > mergeNum):
                        img6 = cv2.imread('./RsOutput/IMG/'+ str(imgname-6) + '.jpg')
                        img5 = cv2.imread('./RsOutput/IMG/'+ str(imgname-5) + '.jpg')
                        img4 = cv2.imread('./RsOutput/IMG/'+ str(imgname-4) + '.jpg')
                        img3 = cv2.imread('./RsOutput/IMG/'+ str(imgname-3) + '.jpg')
                        img2 = cv2.imread('./RsOutput/IMG/'+ str(imgname-2) + '.jpg')
                        img1 = cv2.imread('./RsOutput/IMG/'+ str(imgname-1) + '.jpg')

                        sum_rows = 4320
                        sum_cols = 1280
                        final_matrix = np.zeros((sum_rows, sum_cols, 3), np.uint8)
                        final_matrix[0              :sum_rows//6    , 0:sum_cols] = img1
                        final_matrix[sum_rows//6    :(sum_rows//6)*2, 0:sum_cols] = img2
                        final_matrix[(sum_rows//6)*2:(sum_rows//6)*3, 0:sum_cols] = img3
                        final_matrix[(sum_rows//6)*3:(sum_rows//6)*4, 0:sum_cols] = img4
                        final_matrix[(sum_rows//6)*4:(sum_rows//6)*5, 0:sum_cols] = img5
                        final_matrix[(sum_rows//6)*5:sum_rows       , 0:sum_cols] = img6

                        #cv2.imwrite('./RsOutput/IMGFIN/'+ str(imgfinname) + '.jpg',final_matrix) #存储为图像
                        imgfinname = imgfinname + 1
                        cr_otsu(final_matrix) #肤色识别 灰度处理

                        cv2.namedWindow('status', cv2.WINDOW_FREERATIO)
                        cv2.imshow('status', final_matrix)

                        #删除文件
                        path = './RsOutput/IMG/'+ str(imgname-6) + '.jpg'  # 文件路径
                        if os.path.exists(path):  # 如果文件存在
                            # 删除文件，可使用以下两种方法。
                            os.remove(path)
                            #os.unlink(path)
                        else:
                            print('no such file:'+path)  # 则返回文件不存在

                n = n + 1
                if cv2.waitKey(1) & 0xFF == ord('Q') :  # 如果检测到Q按键，quit中断视频获取
                    #删除文件
                    path = './RsOutput/IMG'  # 文件路径
                    if os.path.exists(path):  # 如果文件存在
                        del_file(path)
                    break
            time.sleep(0.05)
    cap.release()  # 释放捕获
    cv2.destroyAllWindows()  # 摧毁全部窗体


