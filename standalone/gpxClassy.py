#gpx2class
#  -*- coding: utf-8 -*-
"""
Created on Sat Oct 16 21:15:38 2022

@author: Hynek Lukes
"""

import tkinter as tk
#from tkinter import Label 
#from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
#from tkinter import Message
#from tkinter import Frame

import os
import shutil
import gpxpy        #not default, pip install
import sys
import json
import requests
import re
import string

class MainApplication(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
    #Loading config and settings files
        with open(os.path.join(sys.path[0],"key.json"),"r",encoding="UTF-8") as keyfile:
            key_raw = keyfile.read() 
        apiKey_raw = json.loads(key_raw)
        apiKey =apiKey_raw["key"]
    
    #functions
        #GPG function and two start functions - Tkinter button called, check directory function
        def CheckDir(path):
            if os.path.isdir(path) == True:
                return True
            else:
                return False
        global y
        y = 0
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
            mainGpx(inpToPass,outToPass,origToPass,manualToPass,form,emp)

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
            mainGpx(inpToPass,outToPass,origToPass,manualToPass,form,emp)
        
        
        #main gpx 
            #runs just once, while input folder is not empty, calls subGpx in while loop
            #Also handles progress reporting back to Tkinter 
        def mainGpx(inp,outp,orig,manual,form,empt):
            h = 0
            #print(inp)
            #print(outp)
            #print(orig)
            #print(manual)
            #print(empt)
            global countGpxInt
            self.manualStart["state"] = "disabled"
            self.autoStart["state"] = "disabled"
            inpFileList = os.listdir(inp)
            if manual == True:
                manual_files = os.listdir(manual)
            else:
                manual_files = os.listdir(outp)
            for i in inpFileList:
                i_list = i.split(".")
                moved_name = i_list[0]
                moved_ext = i_list[-1]
                moved_name_raw = i
                if i.endswith(".gpx"):
                    pass
                else:
                    while moved_name_raw in manual_files:
                        moved_name_raw = moved_name+"_"+str(h)+"."+moved_ext
                        h= h+1
                    if manual:
                        shutil.move(''.join((inp,"/",i)),''.join((manual,"/",moved_name_raw)))
                    else:
                        shutil.move(''.join((inp,"/",i)),''.join((outp,"/",moved_name_raw)))
            
            
            if (len(os.listdir(inp))):
                countGpxInt = len(os.listdir(inp))
            else:
                countGpxInt = 1
            self.countGpx.set("Gpx celkem: " + str(len(os.listdir(inp))))
            while len(os.listdir(inp)) > 0:
                self.leftGpx.set("Gpx zbývá: " + str(len(os.listdir(inp))))
                root.update_idletasks()
                subGpx(inp,outp,orig,manual,form,empt)
            self.leftGpx.set("Gpx zbývá: " + str(len(os.listdir(inp))))
            self.pb["value"] = 100-((len(os.listdir(inp))/countGpxInt)*100)
        #SubGpx
            # called by mainGpx
            # subGpx represents one file tranfer
        def subGpx(inp,outp,orig,manual,inp_str,empt):
            self.pb["value"] = 100-((len(os.listdir(inp))/countGpxInt)*100)
            self.leftGpx.set("Gpx zbývá: " + str(len(os.listdir(inp))))
            root.update_idletasks()
            root.update()
            global y
            y = 0
            manual_move = False
            file_name = os.listdir(inp)[0]
            in_path_file = ''.join((inp,"/",file_name))
            if orig != False:
                orig_cont = os.listdir(orig)
                if not file_name in orig_cont:
                        shutil.copy2(in_path_file,orig)

            gpx_file = open(in_path_file, 'r', encoding='utf-8')
            gpx = gpxpy.parse(gpx_file)
            data = gpx.tracks[0].segments[0]
            st_coord_lat = ('{0}'.format(data.points[0].latitude))
            st_coord_lon = ('{0}'.format(data.points[0].longitude))
            nd_coord_lat = ('{0}'.format(data.points[-1].latitude))
            nd_coord_lon = ('{0}'.format(data.points[-1].longitude))
            url_api = ''.join(("https://api.bigdatacloud.net/data/reverse-geocode?latitude=",st_coord_lat,"&longitude=",st_coord_lon,"&localityLanguage=en&key=",apiKey)) 
            response = requests.get(url_api)
            json_r = json.loads(response.text)
            url_api2 = ''.join(("https://api.bigdatacloud.net/data/reverse-geocode?latitude=",nd_coord_lat,"&longitude=",nd_coord_lon,"&localityLanguage=en&key=",apiKey)) 
            response2 = requests.get(url_api2)
            json_r2 = json.loads(response2.text)

            Cc = str(json_r['countryCode'])
            city1 = str(json_r['locality'])
            city2 = str(json_r2['locality'])
            data_points = data.points[0]
            year = str(data_points.time.year)
            month = str(data_points.time.month)
            day = str(data_points.time.day)
            if data_points.time.minute<10:
                start_time = (str(data_points.time.hour)+"∶0"+str(data_points.time.minute))
            else:
                start_time = (str(data_points.time.hour)+"∶"+str(data_points.time.minute))
            if data.points[-1].time.minute <10:
                end_time = (str(data.points[-1].time.hour)+"∶0"+str(data.points[-1].time.minute))
            else:
                end_time = (str(data.points[-1].time.hour)+"∶"+str(data.points[-1].time.minute))
            #duration calculation
            duration_raw = data.points[-1].time - data.points[0].time
            duration_sec = duration_raw.total_seconds()
            duration_hour = round(duration_sec/3600)
            if round((duration_sec%3600)/60) <10:
                duration_minutes = ("0"+str(round((duration_sec%3600)/60)))
            else:
                duration_minutes = str(round((duration_sec%3600)/60))
            
            duration = (str(duration_hour)+"∶"+str(duration_minutes))
            #Class for representations and content
            class Infos:
                infos=[]
                def __init__(self,content,rep):
                    self.infos.append(self)
                    self.content = content
                    self.rep = rep
            country_c = Infos(Cc,"%c")                          # %c            country code - always
            duration_c = Infos(duration,"%dur")                 # %dur          duration in format hour:minute
            country_foreign_c = Infos(Cc,"%f")                  # %f            country code, only when not cz - also deletes one character next to intself
            start_c = Infos(city1,"%st")                        # %st           locality of the first point- API
            end_c = Infos(city2,"%e")                           # %e            locality of the last point - API
            year_c = Infos(year,"%y")                           # %y            year of first point
            month_c = Infos(month,"%m")                         # %m            month of the first point
            day_c = Infos(day,"%d")                             # %d            day of first point
            start_time_c = Infos(start_time,"%ts")              # %ts           time of start in format  hour:minute   
            end_time_c = Infos(end_time,"%te")                  # %te           time of end in format  hour:minute

                                                                #second entry (default value = "0")
                                                                    #if one of i.content (time,start etc.) is emty
                                                                    # "0" - deletes one of surrounding characters
                                                                    # "1" - doesnt delete anything
                                                                    # "2" - moves the final gpx to manual if manual folder is selected, otherwise as "0"
                             
            nur= inp_str

            for i in Infos.infos:
                if str(i.rep) in inp_str:
                    if i.content != "":
                        if i.rep != country_foreign_c.rep:
                            nur = nur.replace(i.rep,i.content)
                            #print(str(i.rep))
                        else:
                            if i.content.lower() == "cz":
                                if nur.endswith(str(i.rep)):
                                    inst = re.sub("[^a-zA-Z]?%s" % i.rep,"",nur)
                                    nur = inst
                                elif nur.startswith(str(i.rep)):
                                    inst = re.sub("%s[^a-zA-Z]?" % i.rep,"",nur)
                                    nur = inst
                                else:
                                    inst = re.sub("%s[^a-zA-Z]?" % i.rep,"",nur)
                                    nur = inst
                                # TEST TEST TEST
                            else:
                                nur = nur.replace(i.rep,i.content)
                    else:
                        if (empt == "0") or (empt == "2"):
                            if empt =="2":
                                manual_move = True
                            if nur.endswith(str(i.rep)):
                                inst = re.sub("[^a-zA-Z]?%s" % i.rep,"",nur)
                                nur = inst
                            elif nur.startswith(str(i.rep)):
                                inst = re.sub("%s[^a-zA-Z]?" % i.rep,"",nur)
                                nur = inst
                            else:
                                inst = re.sub("%s[^a-zA-Z]?" % i.rep,"",nur)
                                nur = inst
                        elif empt == "1":
                            nur = nur.replace(i.rep,"")
                        else:
                            nur = nur.replace(i.rep,empt)
            gpx_file.close()
            final_name_raw = nur
            whitelist = set(string.ascii_letters + string.digits + "!_-()ěščřžýáíéĚŠČŘŽÝÁÍÉÚŮúůťď∶ ")
            final_name_raw = ''.join(c for c in final_name_raw if c in whitelist)
            nur = final_name_raw

            if (manual_move == False) or (manual == False):
                while (final_name_raw+".gpx") in os.listdir(outp):
                        y = y+1
                        final_name_raw = nur+"_"+str(y)
                final_name_raw = final_name_raw+".gpx"
                shutil.move(in_path_file,(outp+"\\"+final_name_raw))
            else:
                #Problem, os.listdir not working without manual % should not be a problem

                while (final_name_raw+".gpx") in os.listdir(manual):
                        y = y+1
                        final_name_raw = nur+"_"+str(y)
                final_name_raw = final_name_raw+".gpx"
                shutil.move(in_path_file,(manual+"/"+final_name_raw))
            
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
        self.fileEntry2 = tk.Entry(root, textvariable=self.fileEntryText2,width=60)
        self.fileEntry3 = tk.Entry(root, textvariable=self.fileEntryText3,width=60)
        self.fileEntry4 = tk.Entry(root, textvariable=self.fileEntryText4,width=60)
                #format entry
        self.formatEntry = tk.Entry(root,textvariable=self.formatEntryText,width=25)
        self.formatEntryText.set("%f-%y-%m-%st-%e")
                #empty entry
        self.emptyEntry = tk.Entry(root,textvariable=self.emptyEntryText,width=5)
        self.emptyEntryText.set("0")

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
    
    