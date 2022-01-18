import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import sys
import json
from gpxmove import subGpx
import configparser

class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
    #Loading config and settings files
        #json - replace with configparser
        with open(os.path.join(sys.path[0],"key.json"),"r",encoding="UTF-8") as keyfile:
            key_raw = keyfile.read() 
        apiKey_raw = json.loads(key_raw)
        apiKey =apiKey_raw["key"]
        config = configparser.ConfigParser()
        config.read('settings.ini')
        #print("this is a testc>>"+str(config['sectiones']['Port']))
        default_values = config['defaultvalues']
        default_input = default_values["defaultinputfolder"]
        default_output = default_values["defaultoutputfolder"]
        default_orig = default_values["defaultorigfolder"]
        default_manual = default_values["defaultmanualfolder"]
        default_format = default_values["defaultformat"]
        default_empty = default_values["defaultempty"]

    
        
    
    #functions
        #GPG function and two start functions - Tkinter button called, check directory function
        def CheckDir(path):
            if os.path.isdir(path) == True:
                return True
            else:
                return False
        global y
        y = 0
        
        def startGpx(inp,outp,orig,manual,form,emp):
            if (len(os.listdir(inp))):
                countGpxInt = len(os.listdir(inp))
            else:
                countGpxInt = 1
            self.pb["value"] = 100-((len(os.listdir(inp))/countGpxInt)*100)
            self.leftGpx.set("Gpx zbývá: " + str(len(os.listdir(inp))))
            root.update_idletasks()
            root.update()
            while len(os.listdir(inp)) > 0:
                if (len(os.listdir(inp))):
                    countGpxInt = len(os.listdir(inp))
                else:
                    countGpxInt = 1
                self.pb["value"] = 100-((len(os.listdir(inp))/countGpxInt)*100)
                self.leftGpx.set("Gpx zbývá: " + str(len(os.listdir(inp))))
                root.update_idletasks()
                root.update()
                subGpx(inp,outp,orig,manual,form,emp,apiKey)
            

        def handleManualStart():
            inpToPass = False
            outToPass = False
            origToPass = False
            manualToPass = False
            form = self.formatEntryText.get()
            emp = self.emptyEntryText.get()
            if CheckDir(self.fileEntryText1.get()) == True:
                inpToPass = self.fileEntryText1.get()
            if CheckDir(self.fileEntryText2.get()) == True:
                outToPass = self.fileEntryText2.get()
            if CheckDir(self.fileEntryText3.get()) == True:
                origToPass = self.fileEntryText3.get()
            if CheckDir(self.fileEntryText3.get()) == True:
                manualToPass = self.fileEntryText4.get()
            startGpx(inpToPass,outToPass,origToPass,manualToPass,form,emp)

        def handleAutoStart():

            inpToPass = False
            outToPass = False
            origToPass = False
            manualToPass = False
            form = self.formatEntryText.get()
            emp = self.emptyEntryText.get()
            
            
            
                        


            
            if CheckDir(self.inpAutoPath) == True:
                inpToPass = self.inpAutoPath
            if CheckDir(self.outpAutoPath) == True:
                outToPass = self.outpAutoPath
            if CheckDir(self.origAutoPath) == True:
                origToPass = self.origAutoPath
            if CheckDir(self.manAutoPath) == True:
                manualToPass = self.manAutoPath
            startGpx(inpToPass,outToPass,origToPass,manualToPass,form,emp)


            #print(final_name_raw)
        #functions checking automatic folder search status and changing labels
            #entry1Check and entry2Check (input and output) disable start button if either is not found
        def entry1Check(fileEntryText1):
            if CheckDir(fileEntryText1) == True:
                self.inpStatM.set("✓")
                self.manualStatusLabel1.config(fg="green")
                self.manualStart["state"] = "active"
            else:
                self.inpStatM.set("X")
                self.manualStatusLabel1.config(fg="red")
                self.manualStart["state"] = "disabled"
        
        def entry2Check(fileEntryText2):
            if CheckDir(fileEntryText2) == True:
                self.outStatM.set("✓")
                self.manualStatusLabel2.config(fg="green")
                self.manualStart["state"] = "active"
            else:
                self.outStatM.set("X")
                self.manualStatusLabel2.config(fg="red")
                self.manualStart["state"] = "disabled"

        def entry3Check(fileEntryText3):
            if CheckDir(fileEntryText3) == True:
                self.origStatM.set("✓")
                self.manualStatusLabel3.config(fg="green")
            else:
                self.origStatM.set("X")
                self.manualStatusLabel3.config(fg="red")

        def entry4Check(fileEntryText4):
            if CheckDir(fileEntryText4) == True:
                self.manualStatM.set("✓")
                self.manualStatusLabel4.config(fg="green")
            else:
                self.manualStatM.set("X")
                self.manualStatusLabel4.config(fg="red")
        
        #Tkinter functions
            #handleBrowseClick1,2,3,4 - for selecting folders - opens File explorer window 
        def handleBrowseClick1():
            selected_directory = filedialog.askdirectory()
            self.fileEntryText1.set(selected_directory)
        def handleBrowseClick2():
            selected_directory = filedialog.askdirectory()
            self.fileEntryText2.set(selected_directory)
        def handleBrowseClick3():
            selected_directory = filedialog.askdirectory()
            self.fileEntryText3.set(selected_directory)
        def handleBrowseClick4():
            selected_directory = filedialog.askdirectory()
            self.fileEntryText4.set(selected_directory)


        # This function sets indicators for automatic folder search - runs on startup
        def autostatus():                   
            if (CheckDir(self.inpAutoPath)):
                self.inpStat.set("found")
                self.inputStatus.config(fg="green")
                inpstat = True    
            else:
                self.inpStat.set("not found")
                self.inputStatus.config(fg="red")
                self.autoStart["state"] = "disabled"
            if (CheckDir(self.outpAutoPath)):
                self.outStat.set("found")
                self.outputStatus.config(fg="green")
                outpstat = True 
            else:
                self.outStat.set("not found")
                self.outputStatus.config(fg="red")
                self.autoStart["state"] = "disabled"
            if (CheckDir(self.origAutoPath)):
                self.origStat.set("found")
                self.originalStatus.config(fg="green")
                origstat = True
            else:
                self.origStat.set("not found")
                self.originalStatus.config(fg="red")
            if (CheckDir(self.manAutoPath)):
                self.manualStat.set("found")
                self.manualStatus.config(fg="green")
                manstat = True  
            else:
                self.manualStat.set("not found")
                self.manualStatus.config(fg="red")
        #default actions
        #variables - mostly tk vars for entries
            #entries
        self.fileEntryText1 = tk.StringVar()
        self.fileEntryText2 = tk.StringVar()
        self.fileEntryText3 = tk.StringVar()
        self.fileEntryText4 = tk.StringVar()
                #format entry
        self.formatEntryText=tk.StringVar()
                #empty entry
        self.emptyEntryText = tk.StringVar()
            #labels - status indications
                #auto
        self.inpStat = tk.StringVar()
        self.outStat = tk.StringVar()
        self.origStat = tk.StringVar()
        self.manualStat = tk.StringVar()
                #manual
        self.inpStatM = tk.StringVar()
        self.outStatM = tk.StringVar()
        self.origStatM = tk.StringVar()
        self.manualStatM = tk.StringVar()
                #conversion process status - MainGpx and SubGPX progress reports
        self.countGpx = tk.StringVar()
        self.leftGpx = tk.StringVar()
        self.countErrors = tk.StringVar()

        self.countGpx.set("Gpx zbývá:")
        self.leftGpx.set("Gpxzbývý:")
        self.countErrors.set("Errors:")

            #manual entry validation setup
        self.inpStatM.set("X")
        self.outStatM.set("X")
        self.origStatM.set("X")
        self.manualStatM.set("X")

        self.test2 = self.fileEntryText1
            #checkButtons
        self.checkButton1_state = tk.IntVar()
        self.checkButton2_state = tk.IntVar()
        
            #loading
            
        #for autostart
        manstat = False
        origstat = False
        inpstat = False
        outpstat = False
            #paths
        self.manAutoPath  = ''.join((os.path.dirname(os.path.realpath(sys.argv[0])),"\manual"))
        self.origAutoPath = ''.join((os.path.dirname(os.path.realpath(sys.argv[0])),"\orig"))
        self.inpAutoPath  = ''.join((os.path.dirname(os.path.realpath(sys.argv[0])),"\input"))
        self.outpAutoPath = ''.join((os.path.dirname(os.path.realpath(sys.argv[0])),"\output"))
        
    #tkinter
        #welcome
        self.welcome= tk.Label(text="Přejmenovávač GPX souborů", width=40)
        self.welcome.config(font=("Arial", 18))
        self.welcome.grid(row=0,column=3,columnspan=4)
        #file options
            #labels
        self.col1 = tk.Label(text="manuální výběr")
        self.col2 = tk.Label(text="automatické hledání složek")
        self.col1.config(font=("Arial", 14))
        self.col2.config(font=("Arial", 14))

        self.statusLabel1 = tk.Label(text="input")
        self.statusLabel2 = tk.Label(text="output")
        self.statusLabel3 = tk.Label(text="orig(opt)")
        self.statusLabel4 = tk.Label(text="manual(opt)")

        self.manualStatusLabel1 = tk.Label(textvariable=self.inpStatM)
        self.manualStatusLabel2= tk.Label(textvariable=self.outStatM)
        self.manualStatusLabel3 = tk.Label(textvariable=self.origStatM)
        self.manualStatusLabel4 = tk.Label(textvariable=self.manualStatM)
                #init manual status labels color setup
        self.manualStatusLabel1.config(fg="red")
        self.manualStatusLabel2.config(fg="red")
        self.manualStatusLabel3.config(fg="red")
        self.manualStatusLabel4.config(fg="red")

        self.progress1 = tk.Label(textvariable=self.countGpx)
        self.progress2 = tk.Label(textvariable=self.leftGpx)
        self.progress3 = tk.Label(textvariable=self.countErrors)

            #Grids

        self.manualStatusLabel1.grid(row=3,column=2)
        self.manualStatusLabel2.grid(row=5,column=2)
        self.manualStatusLabel3.grid(row=7,column=2)
        self.manualStatusLabel4.grid(row=9,column=2)

        self.entryLabel1 = tk.Label(text="složka input")
        self.entryLabel2 = tk.Label(text="složka output")
        self.entryLabel3 = tk.Label(text="složka original")
        self.entryLabel4 = tk.Label(text="složka manual")
                    #Automatic status
        self.inputStatus =tk.Label(textvariable=self.inpStat)
        self.outputStatus =tk.Label(textvariable=self.outStat)
        self.originalStatus =tk.Label(textvariable=self.origStat)
        self.manualStatus =tk.Label(textvariable=self.manualStat)
                        #init setup
                #grids
        self.col1.grid(row=1,column=0,columnspan=2)
        self.col2.grid(row=1,column=5,columnspan=2)

        self.entryLabel1.grid(row=2,column=0,columnspan=2)
        self.entryLabel2.grid(row=4,column=0,columnspan=2)
        self.entryLabel3.grid(row=6,column=0,columnspan=2)
        self.entryLabel4.grid(row=8,column=0,columnspan=2)

        self.statusLabel1.grid(row = 2, column = 5)
        self.statusLabel2.grid(row = 3, column = 5) 
        self.statusLabel3.grid(row = 4, column = 5) 
        self.statusLabel4.grid(row = 5, column = 5)

        self.progress1.grid(row = 2, column = 7)
        self.progress2.grid(row = 3, column = 7)
        self.progress3.grid(row = 4, column = 7)                  

        self.inputStatus.grid(row = 2, column = 6) 
        self.outputStatus.grid(row = 3, column = 6) 
        self.originalStatus.grid(row = 4, column = 6) 
        self.manualStatus.grid(row = 5, column = 6)  
            #buttons
                    #browses
        self.inpButton = tk.Button(text="Browse",command=handleBrowseClick1)
        self.outButton = tk.Button(text="Browse",command=handleBrowseClick2)
        self.manButton = tk.Button(text="Browse",command=handleBrowseClick3)
        self.origButton = tk.Button(text="Browse",command=handleBrowseClick4)
                    #mainLaunchers
        self.manualStart = tk.Button(text="Spustit manuálně",command = handleManualStart)
        
                #ym2nit #   

        self.autoStart =tk.Button(text="Spustit automaticky",command=handleAutoStart) 
                #grids
        self.inpButton.grid(row=3,column=0,padx="3")
        self.outButton.grid(row=5,column=0)
        self.manButton.grid(row=7,column=0)
        self.origButton.grid(row=9,column=0)

        self.manualStart.grid(row=12,column=1,columnspan=2)
        self.autoStart.grid(row=12,column=4,columnspan=2)
            #entries
        self.fileEntry1 = tk.Entry(root, textvariable=self.fileEntryText1,width=60)
        self.fileEntryText1.set(default_input)
        self.fileEntry2 = tk.Entry(root, textvariable=self.fileEntryText2,width=60)
        self.fileEntryText2.set(default_output)
        self.fileEntry3 = tk.Entry(root, textvariable=self.fileEntryText3,width=60)
        self.fileEntryText3.set(default_orig)
        self.fileEntry4 = tk.Entry(root, textvariable=self.fileEntryText4,width=60)
        self.fileEntryText4.set(default_manual)
                #format entry
        self.formatEntry = tk.Entry(root,textvariable=self.formatEntryText,width=25)
        self.formatEntryText.set(default_format)
                #empty entry
        self.emptyEntry = tk.Entry(root,textvariable=self.emptyEntryText,width=5)
        self.emptyEntryText.set(default_empty)

                # entries grids
        self.fileEntry1.grid(row=3,column=1,columnspan=1)
        self.fileEntry2.grid(row=5,column=1,columnspan=1)
        self.fileEntry3.grid(row=7,column=1,columnspan=1)
        self.fileEntry4.grid(row=9,column=1,columnspan=1)
                    #format grid
        self.formatEntry.grid(row=11,column=3)
                    #empty entry grid
        self.emptyEntry.grid(row=11,column=4)
            #progress Bar
        self.pb = ttk.Progressbar(
            root,
            orient='horizontal',
            mode='determinate',
            length=280
            )
                #grids
        self.pb.grid(row=7,column=7)
            #Dropdown menu
    
        autostatus()
        self.fileEntryText1.trace("w", lambda name, index, mode,fileEntry1=self.fileEntryText1 : entry1Check(self.fileEntryText1.get()))
        self.fileEntryText2.trace("w", lambda name, index, mode,fileEntry2=self.fileEntryText2 : entry2Check(self.fileEntryText2.get()))
        self.fileEntryText3.trace("w", lambda name, index, mode,fileEntry3=self.fileEntryText3 : entry3Check(self.fileEntryText3.get()))
        self.fileEntryText4.trace("w", lambda name, index, mode,fileEntry4=self.fileEntryText4 : entry4Check(self.fileEntryText4.get()))
                
if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).grid(row=0,column=0)
    root.mainloop()