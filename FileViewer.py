#FileViewer.py
#This file will allow the user to select
#the audio files to train and test the
#machine learing algorithm in 'ph_ml_algo.py'

from tkinter import *
import glob, math, os, re, sys, subprocess, statistics
from tkinter.scrolledtext import ScrolledText
from tkinter import filedialog
from typing import IO
import librosa


class FileViewer(Frame):

    def __init__(self, master, resultWin):
        Frame.__init__(self, master)
        self.master = master
        self.speechFiles = [] 
        self.musicFiles = []
        self.processedAudioData = []
        self.resultWin = resultWin
        self.nums = re.compile(r'(\d+)')
        self.modelBooleans = []
        self.xmax = 150
        self.ymax = 30

        #Create main frame
        mainFrame = Frame(master)
        mainFrame.pack()

        #Create File List frame
        self.listFrame = Frame(mainFrame)
        self.listFrame.pack(side=TOP)

        #Create Compute frame
        computeFrame = Frame(mainFrame)
        computeFrame.pack(side=BOTTOM)

        #Create Results frame
        resultFrame = Frame(self.resultWin)
        resultFrame.pack(side=TOP)
        self.filelist = Canvas(resultFrame)
        resultsControl = Frame(resultFrame)
        resultsControl.pack(side=BOTTOM)

        #Create Buttons
        fileSelector = Button(self.listFrame, text="Pull Files", fg="black", padx=10, width=10, command=lambda: self.get_audio_files())
        fileSelector.pack(side=BOTTOM)
        compAudio = Button(computeFrame, text="Compute", fg="green", padx=10, width=10, command=lambda: self.comp_audio())
        compAudio.pack(side=BOTTOM)

        l1 = Label(self.listFrame, text='Check the files to \nmake the model with: ', fg='red')
        l1.pack(side=LEFT)

        #Create File Listbox
        self.listScrollbar = Scrollbar(self.listFrame) 
        self.filelist = Canvas(self.listFrame, yscrollcommand=self.listScrollbar.set, height=30, width=60)

    def comp_audio_helper(self, fileListP):
        returnTuples = []
        for i in range(len(fileListP)):
            #check to make sure file's checkbox is checked
            x, sr = librosa.load(fileListP[i])
            zero_crossings = librosa.zero_crossings(x)
            spectral_centroids = librosa.feature.spectral_centroid(x, sr=sr)[0]
            chromagram = librosa.feature.chroma_stft(x, sr=sr)
            if "audio/music/" in fileListP[i]:
                self.processedAudioData.append((fileListP[i], zero_crossings, spectral_centroids, chromagram, "yes"))
            else:
                self.processedAudioData.append((fileListP[i], zero_crossings, spectral_centroids, chromagram, "no"))
        return returnTuples

    def comp_audio(self):
        self.processedAudioData.clear()
        processedMusicFiles = self.comp_audio_helper(self.musicFiles)
        processedSpeechFiles = self.comp_audio_helper(self.speechFiles)
        #print(self.processedAudioData)

    def play_file(self, file):
        print(file)
        if sys.platform == "win32":
            if music_file:
                os.startfile("\\file\\")
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, file])
           

    def fileSort(self, num):
        parts = self.nums.split(num)
        parts[1::2] = map(int, parts[1::2])
        return parts

    def filelist_build_helper(self, fileListP, startPoint):
        for i in range(len(fileListP)):
            self.modelBooleans.append(IntVar(0))
            link = Button(self.filelist, bg = "light green", text='Play')
            handler=lambda f=fileListP[i]: self.play_file(f)
            link.configure(command=handler)
            link.pack(side=LEFT, expand=YES)
            self.filelist.create_window(
                150,
                (i + startPoint) * self.ymax,
                anchor=NW,
                window=link, 
                width=50, 
                height=self.ymax)
            cb = Checkbutton(self.filelist, bg='light blue', text=fileListP[i].replace("audio/", ""), variable=self.modelBooleans[i + startPoint], onvalue=1, offvalue=0)
            cb.pack(side=LEFT, expand=YES)
            self.filelist.create_window(
                0,
                (i + startPoint) * self.ymax,
                anchor=NW,
                window=cb, 
                width=self.xmax, 
                height=self.ymax)
            

    def build_filelist(self):
        filecount = len(self.musicFiles) + len(self.speechFiles)
        fullsize = (0, 0, (self.xmax), (self.ymax * filecount))
        
        # Initialize the canvas with dimensions equal to the number of files
        self.filelist.delete(ALL)
        self.filelist.config( 
            width=self.xmax + 50,
            height=self.ymax * filecount /2,
            yscrollcommand=self.listScrollbar.set,
            scrollregion=fullsize)
        self.filelist.pack(side=LEFT)
        self.listScrollbar.config(command=self.filelist.yview)
        self.listScrollbar.pack(side=LEFT, fill=Y)


        self.filelist_build_helper(self.speechFiles, 0)
        self.filelist_build_helper(self.musicFiles, len(self.speechFiles))
    
    #Grab the audio files from the audio directory in the same space as the FileViewer
    def get_audio_files(self):
        self.filelist.delete("1.0","end")
        self.musicFiles.clear()
        self.speechFiles.clear()
        for infile in sorted(glob.glob('audio/music/*.wav'), key=self.fileSort):
            file, ext = os.path.split(infile)
            self.musicFiles.append('audio/music/' + ext)
        for infile in sorted(glob.glob('audio/speech/*.wav'), key=self.fileSort):
            file, ext = os.path.split(infile)
            self.speechFiles.append('audio/speech/' + ext)
        print(self.musicFiles)
        print(self.speechFiles)
        self.build_filelist()
        return
        

if __name__ == '__main__':
    root = Tk()
    root.title('Audio Analysis Tool')
    
    resultWin = Toplevel(root)
    resultWin.title('Result Viewer')
    resultWin.protocol('WM_DELETE_WINDOW', lambda:None)

    fileViewer = FileViewer(root, resultWin)

    root.mainloop()
