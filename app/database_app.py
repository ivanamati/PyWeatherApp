from database import SQLARepozitorij, Korisnik, spoji_se_na_bazu

def kreiraj_korisnika_koji_ne_postoji(repozitorij):
    korisnicno_ime = input("Unesi korisnicko ime: ")
    lozinka = input ("Unesite lozinku: ")
    korisnik = Korisnik(
            username=korisnicno_ime,
            password=lozinka
        )
        #user.ispisi_podatke()
        # tek nakon poziva ove metode imamo objekt u BAZI
    print("Upisujemo korisnika...")
    repozitorij.create_user(korisnik)
    print("Podaci upisanog korisnika su: ", end='')
    korisnik.ispisi_podatke()
    return korisnik


def pokreni_aplikaciju(ime_baze):
    # s ova dva reda ispod se spajamo na bazu i povezujemo s repozitorijem
    session = spoji_se_na_bazu(ime_baze)
    repozitorij = SQLARepozitorij(session)
    kreiraj_korisnika_koji_ne_postoji(repozitorij)


# ovime se postiže da se kod importa ovog modula ne izvodi ništa
if __name__ == "__main__":
    pokreni_aplikaciju("SQLite_Baza_MeteoApp.sqlite")