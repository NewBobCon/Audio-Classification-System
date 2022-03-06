#FileViewer.py
#This file will allow the user to select
#the audio files to train and test the
#machine learing algorithm in 'ph_ml_algo.py'

from tkinter import *
#from tkinter import filedialog
import glob, math, os, re
import statistics

class FileViewer(Frame):

    def __init__(self, master, resultWin):
        Frame.__init__(self, master)
        self.master = master
        self.speechFiles = [] 
        self.musicFiles = []
        self.resultWin = resultWin
        self.nums = re.compile(r'(\d+)')

        #Create main frame
        mainFrame = Frame(master)
        mainFrame.pack()

        #Create File List frame
        listFrame = Frame(mainFrame)
        listFrame.pack(side=TOP)

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
        fileSelector = Button(listFrame, text="File Select", fg="black", padx=10, width=10, command=lambda: self.get_audio_files())
        fileSelector.pack(side=TOP)
        compAudio = Button(computeFrame, text="Compute", fg="green", padx=10, width=10, command=lambda: self.comp_audio())
        compAudio.pack(side=BOTTOM)

        #Create File Listbox
        self.listScrollbar = Scrollbar(listFrame)
        self.list = Listbox(listFrame, yscrollcommand=self.listScrollbar.set, selectmode=BROWSE, height=20)

        

    def fileSort(self, num):
        parts = self.nums.split(num)
        parts[1::2] = map(int, parts[1::2])
        return parts
        
    
    def build_listbar(self):
        for i in range(len(self.speechFiles)):
            self.list.insert(i, self.speechFiles[i])
        for j in range(len(self.musicFiles)):
            self.list.insert(j + len(self.speechFiles), self.musicFiles[j])
        self.list.pack(side=LEFT, fill=BOTH)
        self.list.activate(1)
        self.listScrollbar.config(command=self.list.yview)

    def get_audio_files(self):
        for infile in sorted(glob.glob('audio/music/*.wav'), key=self.fileSort):
            file, ext = os.path.split(infile)
            self.musicFiles.append(ext)
        for infile in sorted(glob.glob('audio/speech/*.wav'), key=self.fileSort):
            file, ext = os.path.split(infile)
            self.speechFiles.append(ext)
        print(self.musicFiles)
        print(self.speechFiles)
        self.build_listbar()
        # filetypes = (('audio files', '*.wav'), ('All files', '*.*'))
        # filenames = filedialog.askopenfilenames(title='Open Files', initialdir='/', filetypes=filetypes)
        # print(filenames)
        # showinfo(title='Selected Files', message=filenames)
        return
        

if __name__ == '__main__':
    root = Tk()
    root.title('Audio Analysis Tool')
    
    resultWin = Toplevel(root)
    resultWin.title('Result Viewer')
    resultWin.protocol('WM_DELETE_WINDOW', lambda:None)

    fileViewer = FileViewer(root, resultWin)

    root.mainloop()
