import re, pafy, threading, os, requests, json
from pydub import AudioSegment
from Tkinter import *

keys = open('key.json', 'r')
API_KEY = json.loads(keys.read())['api_key']
keys.close()

vid_url_list = []
vid_list = []
vid_selection = []

def add_dw():
    try:
        index = cur_titles.curselection()[0]
    except:
        return

    dw_titles.insert(END, vid_list[index].title)
    vid_selection.append(vid_list[index])

def delete_dw():
    if not dw_titles.curselection():
        pass
    else:

        index = dw_titles.curselection()[0]
        dw_titles.delete(index, index)
        vid_selection.pop(index)

        print str(dw_titles.get(0, END))

def add_cur(text):
    cur_titles.insert(END, text)

def clear():
    cur_titles.delete(0, END)
    dw_titles.delete(0, END)
    vid_url_list = []
    vid_list = []
    vid_selection = []

def clear_dw():
    dw_titles.delete(0, END)
    vid_selection = []

def download_async():
    disable_ui()
    threading.Thread(target=download).start()

def download():
    for vid in vid_selection:
        try:
            audio = vid.getbestaudio()
            filename = vid.title + "." + audio.extension
            audio.download(filepath=filename)
            AudioSegment.from_file(filename).export(vid.title + ".mp3", format="mp3")
            os.remove(filename)
        except:
            continue

    enable_ui()

def disable_ui():
    load_button.configure(state='disabled')
    clear_button.configure(state='disabled')
    add_button.configure(state='disabled')
    delete_button.configure(state='disabled')
    download_button.configure(state='disabled')
    clear_button_dw.configure(state='disabled')

def enable_ui():
    load_button.configure(state='normal')
    clear_button.configure(state='normal')
    add_button.configure(state='normal')
    delete_button.configure(state='normal')
    download_button.configure(state='normal')
    clear_button_dw.configure(state='normal')

def load_async():
    disable_ui()
    threading.Thread(target=load).start()

def load():
    try:
        get_urls(playlist_url.get())
    except Exception as e:
        print "Exception: " + str(e)
        clear()
        enable_ui()
        return

    for vid in vid_url_list:
        url = "https://www.youtube.com/watch?v=" + vid
        try:
            video = pafy.new(url)
            vid_list.append(video)
            add_cur(video.title)
        except:
            continue

    enable_ui()

def get_urls(url):
    r = requests.get("https://www.googleapis.com/youtube/v3/playlistItems?playlistId=" + url + "&maxResults=50&part=contentDetails&key=" + API_KEY)
    items = json.loads(r.text)["items"]

    for item in items:
        vid_url_list.append(item["contentDetails"]["videoId"])

def selectall(event=None):
    try:
        event.widget.selection_range(0, END)
    except:
        pass

win = Tk()
win.bind('<Control-a>', selectall)

playlist_url = StringVar()
playlist_url_entry = Entry(win, width=80, textvariable=playlist_url)
playlist_url_entry.event_add('<<Paste>>', '<Control-v>')
playlist_url_entry.event_add('<<Copy>>', '<Control-c>')
playlist_url.set("Playlist ID")
playlist_url_entry.grid(row=0,column=0)

list_frame = Frame(win)

cur_titles = Listbox(list_frame, height=15, width=35)
cur_titles.pack(side=LEFT)
cur_titles_sb = Scrollbar(list_frame ,orient=VERTICAL)
cur_titles_sb.pack(side=LEFT, fill=Y)
cur_titles_sb.configure(command=cur_titles.yview)
cur_titles.configure(yscrollcommand=cur_titles_sb.set)

dw_titles = Listbox(list_frame, height=15, width=35)
dw_titles.pack(side=LEFT)
dw_titles_sb = Scrollbar(list_frame ,orient=VERTICAL)
dw_titles_sb.pack(side=LEFT, fill=Y)
dw_titles_sb.configure(command=dw_titles.yview)
dw_titles.configure(yscrollcommand=dw_titles_sb.set)

list_frame.grid(row=1, column=0)

button_frame = Frame(win)

load_button = Button(button_frame, text="Load",command=load_async)
load_button.grid(row=0,column=0)

clear_button = Button(button_frame, text="Clear All",command=clear)
clear_button.grid(row=0,column=1)

add_button = Button(button_frame, text="Add",command=add_dw)
add_button.grid(row=0,column=2)

delete_button = Button(button_frame, text="Delete",command=delete_dw)
delete_button.grid(row=0,column=3)

clear_button_dw = Button(button_frame, text="Clear Queue",command=clear_dw)
clear_button_dw.grid(row=0,column=4)

download_button = Button(button_frame, text="Download",command=download_async)
download_button.grid(row=0,column=5)

button_frame.grid(row=2, column=0)

win.wm_title("YTPD")
win.resizable(0,0)
win.mainloop()
