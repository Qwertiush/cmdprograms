class Zwierze:
    def __init__(self, nazwa, wiek):
        self.nazwa = nazwa
        self.wiek = wiek

    def wydaj_dzwiek(self):
        pass

    def poruszaj_sie(self):
        pass

    def urodz_sie(self):
        pass

class Ssak(Zwierze):
    def __init__(self, nazwa, wiek, typ_siersci):
        super().__init__(nazwa, wiek)
        self.typ_siersci = typ_siersci

    def urodz_sie_zyworodnie(self):
        pass

    def urodz_sie(self):
        super().urodz_sie()
        self.urodz_sie_zyworodnie()

class Gad(Zwierze):
    def __init__(self, nazwa, wiek, dlugosc_ogona):
        super().__init__(nazwa, wiek)
        self.dlugosc_ogona = dlugosc_ogona

    def urodz_sie_jajorodnie(self):
        pass

    def urodz_sie(self):
        super().urodz_sie()
        self.urodz_sie_jajorodnie()

class Kot(Ssak):
    def __init__(self, nazwa, wiek, typ_siersci, rasa):
        super().__init__(nazwa, wiek, typ_siersci)
        self.rasa = rasa

    def miaucz(self):
        print("Miau")

    def wydaj_dzwiek(self):
        super().wydaj_dzwiek()
        self.miaucz()

class WazRzeczny(Gad):
    def __init__(self, nazwa, wiek, dlugosc_ogona, dlugosc_ciala):
        super().__init__(nazwa, wiek, dlugosc_ogona)
        self.dlugosc_ciala = dlugosc_ciala

    def sycz(self):
        print("Sssssss")

    def wydaj_dzwiek(self):
        super().wydaj_dzwiek()
        self.sycz()

Zwierze zwierze = Kot("Filemon", 3, "krótka", "syjamski");
Zwierze zwierze2 = WazRzeczny("Wąż", 5, 2, 3);
