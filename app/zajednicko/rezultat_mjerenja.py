import random

class RezultatMjerenja:
    tip="NISTA"
    def __init__(self, vrijednost, mjerna_jedinica):
        self.vrijednost = vrijednost
        self.mjerna_jedinica = mjerna_jedinica



class TempRezultatMjerenja(RezultatMjerenja):
    tip="TEMPERATURA"

rez_1 = RezultatMjerenja(100,'C')
rez_2 = RezultatMjerenja(90,'C')

if rez_1.tip ==rez_2.tip:
    print(rez_1.vrijednost== rez_2.vrijednost)


class RezultatMjerenja:
    def __init__(self, tip_senzora, vrijednost, mjerna_jedinica)->None:
        self.tip_senzora = tip_senzora
        self.vrijednost = vrijednost 
        self.mjerna_jedinica = mjerna_jedinica
        


rez_1 = RezultatMjerenja("TEMEPRATURA",100,'C')
rez_2 = RezultatMjerenja("TEMEPRATURA", 90,'C')

if rez_1.tip ==rez_2.tip:
    print(rez_1.vrijednost== rez_2.vrijednost)



        # da vratim klasu cije cu podatke koristiti
        # u returnu vratiti nesto kao sto mi je bio onaj pero
        # da imamo klasu koja vraca neke podatke

        # imat cemo listu instanci klasa pa cemo tako usporedivati
        # poigrati se s klasama, od funkcija do punjenja

        # mogli bi napraviti jednostavniji primjer s vise klasa i nasljedivanjem, 
        # iskoristiti one pojedinacne korake s klasama koje smo imali prosli vikend


        # ZADATAK: tu koristiti klasu, a ne dict. 
        # Klasa mora biti ista kao i u simulator senzora SensorZaRaspberryPi.dohvati_podatke
        # napomena: tu će biti 3 objekta, ne 1

        # osmisliti klasu umjesto ovog dicta
        # u klasi nam teba biti kojeg je tippa senzor i koja je vrijednost i dodati jedinci
