import gpxpy
import requests
import shutil
import re
import os
import sys
import json
import requests
import string

#TODO
#in tkinter, disable buttons after movegpx launch
#Progress reporting to tkinter
#build not-gpx file clenup elsewhere





def subGpx(inp,outp,orig,manual,inp_str,empt,apiKey,country_ignored):
            
            global y
            y = 0
            manual_move = False
            if len(os.listdir(inp)) > 0:
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
                                if i.content.lower() == country_ignored:
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
                            #print (y)
                    final_name_raw = final_name_raw+".gpx"
                    shutil.move(in_path_file,(outp+"\\"+final_name_raw))
                else:
                    #Problem, os.listdir not working without manual

                    while (final_name_raw+".gpx") in os.listdir(manual):
                            y = y+1
                            final_name_raw = nur+"_"+str(y)
                            #print (y)
                    final_name_raw = final_name_raw+".gpx"
                    shutil.move(in_path_file,(manual+"/"+final_name_raw))
            else:
                pass
            