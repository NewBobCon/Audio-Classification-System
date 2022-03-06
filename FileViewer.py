#FileViewer.py
#This file will allow the user to select
#the audio files to train and test the
#machine learing algorithm in 'ph_ml_algo.py'

from tkinter import *
import glob, math, os, re
import statistics
from tkinter.scrolledtext import ScrolledText

class FileViewer(Frame):

    def __init__(self, master, resultWin):
        Frame.__init__(self, master)
        self.master = master
        self.speechFiles = [] 
        self.musicFiles = []
        self.resultWin = resultWin
        self.nums = re.compile(r'(\d+)')
        self.modelBooleans = []

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
        self.canvas = Canvas(resultFrame)
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
        #self.filelist = Listbox(self.listFrame, yscrollcommand=self.listScrollbar.set, selectmode=BROWSE, height=20, width=40)
        self.filelist = ScrolledText(self.listFrame, height=20, width=40)
        self.filelist.pack(side=LEFT)
        
    def fileSort(self, num):
        parts = self.nums.split(num)
        parts[1::2] = map(int, parts[1::2])
        return parts

    def listbar_helper(self, fileListP, startPoint):
        for i in range(len(fileListP)):
            self.modelBooleans.append(IntVar(0))
            cb = Checkbutton(self.filelist, text=fileListP[i], variable=self.modelBooleans[i + startPoint], onvalue=1, offvalue=0)
            self.filelist.window_create('end', window=cb)
            self.filelist.insert('end', '\n')

    def build_listbar(self):
        self.listbar_helper(self.speechFiles, 0)
        self.listbar_helper(self.musicFiles, len(self.speechFiles))
        # for i in range(len(self.speechFiles)):
        #     #self.filelist.insert(i, self.speechFiles[i])
        #     self.modelBooleans.append(IntVar(0))
        #     cb = Checkbutton(self.filelist, text=self.speechFiles[i], variable=self.modelBooleans[i], onvalue=1, offvalue=0)
        #     self.filelist.window_create('end', window=cb)
        #     self.filelist.insert('end', '\n')
        # for j in range(len(self.musicFiles)):
        #     #self.filelist.insert(j + len(self.speechFiles), self.musicFiles[j])
        #     cb = Checkbutton(self.filelist, text=self.musicFiles[j], variable=self.modelBooleans[j], onvalue=1, offvalue=0)
        #     self.filelist.window_create('end', window=cb)
        #     self.filelist.insert('end', '\n')
        self.filelist.pack(side=LEFT, fill=BOTH)
        self.listScrollbar.config(command=self.filelist.yview)

    def get_audio_files(self):
        self.filelist.delete("1.0","end")
        self.musicFiles.clear()
        self.speechFiles.clear()
        for infile in sorted(glob.glob('audio/music/*.wav'), key=self.fileSort):
            file, ext = os.path.split(infile)
            self.musicFiles.append(ext)
        for infile in sorted(glob.glob('audio/speech/*.wav'), key=self.fileSort):
            file, ext = os.path.split(infile)
            self.speechFiles.append(ext)
        print(self.musicFiles)
        print(self.speechFiles)
        self.build_listbar()
        return
        

if __name__ == '__main__':
    root = Tk()
    root.title('Audio Analysis Tool')
    
    resultWin = Toplevel(root)
    resultWin.title('Result Viewer')
    resultWin.protocol('WM_DELETE_WINDOW', lambda:None)

    fileViewer = FileViewer(root, resultWin)

    root.mainloop()
