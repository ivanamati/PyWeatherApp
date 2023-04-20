import requests
import json
import os
from geopy.geocoders import Nominatim

from datetime import datetime

from time import strftime



ime_datoteke = "prognoza_s_weba.json"
url = "https://api.open-meteo.com/v1/forecast?latitude=45.81&longitude=15.96&hourly=temperature_2m,relativehumidity_2m,surface_pressure&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=auto"
# url_ivanec = "https://api.open-meteo.com/v1/forecast?latitude=46.22&longitude=16.12&hourly=temperature_2m,relativehumidity_2m,surface_pressure&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=auto"
# url_zg = "https://api.open-meteo.com/v1/forecast?latitude=45.81&longitude=15.96&hourly=temperature_2m,relativehumidity_2m,surface_pressure&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=auto"
url_placeholder = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=auto"

class JsonPrognozaKlasa:
    
    def __init__(self, url, ime_datoteke):
        self.url = url
        self.ime_datoteke = ime_datoteke
        # longituda i latituda

    def dohvati_prognozu_s_meteo_api(self):
        """ ova metoda dohvaca podatke s weba """
        prognoza = {}
        try: 
            response = requests.get(self.url)
            if response.status_code == requests.codes.ok:
                # dobili smo listu dictova
                prognoza = response.json()
            else:
                prognoza = {}
        except Exception as e:
            print(f"Ooooops!!!  {e}")
            puna_putanja = self.spoji_json_s_folderom(self.ime_datoteke)
            with open(puna_putanja, "r", encoding="utf-8") as datoteka_koju_citamo:
                prognoza = json.load(datoteka_koju_citamo)
        return prognoza
      
    def upisi_json_u_datoteku(self, vrijednost_za_upis):
        """ ova metoda upisuje sadrzaj u datoteku """
        puna_putanja = self.spoji_json_s_folderom(self.ime_datoteke)
        with open(puna_putanja, "w", encoding="utf-8") as datoteka_u_koju_pisemo:
            json.dump(vrijednost_za_upis, datoteka_u_koju_pisemo, indent=4)
            
        print(f"Uspješno smo upisali podatak u datoteku {ime_datoteke}.")
                
    def upisi_json(self):
        prognoza = self.dohvati_prognozu_s_meteo_api()
        self.upisi_json_u_datoteku(prognoza)

    def spoji_json_s_folderom(self, datoteka):
        # if os.path.exists(datoteka):
        #     return datoteka
        #  puna putanja do foldera sa slikama koji se nalazi odmah uz ovaj file
        folder_za_json = os.path.abspath(
            os.path.join(
                os.path.dirname((os.path.dirname(__file__))),   # folder u kojem se nalazi ovaj file
                "ispis"              # folder u koji ćemo spremati json
            )
        )
        puna_putanja = os.path.join(
            folder_za_json, 
            datoteka
        )
        #print(puna_putanja)
        return str(puna_putanja)

    def procitaj_json_iz_datoteke(self):
        """ ova metoda cita sadrzaj datoteke 'json_s_weba """
        puna_putanja = self.spoji_json_s_folderom(self.ime_datoteke)
        with open(puna_putanja, "r", encoding="utf-8") as datoteka_koju_citamo:
            procitani_dict = json.load(datoteka_koju_citamo)
            print(procitani_dict)

   
#objekt = JsonPrognozaKlasa(url,ime_datoteke)
#objekt.izvuci_temperaturu_iz_jsona()
#objekt.izvuci_tlak_vlagu_temp_iz_jsona()
#objekt.upisi_json()
#objekt.procitaj_json_iz_datoteke()

# funkcija koja prima lat i long i vraca json prognoza klasa
def funkcija_koja_vraca_objekt(latitude,longitude, ime_datoteke):
    url_placeholder =   f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m,surface_pressure&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=auto"
    # url = https://api.open-meteo.com/v1/forecast?latitude=45.81&longitude=15.96&hourly=temperature_2m,relativehumidity_2m,surface_pressure&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=auto
    objekt = JsonPrognozaKlasa(url_placeholder, ime_datoteke)
    return objekt




# GEOLOKATOR
geolocator = Nominatim(user_agent="geoapiExercises")
# Latitude & Longitude input
Latitude = "45.82"
Longitude = "15.959999"

location = geolocator.reverse(f"{Latitude},{Longitude}")
 
# Display
#print(location)
address = location.raw['address']
#print(address)

grad = address.get('city')
drzava = address.get('country', '')
# print(f"{grad}, {drzava}")