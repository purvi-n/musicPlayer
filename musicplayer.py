import os
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog
import pygame
from mutagen.mp3 import MP3
import time
from ttkthemes import themed_tk as tk
from tkinter import ttk

pygame.mixer.init()

root = tk.ThemedTk()
root.set_theme("breeze")

root.geometry('600x300')
root.title("Music Player")
root.iconbitmap('icon.ico')

listframe = Frame(root)
listframe.pack(side=LEFT, padx=30)

buttonframe = Frame(root)
buttonframe.pack(side=RIGHT, padx=15, pady=10)

songs = []
filepath = ''					#path of song

index = 0
playing = False
replay = False

lengthlabel = Label(buttonframe, text='Length: --:--')
lengthlabel.grid(row=2, column=0, pady=15)

namelabel = Label(buttonframe, text='')
namelabel.grid(row=3, column=0, pady=15)

def play():
	try:
		global filepath
		global file
		playing = True
		toPlay = listbox.curselection()
		toPlay = int(toPlay[0])
		playSong = songs[toPlay]
		pygame.mixer.music.load(playSong)
		pygame.mixer.music.play()
	except:
		playing = False
		tkinter.messagebox.showerror('File not found', 'Please select a song')
		print("Error")
	showDetails()
	namelabel['text'] = os.path.basename(filepath)


def stop():
	global playing
	playing = False
	pygame.mixer.music.stop()

def pause():
	global playing
	if(playing):
		pygame.mixer.music.pause()
		playing=False
	else:
		pygame.mixer.music.unpause()
		playing=True
	showDetails()

def rewind():
	global replay
	if(replay==False):
		replay = True
		pygame.mixer.music.play(-1)
	else:
		pygame.mixer.music.play()

def setVol(val):
	volume = int(val)/100
	pygame.mixer.music.set_volume(volume)

def showDetails():
	global filepath
	file_data = os.path.splitext(filepath)

	if file_data[1] == '.mp3':
		audio = MP3(filepath)
		total_length = audio.info.length
	else:
		a = pygame.mixer.Sound(filepath)
		total_length = a.get_length()

	mins, secs = divmod(total_length, 60)
	mins = round(mins)
	secs = round(secs)
	timeformat = '{:02d}:{:02d}'.format(mins, secs)
	lengthlabel['text'] = "Length" + ': ' + timeformat

def aboutUs():
	tkinter.messagebox.showinfo('About this Music Player', 
		'This is a music player build using Python tkinter, pygame and mutagen')

def browseFile():
	global filepath
	filepath = filedialog.askopenfilename()
	add(filepath)

def add(file):
	file = os.path.basename(file)
	index = 0
	listbox.insert(index, file)
	songs.insert(index, filepath)
	index += 1

def delFromPlaylist():
    toDel = listbox.curselection()
    toDel = int(toDel[0])
    listbox.delete(toDel)
    songs.pop(toDel)

def onClosing():
	stop()
	root.destroy()

menubar = Menu(root)
root.config(menu=menubar)

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browseFile)
subMenu.add_command(label="Exit", command=root.destroy)

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=aboutUs)

listbox = Listbox(listframe)
listbox.grid()

addPhoto = PhotoImage(file='plus.png')
addBtn = Button(listframe, image=addPhoto, command=browseFile, bd=0)
addBtn.grid(padx = 10, pady = 10)

delPhoto = PhotoImage(file='delete.png')
delBtn = Button(listframe, image=delPhoto, command=delFromPlaylist, bd=0)
delBtn.grid(padx = 10, pady = 10)

playPhoto = PhotoImage(file='play.png')
playBtn = Button(buttonframe, image=playPhoto, command=play, bd=0)
playBtn.grid(row=1, column=1, padx=5)

stopPhoto = PhotoImage(file='stop.png')
stopBtn = Button(buttonframe, image=stopPhoto, command=stop, bd=0)
stopBtn.grid(row=1, column=2, padx=5)

pausePhoto = PhotoImage(file='pause.png')
pauseBtn = Button(buttonframe, image=pausePhoto, command=pause, bd=0)
pauseBtn.grid(row=1, column=3, padx=5)

rewindPhoto = PhotoImage(file='rewind.png')
rewindBtn = Button(buttonframe, image=rewindPhoto, command=rewind, bd=0)
rewindBtn.grid(row=2, column=2, padx=5, pady=10)

vol_scale = Scale(buttonframe, from_=0, to=100, orient=HORIZONTAL, command=setVol, bd=0)
vol_scale.set(50)
pygame.mixer.music.set_volume(50)
vol_scale.grid(row=3, column=2, padx=5)


root.protocol("WM_DELETE_WINDOW", onClosing)
root.mainloop()
