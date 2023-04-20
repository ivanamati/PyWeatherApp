from enum import unique
import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Korisnik(Base):
    __tablename__ = "Korisnici"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True, nullable = False)
    password = db.Column(db.String, nullable=False)

    def ispisi_podatke(self):
        print(f"ID={self.id}, Name={self.username}, password={self.password}")

def spoji_se_na_bazu(ime_baze):
    """
    Glavna funkcija ovog modula
    Spaja se na bazu i kreria tablicu ako ne postoji
    """
    # Povezimo se s bazom koristeci SQLAlchemy
    db_engine = db.create_engine(f"sqlite:///{ime_baze}")

    # Kreiraj bazu sa tablicom koju smo deklarirali u klasi Korisnik
    # odnosno izvršit će SQL upit:
    """
        CREATE TABLE IF NOT EXISTS Korisnici (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL, 
        );
    """
    Base.metadata.create_all(db_engine)

    # otvori konekciju koju ćemo koristiti za upite prema bazi
    Session = sessionmaker()
    Session.configure(bind=db_engine)
    session = Session()
    return session

class SQLARepozitorij:

    def __init__(self, session):
        # ovo je session koji dobijemo nakon poziva funkcije spoji_se_na_bazu
        self.session = session

    def create_user(self, user: Korisnik):
        """
        spremi objekt tipa Employee u bazu i vrati isti objekt natrag
        :param djelatnik: objekt tipa Employee
        :type djelatnik: Employee
        :return: Employee
        :rtype: Employee
        """

        # INSERT INTO Employees(id, name, email) VALUES(?, ?, ?)
        self.session.add(user)
        self.session.commit()
        return user

    def get_user_by_username(self, username):
        # ako nemamo u bazi zapisa koji ima username = username, ovo vraća None!
        return self.session.query(Korisnik).filter(Korisnik.username==username).first()


# session = spoji_se_na_bazu("SQLite_Baza_MeteoApp.sqlite")
# repozitorij = SQLARepozitorij(session)


