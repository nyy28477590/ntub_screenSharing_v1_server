from time import  sleep
from  os import startfile
from zlib import  compress
from threading import  Thread
from socket import (socket, AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_BROADCAST)
from tkinter import  Tk, BooleanVar, Button, Label
from PIL.ImageGrab import grab
from PIL import  Image
import pyautogui as pag

root = Tk()
root.title('北商商務系廣播系統|教師端')
root.geometry('640x100+500+200')
root.iconbitmap('./seanleetech.ico')
root.resizable(False, False)

BUFFER_SIZE = 60*1024

sending = BooleanVar(root, value=False)

def send_image():
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
    IP = '255.255.255.255'
    cursor = Image.open('./cursor.png')

    while sending.get():
        x, y = pag.position()
        im = grab()
        im.paste(cursor, box=(x, y), mask=cursor)
        w, h = im.size

        im_bytes = compress(im.tobytes())

        sock.sendto(b'start', (IP, 22222))
        for i in range(len(im_bytes)//BUFFER_SIZE+1):
            start = i * BUFFER_SIZE
            end = start  + BUFFER_SIZE
            sock.sendto(im_bytes[start:end], (IP, 22222))

        sock.sendto(b'_over'+str((w,h)).encode(), (IP, 22222))

        sleep(0.0001)

    sock.sendto(b'close', (IP, 22222))
    sock.close()

def btnStartClick():
    sending.set(True)
    Thread(target=send_image).start()

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
    IP = '255.255.255.255'
    sock.sendto(b'big', (IP, 10000))

    btnStart['state'] = 'disabled'
    btnStop['state'] = 'normal'

btnStart = Button(root, text='開始廣播', command=btnStartClick)
btnStart.place(x=60, y=15, width=250, height=50)

def btnStopClick():
    sending.set(False)

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.setsockopt(SOL_SOCKET, SO_BROADCAST, True)
    IP = '255.255.255.255'
    sock.sendto(b'small', (IP, 10000))

    btnStart['state'] = 'normal'
    btnStop['state'] = 'disable'

btnStop = Button(root, text='停止廣播', command = btnStopClick)
btnStop['state'] = 'disabled'
btnStop.place(x=330, y=15, width=250, height=50)

lbCopyRight = Label(root, text="Power by SeanLeeTech.com", fg='blue', cursor='heart')
lbCopyRight.place(x=5, y=80, width=600, height=20)
url = r'https://www.seanleetech.com'
lbCopyRight.bind("<Button-1>", lambda e: startfile(url))

root.mainloop()


