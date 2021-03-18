#import necessary packages
from tkinter import *
import pathlib
from tkinter.ttk import Progressbar
from pytube import YouTube
from PIL import Image,ImageTk
import os
import requests
import re
from tkinter import messagebox, filedialog
import threading


# Defining CreateWidgets() function
# to create necessary tkinter widgets
def Widgets():
    url= Label(root, text="YouTube link :", bg="red",fg="white" )
    url.place(x=50,y=60,height=30)

    linkTxt = Entry(root,textvariable=video_Link)
    linkTxt.place(x=160,y=60,height=30,width=250)

    destination_lbl=Label(root, text="Destination :", bg="red",fg="white")
    destination_lbl.place(x=50,y=100,height=30)

    destination_Txt=Entry(root, textvariable=download_Path)
    destination_Txt.place(x=160,y=100,height=30,width=200)

    browse_Btn=Button(root, text="Browse", command=Browse, bg="blue",fg="white")
    browse_Btn.place(x=370,y=105)

    Download_Btn=Button(root, text="Download", command=Download,bg="green",fg="white",activebackground="orange")
    Download_Btn.place(x=180,y=180,height=35,width=80)

    cancel_btn=Button(root,text="cancel",command=quit,bg="grey",fg="white",activebackground="purple")
    cancel_btn.place(x=300,y=180,height=35,width=100)

    progress_bar = Progressbar(root, orient=HORIZONTAL, length=590, mode='determinate')
    progress_bar.place(x=40, y=250, height=25, width=400)
    label=Label(root,text="Status",bg="brown",fg="white").place(x=200,y=280)



# Defining Browse() to select a
# destination folder to save the video
def Browse():
    #download_Directory = filedialog.askdirectory(initialdir=pathlib.Path.cwd())
    download_Directory1=filedialog.asksaveasfilename(initialdir=pathlib.Path.cwd())
    # Displaying the directory in the directory
    # textbox
    #download_Path.set(download_Directory)
    download_Path.set(download_Directory1)

def getStandardSize(size):
    itme=['bytes','KB','MB','GB','TB']
    for x in itme:
        if size < 1024.0:
            return  "%3.1f %s" % (size,x)
        size/=1024.0
    return size


# Defining Download() to download the video
def Download():
    # getting user-input Youtube Link
    url= video_Link.get()
   # downloadThread = threading.Thread(target=lambda: addDownloadItem(url))
    #downloadThread.start()

    # select the optimal location for
    # saving file's
    download_Folder = download_Path.get()
    # Creating object of YouTube()
    getVideo = YouTube(url)
    # Getting all the available streams of the
    # youtube video and selecting the first
    # from the
    videoStream = getVideo.streams.first()
    # Downloading the video to destination
    # directory
    videoStream.download(download_Folder)

    # Displaying the message
    messagebox.showinfo("SUCCESSFULLY", "DOWNLOADED AND SAVED IN\n"
                        + download_Folder)


def addDownloadItem(url):

    if url!=None:
        req=requests.get(url,stream=True)

        if "Content-Length" in req.headers:
            total_size=req.headers['Content-Length']
        else:
            total_size=None



        if "Content-Disposition" in req.headers.keys():
            fname=re.findall("filename=(.+)",req.headers["Content-Disposition"])[0]
        else:
            fname=url.split("/")[-1]



        progress=Progressbar(root)
        progress['value']=0
        progress.place(x=10,column=100,sticky="nsew",mode="intermediate")

        labelPercentage=Label(root,text="0 %",padx="5",anchor="w",bg="#E67E22",fg="white")
        labelPercentage.grid(row=0,column=2)
        labelsize=Label(root,text="0 KB",padx="5",anchor="w",bg="#E67E22",fg="white")
        labelsize.grid(row=1,column=2)


        with open(fname,"wb") as obj:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    obj.write(chunk)
                    current_size=os.path.getsize(fname)
                    labelsize.config(text=str(getStandardSize(current_size)))



                    if total_size!=None:
                        percentge=round((int(current_size)/int(total_size))*100)
                        labelPercentage.config(text=str(percentge)+" %")
                        progress['value']=percentge
                    else:
                        percentge="Infinte"
                        progress.config(mode="indeterminate")
                        progress.start()
                        labelPercentage.config(text=str(percentge)+" %")




        if total_size!=None:
            current_size=os.path.getsize(fname)
            labelsize.config(text=str(getStandardSize(current_size)))
            labelPercentage.config(text=str(percentge) + " %")
            percentge=round((int(current_size)/int(total_size))*100)
            progress['value']=percentge
        else:
            current_size=os.path.getsize(fname)
            labelsize.config(text=str(getStandardSize(current_size)))
            labelPercentage.config(text="100 %")
            progress['value'] = 100


# Creating object of tk class
root = Tk()
icon=PhotoImage(file="icon1.png")
root.iconphoto(False,icon)
root.geometry("500x400")
root.resizable(False,False)
root.title("YouTube Video Downloader")
root.config(background="black")
label1=Label(root,text="Video Downloader",font="Dosis,10,Bold",bg="red",fg="white",width=40,borderwidth=10).place(x=50,y=10,height=40)

# Creating the tkinter Variables
video_Link = StringVar()
download_Path = StringVar()
# Calling the Widgets() function
Widgets()
root.mainloop()