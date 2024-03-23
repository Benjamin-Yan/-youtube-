# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 17:03:17 2022
Youtube影片用BeautifulSoup的select, find_all等選取id或class會回傳Null，
所以得利用"正規表示式"擷取文字的方式才行
"""
import requests
import re
import os
import time
from pytube import YouTube
from moviepy.editor import *
from tkinter import *

'''常數'''
icon_path = 'C:\\Users\\acer\\Desktop\\python\\轉檔\\hololive.ico'
path = 'C:\\Users\\acer\\Desktop\\temp'

'''下載函式'''
def check_path():
    if not os.path.isdir(path):
        os.mkdir(path) #若無該目錄下的某資料夾，則新增一個

def download_by_playlist(url):  #傳入清單網址
    if len(url) == 0:  #什麼都沒輸入
        messagebox.showwarning("輸入錯誤", "請輸入網址!")
    elif url.isspace():  #輸入全為空白
        messagebox.showwarning("輸入錯誤", "請勿輸入空白!")
    elif len(url) != 72:
        messagebox.showwarning("輸入錯誤", "請勿輸入非播放清單之網址!")
    else:
        El1.delete(0,END)
        Ll3.config(text='')
        '''抓影片們的網址'''
        
        vid_urls = []
        
        html = requests.get(url)
        resl = re.findall(r'/watch[\w+&@#/%?=~|!:,.;-]+[\w+&@#/%=~|]', html.text)#多了-才會全抓到
        
        for i in resl:
            if (i not in vid_urls) and (i != '/watch_page/send') \
                and (len(i) == 20):  #刪除重複網址
                vid_urls.append(i)
        
        temp = '共有 ' + str(len(vid_urls)) + ' 首\n' + '開始下載'
        Ll3.config(text=temp, font=("Meiryo",24,"bold"))
        
        '''影片們下載'''
        if len(vid_urls) == 0:
            messagebox.showwarning("輸入網址產生問題", "There's no data\nto download!")
        else:
            n = 1
            for video in vid_urls:
                yt = YouTube('https://www.youtube.com' + video)
                temp = str(n) + '. ' + yt.title
                print(temp)
                time.sleep(3)
                root.update()
                Ll3.config(text=temp, font=("Meiryo",8,"bold"))
                
                yt.streams.filter(subtype='mp4').first().download(path, filename = "temp.mp4")
                
                origin_path = os.getcwd()
                os.chdir(path)  #可以改變當前程序的工作路徑
                
                videoclip = VideoFileClip("temp.mp4")
                audioclip = videoclip.audio
                audioclip.write_audiofile(temp + '.mp3')#若有bug就改成[str(n)+'.mp3']就好
                os.chdir(origin_path)
                n += 1
            Ll3.config(text='Download Completed', font=("Blackadder ITC",36,"bold"))
    El1.delete(0,END)

def download_by_list():
    for video, i in zip(down_list, range(1, len(down_list) + 1)):
        yt = YouTube(video)
        tem = str(i) + '. ' + yt.title
        print(tem)
        yt.streams.filter(subtype='mp4').first().download(path, filename = "temp.mp4")
        
        origin_path = os.getcwd()
        os.chdir(path)  #可以改變當前程序的工作路徑
        
        videoclip = VideoFileClip("temp.mp4")
        audioclip = videoclip.audio
        audioclip.write_audiofile(tem + '.mp3')
        os.chdir(origin_path)

'''其他函式'''
#1.印出清單
down_list = list()
def print_list():
    cont = Er1.get()
    Er1.delete(0,END)
    if len(cont) == 0:  #什麼都沒輸入
        messagebox.showwarning("輸入錯誤", "請輸入網址!")
    elif cont.isspace():  #輸入全為空白
        messagebox.showwarning("輸入錯誤", "請勿輸入空白!")
    else:
        down_list.append(cont)
        content = '列表內容如如下:\n'
        for i in down_list:
            content += i + '\n'
        Lr3.config(text=content)

#2.清除清單
def reset():
    Er1.delete(0,END)
    Lr3.config(text = "")
    down_list.clear()

#3.下載
def download(typ):
    if len(down_list) == 0:
        messagebox.showwarning("錯誤!", "請先輸入網址到列表!")
    else:
        Er1.delete(0,END)
        Lr4.config(text='')
        check_path()
        if typ == 'mp3':
            download_by_list()
            Lr4.config(text='Download Completed')
            f3.destroy()
            reset()
        else:
            for i in down_list:
                yt = YouTube(i)
                yt.streams.filter(subtype='mp4').first().download(path)
            Lr4.config(text='Download Completed')
            f3.destroy()
            reset()

#詢問下載種類
def down_type():
    global f3
    f3 = Toplevel(root)
    f3.title('下載種類')
    f3.configure(bg="#7AFEC6")
    f3.geometry('250x100')
    f3.iconbitmap(icon_path)
    Label(f3, text='請選擇下載種類', bg="#7AFEC6",font=("Meiryo",18,"bold")).pack()
    Button(f3, text='MP3',fg='blue', bg='pink',width = 4,command=lambda: download('mp3'),
           font=("Viner Hand ITC",10,"bold")).place(x=60, y=50)
    Label(f3, text='或', font=(1), bg="#7AFEC6").place(x=115,y=50)
    Button(f3, text='MP4',fg='blue', bg='pink',width = 4,command=lambda: download('mp4'),
           font=("Viner Hand ITC",10,"bold")).place(x=150, y=50)
    x = root.winfo_x()
    y = root.winfo_y()
    f3.geometry("+%d+%d" %(x+480,y+250))  #置中顯示

def bind_l(event):
    Ll1.config(text='作者: 太陽餅')

def bind_l1(event):
    Ll1.config(text='By 播放清單')

def bind_r(event):
    Lr1.config(text='日期\n2022.1.25')

def bind_r1(event):
    Lr1.config(text='By 批量新增')

'''主畫面'''
root = Tk()
root.title('Install MP3 & MP4')
root.configure(bg="#7AFEC6")
root.iconbitmap(icon_path) # 更改左上角的icon圖示
#root.iconphoto(True, tk.PhotoImage(file=path)) #png可以，但jpg不行
root.geometry('1200x600')

f1 = Frame(root, bg='gold',highlightthickness=2) #邊框寬度2
f2 = Frame(root, bg='green',highlightthickness=2)

f1.grid(row=0,column=0,sticky="WESN")
f2.grid(row=0,column=1,sticky="WESN")

f1.columnconfigure(0, weight=1)
f2.columnconfigure(0, weight=1)

'''LEFT'''#清單下載
Ll1 = Label(f1,text='By 播放清單',bg='gold',fg="#8B008B", font=("Algerian",48,"bold"))
Ll2 = Label(f1,text='Playlist',bg='gold',fg="#6495ED", font=("Viner Hand ITC",24,"bold"))
El1 = Entry(f1, width = 73, bg='#FEDFE1',fg="#8B008B")
Bl1 = Button(f1, text='Download all MP3s', fg='blue', bg='pink', pady=1, width = 25,
             font=("Viner Hand ITC",14,"bold"),
             command=lambda: download_by_playlist(El1.get()))
Ll3 = Label(f1,text='',bg='gold',fg="#FB9966", font=("Blackadder ITC",36,"bold"))

Ll1.grid(row=0,column=0,padx=6,pady=6)
Ll2.grid(row=1,column=0,padx=6,pady=6)
El1.grid(row=2,column=0,padx=6,pady=6)
Bl1.grid(row=3,column=0,padx=6,pady=6)
Ll3.grid(row=4,column=0,padx=6,pady=25)

Ll1.bind("<Enter>", bind_l)    # 滑鼠進入小部件事件
Ll1.bind("<Leave>", bind_l1)  # 滑鼠離開小部件事件

'''RIGHT'''#1.印出清單2.清除清單3.下載
Lr1 = Label(f2,text='By 批量新增',bg='green',fg="#DAA520", font=("Algerian",48,"bold"))
Lr2 = Label(f2,text='請輸入欲存到下載清單的網址',bg='green',fg="#AFEEEE",
            font=("Meiryo",24,"bold"))
Er1 = Entry(f2, width = 50, bg='#668c1c',fg="#d9ceba")
Br1 = Button(f2,text='加到列表', fg='#6A4C9C', bg='#90B44B',pady=1, width = 10,
            font=("Meiryo",14,"bold"), activebackground='#B5CAA0', command = print_list)
Lr3 = Label(f2,text='',bg='green',fg="#B28FCE", font=("Meiryo",8,"bold"))
Br2 = Button(f2,text='清除列表', fg='#6A4C9C', bg='#90B44B',pady=1, width = 10,
            font=("Meiryo",14,"bold"), activebackground='#B5CAA0', command = reset)
Br3 = Button(f2,text='Download all MP3s', fg='#6A4C9C', bg='#90B44B',pady=1, width = 20,
            font=("Viner Hand ITC",14,"bold"), activebackground='#B5CAA0',command=down_type)
Lr4 = Label(f2,text='',bg='green',fg="#AFEEEE", font=("Blackadder ITC",36,"bold"))

Lr1.grid(row=0,column=0,padx=6,pady=6)
Lr2.grid(row=1,column=0,padx=6,pady=6)
Er1.grid(row=2,column=0,padx=6,pady=6)
Br1.grid(row=3,column=0,padx=6,pady=6)
Lr3.grid(row=4,column=0,padx=6,pady=6)
Br2.grid(row=5,column=0,padx=6,pady=6)
Br3.grid(row=6,column=0,padx=6,pady=6)
Lr4.grid(row=7,column=0,padx=6,pady=6)

Lr1.bind("<Enter>", bind_r)
Lr1.bind("<Leave>", bind_r1)

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

root.mainloop()


'''
for tem_url in resl:
    if 'list=' and 'index=' in tem_url:  #必須包含list=和index=
        vid_urls.append(tem_url)
print(vid_urls)
'''
