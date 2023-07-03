import tkinter
import pygetwindow
import requests
import os
from bs4 import BeautifulSoup
from tkinter import messagebox

def movehere():
    if mylist.get(tkinter.ANCHOR) != "":
        selected = pygetwindow.getWindowsWithTitle(mylist.get(tkinter.ANCHOR))[0]
        selected.moveTo(0, 0)

def refresh():
    window_titles = getwindowtitles()

    mylist.delete(0, tkinter.END)
    for title in window_titles:
        mylist.insert(tkinter.END, title)

def getwindowtitles():
    window_titles = pygetwindow.getAllTitles()

    new_titles = []
    for title in window_titles:
        if title != "":
            new_titles.append(title)

    return new_titles

def uponexit():
    current_window = pygetwindow.getActiveWindow()
    current_window.moveTo(0, 0)
    window.destroy()

def extractversion(title: str):
    first = title.find('(')
    second = title.find(')')
    return title[first + 1:second]

def continuewiththisversion():
    answer = messagebox.askyesno("Warning: old version detected", "You are using old version of Window Mover. Do you want to get newest version?")
    if answer:
        getnewestversion()
        messagebox.showinfo("Success", "Program has been updated!")
        window.destroy()

def getnewestversion():
    FILE_URL = "https://raw.githubusercontent.com/Zhustas/Window-Mover/main/src/main.py"
    FILE_NAME = os.path.basename(__file__)

    req = requests.get(FILE_URL)
    soup = BeautifulSoup(req.content, 'html.parser')

    f = open(FILE_NAME, "w")
    f.write(soup.prettify())


VERSION = "Version 1"
REMOTE_REPOSITORY_URL = "https://github.com/Zhustas/Window-Mover"

req = requests.get(REMOTE_REPOSITORY_URL)

soup = BeautifulSoup(req.content, 'html.parser')
title = soup.title.text
latest_version = extractversion(title)

version_warning = False
if VERSION != latest_version:
    version_warning = True


window = tkinter.Tk()
window.title("Window Mover (Made by Justas)") # Window's title
window.geometry("700x600") # Window's width and height
window.configure(bg="#28ed91") # Window's background color
window.resizable(False, False) # Window is not resizable by width and height

window_titles = getwindowtitles()

mylist = tkinter.Listbox(window, bg="#6cf3f5", bd=3, height=34, width=80, cursor="hand2")
for title in window_titles:
    mylist.insert(tkinter.END, title)
mylist.place(x=20, y=20)

button = tkinter.Button(window, command=movehere, text="Move", bg="#15ad66", cursor="hand2")
button.place(x=590, y=30)

refresh = tkinter.Button(window, command=refresh, text="Refresh", bg="#15ad66", cursor="hand2")
refresh.place(x=585, y=80)

if version_warning:
    window.after(500, continuewiththisversion)

window.protocol("WM_DELETE_WINDOW", uponexit)
window.mainloop()
