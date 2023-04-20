
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


Također, aplikacija podatke od senzora treba dobiti pozivanjem 
modula RaspberryPi u kojem ćete implementirati kalsu koja emulira RaspberryPi 
i vraća podatke sa svih senzora koji su definirani (senzori su isto klase)

