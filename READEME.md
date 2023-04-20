
Projekt je:

Napraviti aplikaciju koja će prikazivati podatke dobivene sa senzora i s interneta.

Aplikacija korisniku koji nije ulogiran prikazuje datum, 
grad po vašem odabiru i prognozu za njega dohvaćenu sa: 
    Weather Forecast API | Open-Meteo.com

Nakon što se korisnik ulogira aplikacija mora prikupiti podatke sa senzora za: 
vlažnost, temeperaturu i tlak.

Ovisno o vrijednostima potrebno je naglastiti 
prelazi li vrijednost neku maksimlanu vrijednost 
(npr. temperatura je veća od 23 sutpnja C) ili je vrijednost manaj od neke kritične( npr. tlak je ispod 1012 hPa)

Aplikacija ima mogućnost 
i spremanja podataka u bazu, te ispis podataka u JSON datoteku.



Struktura koda mora biti:


Folder u kojem je aplikacija
   - folder data u kojem će biti baza podataka
   - folder ispis u koji će se spremati izlazna json datoteka
   - folder app u kojem će biti kod podijeljen u module


Također, aplikacija podatke od senzora treba dobiti pozivanjem 
modula RaspberryPi u kojem ćete implementirati kalsu koja emulira RaspberryPi 
i vraća podatek sa svih senzora koji su definirani (senzori su isto klase)

KLASA Jagodica
dvije klase Jagodica i senzor 
instanciramo jednu i napunimo je drugom!
atribut klase ce biti senzori, umjesto

kada ju pozovemo i napunimo senzorima, metoda dohvati podatke i zelimo da jagodica dohvaca podatke

class Senzor:
   def dohvati_podatke(self):
   return 5

class Jagodica:

   koja kad je mi pokrenemo 






Kako je dosta štura specifikacija za početak je potrebno korištenjem 
računalnog razmišljanja detaljnije raspisati rad aplikacije u dokumentu.
nakon toga ćete krenuti u izradu aplikacije 
prema koracima koje ste definirali u tom dokumentu.


Za izradu ove aplikacije u Pythonu trebat ćete razviti sljedeće module i klasu:

RaspberryPi modul koji će simulirati RaspberryPi i senzore te će sadržavati klasu "Senzor" za prikupljanje podataka s pojedinog senzora i klasu "RaspberryPi" za prikupljanje svih podataka s RaspberryPi-a.

WeatherForecast modul za dohvaćanje vremenskih prognoza pomoću Weather Forecast API | Open-Meteo.com.

BazaPodataka modul za povezivanje i spremanje podataka u SQLite bazu podataka.

JSONIspis modul za spremanje podataka u JSON datoteku.

Glavni modul aplikacije koji će sadržavati korisničko sučelje, autentikaciju, prikupljanje i prikazivanje podataka s RaspberryPi-a i interneta te spremanje podataka u bazu podataka i JSON datoteku.

Ovdje je općenita struktura koda za ovu aplikaciju:

myapp/
   app/
      _init_.py
      main.py
      auth.py
      sensors.py
      weather.py
      database.py
      json_output.py
   data/
      mydatabase.db
   output/
      myoutput.json