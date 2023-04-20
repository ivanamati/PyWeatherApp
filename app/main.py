from gui import PrognozaApp

gui_program = PrognozaApp(repozitorij="SQLite_Baza_MeteoApp.sqlite")
#ZAGREB:
gui_program.pokreni(        
    latitude = "45.82",
    longitude = "15.959999")

#SPLIT 
# gui_program.pokreni(        
#     latitude = "43.508133",
#     longitude = "16.440193")

