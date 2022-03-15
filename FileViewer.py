#FileViewer.py
#This file will allow the user to select
#the audio files to train and test the
#machine learing algorithm in 'ph_ml_algo.py'

from tkinter import *
import glob, math, os, re, sys, subprocess, statistics
from typing import IO
import librosa
import sklearn
from sklearn.ensemble import RandomForestClassifier
import warnings
warnings.filterwarnings("ignore")

class FileViewer(Frame):

    def __init__(self, master, resultWin):
        Frame.__init__(self, master)
        self.master = master
        self.speechFiles = [] 
        self.musicFiles = []
        self.processedAudioData = []
        self.processedGroundTruths = []
        self.resultWin = resultWin
        self.nums = re.compile(r'(\d+)')
        self.modelBooleans = []
        self.xmax = 150
        self.ymax = 30
        self.clf = RandomForestClassifier(random_state=0)

        #Create main frame
        mainFrame = Frame(master)
        mainFrame.pack()

        #Create Main File List frame
        self.mainListFrame = Frame(mainFrame)
        self.mainListFrame.pack(side=TOP)

        #Create Compute frame
        computeFrame = Frame(mainFrame)
        computeFrame.pack(side=BOTTOM)

        #Create Results frame
        resultFrame = Frame(self.resultWin)
        resultFrame.pack(side=TOP)
        self.outputList = Canvas(resultFrame)
        # resultsControl = Frame(resultFrame)
        # resultsControl.pack(side=BOTTOM)

        #Create Result File List frame
        self.resultListFrame = Frame(resultFrame)
        self.resultListFrame.pack(side=TOP)

        #Create Buttons
        fileSelector = Button(self.mainListFrame, text="Pull Files", fg="black", padx=10, width=10, command=lambda: self.get_audio_files())
        fileSelector.pack(side=BOTTOM)
        compAudio = Button(computeFrame, text="Compute", fg="green", padx=10, width=10, command=lambda: self.comp_audio())
        compAudio.pack(side=BOTTOM)

        l1 = Label(self.mainListFrame, text='Check the files to \nmake the model with: ', fg='red')
        l1.pack(side=TOP)
        self.label = Label(self.mainListFrame, text="Need this many \nmore files for model: 0")
        self.label.pack(side=BOTTOM)

        #Create File Listbox
        self.listScrollbar = Scrollbar(self.mainListFrame) 
        self.filelist = Canvas(self.mainListFrame, yscrollcommand=self.listScrollbar.set, height=30, width=60)

        #Create Results Listbox
        self.resultScrollbar = Scrollbar(self.resultListFrame)
        self.resultList = Canvas(self.resultListFrame, yscrollcommand=self.resultScrollbar.set, height=20, width=60)

    def comp_audio_helper(self, fileListP, startValue):
        for i in range(len(fileListP)):
            #check to make sure file's checkbox is checked
            if self.modelBooleans[i+startValue].get() == 0:
                continue
            x, sr = librosa.load(fileListP[i])
            zero_crossing = librosa.feature.zero_crossing_rate(x).tolist()
            zcstdev = statistics.stdev(zero_crossing[0])
            spectral_centroids = librosa.feature.spectral_centroid(x, sr=sr).tolist()
            sca = statistics.mean(spectral_centroids[0])
            bandwidth = librosa.feature.spectral_bandwidth(x, sr=sr).tolist()
            bwa = statistics.mean(bandwidth[0])
            #chromagram = librosa.feature.chroma_stft(x, sr=sr).tolist()
            #cgstdev = statistics.stdev(chromagram[0])
            print("Model, ", fileListP[i], zcstdev, sca, bwa)
            if "audio/music/" in fileListP[i]:
                self.processedAudioData.append((zcstdev, sca, bwa))
                self.processedGroundTruths.append("MUSIC")
            else:
                self.processedAudioData.append((zcstdev, sca, bwa))
                self.processedGroundTruths.append("SPEECH")

    def comp_audio(self):
        if round((len(self.speechFiles) + len(self.musicFiles)) * (2 / 3) - self.modelBooleansCounter()) != 0:
            return
        self.processedAudioData.clear()
        self.processedGroundTruths.clear()        
        self.comp_audio_helper(self.speechFiles, 0)
        self.comp_audio_helper(self.musicFiles, len(self.speechFiles))
        print(self.processedAudioData[23])
        self.comp_model()
        self.build_results()

        #print(self.processedAudioData)

    def comp_model(self):
        #clf.fit(self.processedAudioData[:,1,2,3], self.processedAudioData[:,4])
        self.clf.fit(self.processedAudioData, self.processedGroundTruths)
                
    def results_helper(self, fileListP, startValue, colStartVal):
        fileListStr = ""
        if fileListP[0] in self.speechFiles:
            fileListStr = "Speech"
        else:
            fileListStr = "Music"
        counter = 0
        for i in range(len(fileListP)):
            if self.modelBooleans[i+startValue].get() == 0:
                link = Button(self.resultList, bg = "light green", text='Play')
                handler=lambda f=fileListP[i]: self.play_file(f)
                link.configure(command=handler)
                link.pack(side=LEFT, expand=YES)
                self.resultList.create_window(
                    450,
                    (counter + colStartVal) * self.ymax, 
                    anchor=NW,
                    window=link, 
                    width=50, 
                    height=self.ymax)
                lb1 = Label(self.resultList, bg='light blue', text=fileListP[i].replace("audio/", ""))
                lb1.pack(side=LEFT, expand=YES)
                self.resultList.create_window(
                    0,
                    (counter + colStartVal) * self.ymax,
                    anchor=NW,
                    window=lb1, 
                    width=self.xmax, 
                    height=self.ymax)
                #Calculate each feature 
                x, sr = librosa.load(fileListP[i])
                zero_crossing = librosa.feature.zero_crossing_rate(x).tolist()
                zcstdev = statistics.stdev(zero_crossing[0])
                spectral_centroids = librosa.feature.spectral_centroid(x, sr=sr).tolist()
                sca = statistics.mean(spectral_centroids[0])
                bandwidth = librosa.feature.spectral_bandwidth(x, sr=sr).tolist()
                bwa = statistics.mean(bandwidth[0])
                #chromagram = librosa.feature.chroma_stft(x, sr=sr).tolist()
                #cgstdev = statistics.stdev(chromagram[0])
                prediction = self.clf.predict([(zcstdev, sca, bwa)]).reshape(1, -1)
                lb2 = Label(self.resultList, bg='light yellow', text="Prediction: " + str(prediction[0][0]))
                lb2.pack(side=LEFT, expand=YES)
                self.resultList.create_window(
                    150,
                    (counter + colStartVal) * self.ymax,
                    anchor=NW,
                    window=lb2, 
                    width=self.xmax, 
                    height=self.ymax)
                lb3 = Label(self.resultList, bg='honeydew2', text="Truth: " + fileListStr)
                lb3.pack(side=LEFT, expand=YES)
                self.resultList.create_window(
                    300,
                    (counter + colStartVal) * self.ymax,
                    anchor=NW,
                    window=lb3, 
                    width=self.xmax, 
                    height=self.ymax)
                counter += 1

    def build_results(self):
        filecount = len(self.speechFiles) + len(self.musicFiles) - round(((len(self.speechFiles) + len(self.musicFiles)) * (2 / 3)))
        fullsize = (0, 0, (self.xmax), (self.ymax * filecount))

        self.resultList.delete(ALL)
        self.resultList.config( 
            width=self.xmax + 350,
            height=self.ymax * 10,
            yscrollcommand=self.resultScrollbar.set,
            scrollregion=fullsize)
        self.resultList.pack(side=LEFT)
        self.resultScrollbar.config(command=self.resultList.yview)
        self.resultScrollbar.pack(side=LEFT, fill=Y)

        unselected_speech_files = 0
        for i in range(len(self.speechFiles)):
            if self.modelBooleans[i].get() == 0:
                unselected_speech_files += 1
        self.results_helper(self.speechFiles, 0, 0)
        self.results_helper(self.musicFiles, len(self.speechFiles), unselected_speech_files)

    def play_file(self, file):
        if sys.platform == "win32":
            if music_file:
                os.startfile("\\file\\")
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, file])
    
    def modelBooleansCounter(self):
        count = 0
        for check in self.modelBooleans:
            if check.get() == 1:
                count += 1
        return count

    def modelPercentage(self):
        count = self.modelBooleansCounter()
        boundary = round(((len(self.speechFiles) + len(self.musicFiles)) * (2 / 3))) - count
        if boundary == 0:
            self.label.configure(text="Ready!\n")
        elif boundary > 0:
            self.label.configure(text="Need this many \nmore files for model: " + str(round(boundary)))
        elif boundary < 0:
            self.label.configure(text="Unselect this many files: " + str(abs(round(boundary))) + "\n")
        return

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
            cb = Checkbutton(self.filelist, bg='light blue', text=fileListP[i].replace("audio/", ""), variable=self.modelBooleans[i + startPoint], onvalue=1, offvalue=0, command=lambda: self.modelPercentage())
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
            height=self.ymax * 20,
            yscrollcommand=self.listScrollbar.set,
            scrollregion=fullsize)
        self.filelist.pack(side=LEFT)
        self.listScrollbar.config(command=self.filelist.yview)
        self.listScrollbar.pack(side=LEFT, fill=Y)


        self.filelist_build_helper(self.speechFiles, 0)
        self.filelist_build_helper(self.musicFiles, len(self.speechFiles))
        self.label.configure(text="Need this many \nmore files for model: " + str(round((len(self.speechFiles) + len(self.musicFiles)) * (2 / 3))))
    
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
        # print(self.musicFiles)
        # print(self.speechFiles)
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
