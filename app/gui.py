import tkinter as tk
import ttkbootstrap as ttk

from ttkbootstrap.constants import *
from ttkbootstrap import Style
from PIL import ImageTk, Image, ImageFilter
from tkinter.messagebox import showerror, showinfo

import json

from time import strftime
from datetime import date, datetime
import pathlib
import pandas as pd

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from json_output import funkcija_koja_vraca_objekt

from database import Korisnik, SQLARepozitorij, spoji_se_na_bazu
from prikaz_grafova import graf_podataka_sa_senzora,dohvati_podatke_sa_senzora, dohvati_prognozu, obradi_podatke, obradi_podatke_i_nacrtaj_graf
from sensors_simulator import ocitanje_vrijednosti
from configuration import dohvati_grad_iz_latitude_i_longitude



ime_datoteke = "prognoza_s_weba.json"
# url_zg = "https://api.open-meteo.com/v1/forecast?latitude=45.81&longitude=15.96&hourly=temperature_2m,relativehumidity_2m,surface_pressure&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=auto"

class PrognozaApp:

    def __init__(self, repozitorij):
        self.root = ttk.Window(themename="solar")
        self.root.title('MeteoApp - Parcijalni ispit')
        self.width = 560
        self.height = 540
        self.root.geometry(f'{self.width}x{self.height}')
        self.root['bg']= '#f3f6f4'
        self.repozitorij = repozitorij
        
        self.style = ttk.Style()
        self.style.configure('warning.Outline.TButton', font=('Quicksand', 11), borderwidth=2)
        self.pero = None

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def unos_korisnicko_ime_i_lozinka(self):
        oznaka_username = ttk.Label(
            self.root, text='username', 
            font='16',bootstyle="warning", background='#FBBC34')
        oznaka_username.place(anchor="center",relx=0.6,rely=0.23)
        
        self.username = ttk.Entry(self.root, bootstyle="warning", font = ('quicksand' , 9))
        self.username.place(anchor="center",relx=0.6,rely=0.28)

        oznaka_lozinka = ttk.Label(
            self.root, text='password', 
            font="16",bootstyle="warning", background='#FBBC34') 
        oznaka_lozinka.place(anchor="center",relx=0.6,rely=0.4)

        self.password = ttk.Entry(self.root, bootstyle="warning",show="*")
        self.password.place(anchor="center",relx=0.6,rely=0.45,width=154)

    def provjeri_korisnika(self):
        """ 
        ova metoda provjerava postoji li korisnik 
        (u dictu) uskoro u bazi 
        """
        korisnik = repozitorij.get_user_by_username(self.username.get())
        if korisnik:
            if self.password.get() == korisnik.password:
                #return True
                showinfo(title="Registracija", message=f"Korisnik '{korisnik.username}' postoji!\nDobrodoŠČi!")
                print(f"Korisnik {self.username.get()} postoji u bazi. Ulaz slobodan.")
                self.nacrtaj_prozor_tlak_vlaga_klasa()
            else: 
                showinfo(title="Registracija", message=f"Korisnik '{korisnik.username}' postoji,\nali lozinka je neispravna!")
                print(f'Korisnička lozinka je neispravna')
            return True
        else:
            showinfo(title="Registracija", message=f"Korisnik '{korisnik.username}' ne postoji!")
            print(f'Korisnik ne postoji')
            self.nacrtaj_pocetni_prozor()

    def dohvati_prognozu_s_urla(self,latitude,longitude):
        """ ova metoda dohvaca podatke s weba """
        self.pero = funkcija_koja_vraca_objekt(latitude=latitude, longitude=longitude, ime_datoteke="prognoza_s_weba_gui.json")
        puna_putanja = self.pero.dohvati_prognozu_s_meteo_api()
        #print(puna_putanja)
        return puna_putanja

    #napraviti da spremi json s guia koristeci tipku
    def povuci_json_s_gui(self):
        if self.pero:
            self.pero.upisi_json()
            self.pero.procitaj_json_iz_datoteke()

    def nacrtaj_pocetni_prozor(self):
        """ 
        ova metoda crta prozor koji pokazuje:
        datum, grad i prognozu 
        """
        self.pocetna_slikica("media\meteo.png")
        temperatura = self.dohvati_prognozu_s_urla(self.latitude,self.longitude)["current_weather"]["temperature"]
        longituda = self.dohvati_prognozu_s_urla(self.latitude,self.longitude)["longitude"]
        latituda = self.dohvati_prognozu_s_urla(self.latitude,self.longitude)["latitude"]
        today = date.today()
        # dd/mm/YY
        datum = today.strftime("%d.%m.%Y.")
        vrijeme = strftime("%H:%M:%S")
        grad = dohvati_grad_iz_latitude_i_longitude(latituda, longituda)

        self.label(
            self.root,f"{datum}\n\nGrad:\n{grad}\n\ntrenutno je {temperatura} Celziusa \n\n\n{vrijeme}",
            "5",bootstyle="light-inverse",poravnanje="center",pozadina="#FBBC34"
            )

        button_ulogiraj = ttk.Button(
            self.root, text='login', 
            style='warning.Outline.TButton',
            bootstyle="warning-outline", 
             padding=20, width=20, command=self.nacrtaj_login_prozor
            ).place(anchor="center", relx=0.5, rely=0.7)

    def nacrtaj_login_prozor(self): 
        """ 
        ova metoda crta prvi prozor aplikacije u kojem se 
        postojeci korisnik
        LOGIRA u aplikaciju PyFlora
        """
        self.clear_frame()
        self.pocetna_slikica("media\meteo.png")
        #self.nacrtaj_header_prijava()
        self.root['bg']= '#f3f6f4'
        self.unos_korisnicko_ime_i_lozinka()

        button_ulogiraj = ttk.Button(
            self.root, text='login', 
            style='warning.Outline.TButton',
            bootstyle="warning-outline", command=self.provjeri_korisnika,
             padding=20, width=20
            ).place(anchor="center", relx=0.5, rely=0.7)  #command=self.dohvati_podatke,
        
    def button_usporedba_podataka_senzora_i_jsona(self):
        self.clear_frame()
        self.pocetna_slikica("media\meteo.png")

        sati = self.dohvati_prognozu_s_urla(latitude=self.latitude,longitude=self.longitude)["hourly"]["time"]
        sada = datetime.now()
        iso_puni_sat = sada.strftime("%Y-%m-%dT%H:00")
        index_json = sati.index(iso_puni_sat)

        #vrijednosti s jsona
        temp_index = self.dohvati_prognozu_s_urla(latitude=self.latitude,longitude=self.longitude)["hourly"]["temperature_2m"][index_json] 
        tlak_index = self.dohvati_prognozu_s_urla(latitude=self.latitude,longitude=self.longitude)["hourly"]["surface_pressure"][index_json]
        vlaznost_index = self.dohvati_prognozu_s_urla(latitude=self.latitude,longitude=self.longitude)["hourly"]["relativehumidity_2m"][index_json]

        #vrijednosti sa senzora
        temperatura = ocitanje_vrijednosti(ime_senzora="temperatura",max_vrijednost= 180,min_vrijednost= -20,mjerna_jedinica= "°C")
        vlaga = ocitanje_vrijednosti("vlaga",100,0,"%")
        tlak =ocitanje_vrijednosti("tlak",1900,20,"hPa")

        self.usporedba_vrijednosti(temperatura,temp_index)

        button_refresh = ttk.Button(
            self.root, text='REFRESH', 
            bootstyle="danger-outline", 
             padding=20, width=20, command=self.nacrtaj_prozor_tlak_vlaga_klasa
            ).place(anchor="center", relx=0.6, rely=0.8)
    
    def usporedba_vrijednosti(self,vrijednost_senzor,vrijednost_web):
        """ ova metoda usporeduje vrijednosti sa senzora i weba
            te ih ispisuje kao label na ekranu aplikacije"""
        if vrijednost_senzor < vrijednost_web:
            self.label(self.root,f"Vrijednost web: {vrijednost_web}\nSenzor: {vrijednost_senzor}\nIzmjerena vrijednost \nsa senzora je niža.","5","light-inverse","center","#FBBC34")
        elif vrijednost_senzor > vrijednost_web:
            self.label(self.root,f"Vrijednost web: {vrijednost_web}\nSenzor: {vrijednost_senzor}\nIzmjerena vrijednost \nsa senzora je viša.","5","light-inverse","center","#FBBC34")
        else:
            self.label(self.root,f"Vrijednost web: {vrijednost_web}\nSenzor: {vrijednost_senzor}\nIzmjerena vrijednost \nsa senzora je ista.","5","light-inverse","center","#FBBC34")

    def nacrtaj_prozor_tlak_vlaga_za_json(self):
        """ ovu metodu ne koristim; 
        ona je bila tu kada su se temp, 
        vlaga i tlak skidali s weba"""
        self.clear_frame()
        self.pocetna_slikica()

        sati = self.dohvati_prognozu_s_urla()["hourly"]["time"]
        sada = datetime.now()
        iso_puni_sat = sada.strftime("%Y-%m-%dT%H:00")
        index_json = sati.index(iso_puni_sat)

        temp_index = self.dohvati_prognozu_s_urla()["hourly"]["temperature_2m"][index_json] 
        tlak_index = self.dohvati_prognozu_s_urla()["hourly"]["surface_pressure"][index_json]
        vlaznost_index = self.dohvati_prognozu_s_urla()["hourly"]["relativehumidity_2m"][index_json]

        today = date.today()
        datum = today.strftime("%d.%m.%Y.")
        vrijeme = strftime("%H:%M")
 
        self.label(self.root, 
                   f"{vrijeme}\n{datum}\n\ntrenutno je {temp_index} celziusa\n\ntlak je trenutno {tlak_index}\n\nvlaga je {vlaznost_index}", 
                   "5", "light-inverse","center","#FBBC34")

        button_izlaz = ttk.Button(
            self.root, text='IZLAZ', 
            bootstyle="danger-outline", 
             padding=20, width=20, command=self.root.destroy
            ).place(anchor="center", relx=0.5, rely=0.7)
        
    def nacrtaj_prozor_tlak_vlaga_klasa(self):
        self.clear_frame()
        self.pocetna_slikica("media\meteo.png")

        temperatura = ocitanje_vrijednosti(ime_senzora="temperatura",max_vrijednost= 180,min_vrijednost= -20,mjerna_jedinica= "°C")
        vlaga = ocitanje_vrijednosti("vlaga",100,0,"%")
        tlak =ocitanje_vrijednosti("tlak",1900,20,"hPa")

        today = date.today()
        datum = today.strftime("%d.%m.%Y.")
        vrijeme = strftime("%H:%M")
 
        self.label(self.root, 
                   f"{vrijeme}\n{datum}\n\ntemperatura je {temperatura} °C\n\ntlak je {tlak} hPa\n\nvlaga je {vlaga}%", 
                   "5", "light-inverse","center","#FBBC34")

        button_izlaz = ttk.Button(
            self.root, text='IZLAZ', 
            bootstyle="danger", 
             padding=15, width=15, command=self.root.destroy
            ).place(anchor="center", relx=0.2, rely=0.15)

        button_refresh = ttk.Button(
            self.root, text='REFRESH', 
            bootstyle="danger-outline", 
             padding=20, width=20, command=self.nacrtaj_prozor_tlak_vlaga_klasa
            ).place(anchor="center", relx=0.6, rely=0.75)

        button_usporedba = ttk.Button(
            self.root, text='USPOREDI TEMP', 
            bootstyle="danger-outline", 
             padding=15, width=15, command=self.button_usporedba_podataka_senzora_i_jsona
            ).place(anchor="center", relx=0.2, rely=0.4)

        button_refresh = ttk.Button(
            self.root, text='spremi prognozu', 
            bootstyle="danger-outline",
             padding=15, width=15, command=self.povuci_json_s_gui
            ).place(anchor="center", relx=0.2, rely=0.5)
        
        button_prikaz_grafa = ttk.Button(
            self.root, text='GRAFovlje',bootstyle = "danger_outline",
            padding=15, width=15,command=#self.prozor_s_grafovima
            graf_podataka_sa_senzora 
            #prikaz_sva_tri_grafa
            ).place(anchor="center",relx=0.2,rely=0.6)
        
    def prozor_s_grafovima(self):
        self.clear_frame()
        self.pocetna_slikica("media\meteo.png")

        podaci = dohvati_podatke_sa_senzora()
        df = obradi_podatke(podaci)

        figure1 = plt.Figure(figsize=(6, 5), dpi=100)
        ax1 = figure1.add_subplot(111)


        prikaz = FigureCanvasTkAgg(figure1, self.root)
        prikaz.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

        obradi_podatke_i_nacrtaj_graf(podaci,'senzori')
        df.plot(kind='line',legend=True,ax=ax1)
 
        ax1.set_title('Prikaz podataka sa senzora')



        povratak = ttk.Button(self.root,text='BACK', 
            bootstyle="danger-outline", 
             padding=20, width=20, command=self.nacrtaj_prozor_tlak_vlaga_klasa
            ).place(anchor="center", relx=0.5, rely=0.85)
            

 
    def pocetna_slikica(self,slikica):
        """ ova metoda prikazuje odabranu sliku kao pozadinu prozora """
        slika = ImageTk.PhotoImage(Image.open(slikica))
        label1 = ttk.Label(image = slika, borderwidth=0)
        label1.image = slika
        label1.place(anchor='center', relx=0.5, rely=0.5)
    
    def label(self,frame,tekst,font_slova,bootstyle, poravnanje, pozadina):
        """ ova metoda ispisuje automatski zadan label i radi place """
        tekst_labela = ttk.Label(
            frame, text=tekst, font=font_slova, 
            bootstyle=bootstyle,justify=poravnanje, 
            background=pozadina)
        tekst_labela.place(anchor="center",relx=0.6, rely=0.35)
        
    def pokreni(self,latitude,longitude):
        # tu bi trebalo pozvati konfiguraciju (postavke s lat i long) i proslijediti u pocetni prozor 
        self.latitude = latitude
        self.longitude = longitude
        self.nacrtaj_prozor_tlak_vlaga_klasa()
        #self.nacrtaj_pocetni_prozor()
        self.root.mainloop()
   
        # tu ucitava postavke
        # tu da prima latitude i longitude, da zadam self.latitude je nesto, self.longitude je nesto
        # pa kada se pokrece da uzima ove podatke


session = spoji_se_na_bazu("SQLite_Baza_MeteoApp.sqlite")
repozitorij = SQLARepozitorij(session)


def load_configuration():
    putanja_do_ovog_filea = pathlib.Path(__file__).parent
    configuration_file = putanja_do_ovog_filea.joinpath("postavke.json")
    if configuration_file.exists():
        with open(configuration_file.absolute(),"r", encoding="utf-8") as konfiguracijski_file:
            konfiguracija = json.load(konfiguracijski_file)
    else:
        print("Ne postoji konfiguracija")
        konfiguracija = {"latitude":46.22306, "longitude":16.12}
    return konfiguracija


# if __name__ == "__main__":
#     gui_program = PrognozaApp(repozitorij="SQLite_Baza_MeteoApp.sqlite")
#     gui_program.pokreni(        
#     latitude = "45.82",
#     longitude = "15.959999")


#     # # ovdje predati latitude i longitude u pokreni
