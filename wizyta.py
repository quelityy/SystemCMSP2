class Wizyta:
    def __init__(self, pesel, imie, terapia, telefon, opis, koszt, status="Oczekuje"):
        self.pesel = pesel
        self.imie = imie
        self.terapia = terapia
        self.telefon = telefon
        self.opis = opis
        self.koszt = koszt
        self.status = status

    def to_dict(self):
        return {
            "pesel": self.pesel,
            "imie": self.imie,
            "terapia": self.terapia,
            "telefon": self.telefon,
            "opis": self.opis,
            "koszt": self.koszt,
            "status": self.status,
        }
