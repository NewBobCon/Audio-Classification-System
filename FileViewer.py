#FileViewer.py
#This file will allow the user to select
#the audio files to train and test the
#machine learing algorithm in 'ph_ml_algo.py'

from tkinter import *

class FileViewer(Frame):

    def __init__(self, master, resultWin):
        Frame.__init__(self, master)
        self.master = master
        self.resultWin = resultWin

        #Create main frame
        mainFrame = Frame(master)
        mainFrame.pack()

        #Create List frame
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
        self.listScrollbar.pack(side=RIGHT, fill=Y)
        self.list = Listbox(listFrame, yscrollcommand=self.listScrollbar.set, selectmode=BROWSE, height=20)
        

if __name__ == '__main__':
    root = Tk()
    root.title('Audio Analysis Tool')
    
    resultWin = Toplevel(root)
    resultWin.title('Result Viewer')
    resultWin.protocol('WM_DELETE_WINDOW', lambda:None)

    fileViewer = FileViewer(root, resultWin)

    root.mainloop()
