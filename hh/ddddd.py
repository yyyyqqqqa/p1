# -*- coding: UTF-8 -*-
from tkinter import *
import tkinter.filedialog
import requests


def Upload():
    print('upload')
    selectFileName = tkinter.filedialog.askopenfilename(title='选择文件')  # 选择文件

    r = requests.post('http://127.0.0.1:8000/upload', files={'file': open(selectFileName, 'rb')})
    print(r.content.decode('utf-8'))
    setText = r.content.decode('utf-8')
    print(setText.__class__)
    e1.delete(0, END)
    e1.insert(0, setText)


def Download():
    link = e1.get()
    files = requests.get(link)
    files.raise_for_status()
    path = tkinter.filedialog.asksaveasfilename()
    print(files.content)
    with open(path, 'wb') as f:
        f.write(files.content)


root = Tk()
root.title('Download')
root.geometry('+500+300')

e1 = Entry(root, width=50)
e1.grid(row=0, column=0)

btn1 = Button(root, text=' 上传 ', command=Upload).grid(row=1, column=0, pady=5)
btn2 = Button(root, text=' 下载 ', command=Download).grid(row=2, column=0, pady=5)
btn3 = Button(root, text=' 复制 ', ).grid(row=3, column=0, pady=5)

mainloop()