import requests
import json
import os
from geopy.geocoders import Nominatim

from datetime import datetime

from time import strftime
from json_output import funkcija_koja_vraca_objekt


# UČIN KOD ZA DOHVATI PROGNOZE - 29.3.
base_url = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,relativehumidity_2m,surface_pressure&current_weather=true&timezone=auto"

def dohvati_prognozu(url, latitude, longitude):
    return requests.get(url.format(latitude=latitude, longitude=longitude)).json()

def obradi_prognozu(podaci):
    data = []
    hourly_data = podaci.get("hourly", {})
    for indeks, vrijeme in enumerate(hourly_data.get("time", [])):
        # ZADATAK: tu koristiti klasu, a ne dict. 
        # Klasa mora biti ista kao i u simulator senzora SensorZaRaspberryPi.dohvati_podatke
        # napomena: tu će biti 3 objekta, ne 1
        #data[vrijeme] = {
        #    "TEMPERATURA": hourly_data["temperature_2m"][indeks],
        #    "TLAK": hourly_data["surface_pressure"][indeks],
        #    "VLAGA": hourly_data["relativehumidity_2m"][indeks],
        #}
        data.append({
            "ime senzora": "TEMPERATURA",
            "vrijednost": hourly_data["temperature_2m"][indeks],
            "mjerna jedinica": "°C",
            "vrijeme dohvata": vrijeme
        })
        
        data.append({
            "ime senzora": "TLAK",
            "vrijednost": hourly_data["surface_pressure"][indeks],
            "mjerna jedinica": "hPA",
            "vrijeme dohvata": vrijeme
        })
        
        data.append({
            "ime senzora": "VLAGA",
            "vrijednost": hourly_data["relativehumidity_2m"][indeks],
            "mjerna jedinica": "%",
            "vrijeme dohvata": vrijeme
        })
    return data


# MOJ KOD ZA PARCIJALNI ISPIT ZA DOHVAT PROGNOZE

ime_datoteke = "prognoza_s_weba.json"
url_neki = "https://api.open-meteo.com/v1/forecast?latitude=45.81&longitude=15.96&hourly=temperature_2m,relativehumidity_2m,surface_pressure&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=auto"
url_placeholder = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=auto"
url = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly={temperatura},{vlaznost},{tlak}&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=auto"

class Prognoza:

    def __init__(self, tip_vrijednosti,vrijednost,mjerna_jedinica,latitude,longitude):
        self.tip_vrijednosti = tip_vrijednosti
        self.vrijednost = vrijednost
        self.mjerna_jedninica = mjerna_jedinica
        self.latitude = latitude
        self.longitude = longitude


    def dohvati_prognozu_s_meteo_api(self):
        """ ova metoda dohvaca podatke s weba """
        url = f"https://api.open-meteo.com/v1/forecast?latitude={self.latitude}&longitude={self.longitude}&hourly=temperature_2m,relativehumidity_2m,surface_pressure&daily=temperature_2m_max,temperature_2m_min&current_weather=true&timezone=auto"
        prognoza = {}
        try: 
            response = requests.get(url)
            if response.status_code == requests.codes.ok:
                # dobili smo listu dictova
                prognoza = response.json()
            else:
                prognoza = {}
        except Exception as e:
            print(f"Ooooops!!!  {e}")
        return prognoza
    

    def vrijednosti_s_weba(self,vrijednost):  #"temperature_2m", "relativehumidity_2m","surface_pressure"
        index = self.aktualni_sat()
        vrijednost_api = self.dohvati_prognozu_s_meteo_api()["hourly"][vrijednost][index]
        print (vrijednost_api)
    
    def aktualni_sat(self):
        sati = self.dohvati_prognozu_s_meteo_api()["hourly"]["time"]
        sada = datetime.now()
        iso_puni_sat = sada.strftime("%Y-%m-%dT%H:00")
        index_json = sati.index(iso_puni_sat)
        #return index_json
        return index_json

objekt = Prognoza("temperatura"," ","celzijevci",latitude = "45.82",longitude = "15.959999")
# ->
# print("Trenutna temp je:")
# objekt.vrijednosti_s_weba(("temperature_2m"))
# print("Trenutna vlaga je:")
# objekt.vrijednosti_s_weba(("relativehumidity_2m"))
# print("Trenutni tlak je:")
# objekt.vrijednosti_s_weba(("surface_pressure"))

# funkcija koja prima lat i long i vraca json prognoza klasa
# ->
def funkcija_koja_vraca_prognozu_s_weba():
    prognoza = Prognoza()
    return prognoza







