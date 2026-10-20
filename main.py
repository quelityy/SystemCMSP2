# importy
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from wizyta import Wizyta


# slownik z terapiami i zabiegami
TERAPIE = {
    "Ortopedyczna": ["Masaz gleboki", "Mobilizacja stawow", "Taping", "Cwiczenia po zlamaniu", "Stretching"],
    "Neurologiczna": ["Metoda Bobath", "Metoda PNF", "Rehabilitacja po udarze", "Elektrostymulacja"],
    "Sportowa": ["Masaz sportowy", "Krioterapia", "Ultradzwieki", "Powrot do sportu"],
    "Kregoslupowa": ["McKenzie", "Trakcja manualna", "Cwiczenia stabilizacyjne", "TENS"],
    "Pediatryczna": ["NDT Bobath", "Integracja sensoryczna", "Cwiczenia korekcyjne"],
    "Geriatryczna": ["Trening rownowagi", "Cwiczenia wzmacniajace", "Masaz relaksacyjny"],
}


class Aplikacja:

    def __init__(self, okno):
        self.okno = okno
        self.okno.title("Centrum Rehabilitacji - Zarzadzanie Wizytami")
        self.okno.state("zoomed")
        self.okno.configure(bg="#1a1a2e")

        self.wizyty = []
        self.plik = "wizyty.json"
        self.okno_zbudowane = False  # flaga zeby wiedziec czy okno jest juz gotowe

        self.wczytaj()
        self.buduj_okno()
        self.okno_zbudowane = True
        self.odswiez()

    # budowanie okna glownego
    def buduj_okno(self):
        self.okno.geometry("1100x700")
        self.okno.config(bg="#20232b")

        czcionka = ("Segoe UI", 10)
        czcionka_bold = ("Segoe UI", 11, "bold")

        # gorny pasek z tytulem
        naglowek = tk.Frame(self.okno, bg="#15181d", bd=0)
        naglowek.pack(fill="x")
        tk.Label(naglowek, text="Centrum Rehabilitacji i Fizjoterapii", font=("Segoe UI", 18, "bold"), bg="#15181d", fg="#61dafb").pack(side="left", padx=20, pady=14)
        tk.Label(naglowek, text="Konrad Płonka", font=("Segoe UI", 10), bg="#15181d", fg="#abb2bf").pack(side="right", padx=20)

        # glowny kontener
        ramka_glowna = tk.Frame(self.okno, bg="#20232b")
        ramka_glowna.pack(fill="both", expand=True, padx=16, pady=16)

        # lewy panel - formularz
        lewa = tk.Frame(ramka_glowna, bg="#282c34", bd=0)
        lewa.pack(side="left", fill="y", padx=(0, 12), ipadx=10, ipady=10)

        tk.Label(lewa, text="WPROWADŹ DANE", font=czcionka_bold, bg="#282c34", fg="#e5e5e5").grid(row=0, column=0, columnspan=2, pady=(0, 14))

        tk.Label(lewa, text="PESEL", bg="#282c34", fg="#a3aab8", font=czcionka).grid(row=1, column=0, sticky="w", pady=6)
        self.pole_pesel = tk.Entry(lewa, width=24, font=czcionka, bg="#343a46", fg="#f5f7fa", insertbackground="#f5f7fa", bd=0)
        self.pole_pesel.grid(row=1, column=1, pady=6, padx=(0, 6))

        tk.Label(lewa, text="IMIE I NAZWISKO", bg="#282c34", fg="#a3aab8", font=czcionka).grid(row=2, column=0, sticky="w", pady=6)
        self.pole_imie = tk.Entry(lewa, width=24, font=czcionka, bg="#343a46", fg="#f5f7fa", insertbackground="#f5f7fa", bd=0)
        self.pole_imie.grid(row=2, column=1, pady=6, padx=(0, 6))

        tk.Label(lewa, text="TERAPIA", bg="#282c34", fg="#a3aab8", font=czcionka).grid(row=3, column=0, sticky="w", pady=6)
        lista_terapii = []
        for nazwa in TERAPIE:
            lista_terapii.append(nazwa)
        self.pole_terapia = ttk.Combobox(lewa, values=lista_terapii, width=22, font=czcionka)
        self.pole_terapia.grid(row=3, column=1, pady=6, padx=(0, 6))
        self.pole_terapia.set("Wybierz...")
        self.pole_terapia.bind("<<ComboboxSelected>>", self.zmien_terapie)

        tk.Label(lewa, text="PROCEDURA", bg="#282c34", fg="#a3aab8", font=czcionka).grid(row=4, column=0, sticky="w", pady=6)
        self.pole_procedura = ttk.Combobox(lewa, values=[], width=22, font=czcionka)
        self.pole_procedura.grid(row=4, column=1, pady=6, padx=(0, 6))
        self.pole_procedura.set("Wybierz...")

        tk.Label(lewa, text="TELEFON", bg="#282c34", fg="#a3aab8", font=czcionka).grid(row=5, column=0, sticky="w", pady=6)
        self.pole_telefon = tk.Entry(lewa, width=24, font=czcionka, bg="#343a46", fg="#f5f7fa", insertbackground="#f5f7fa", bd=0)
        self.pole_telefon.grid(row=5, column=1, pady=6, padx=(0, 6))

        tk.Label(lewa, text="KOSZT (ZL)", bg="#282c34", fg="#a3aab8", font=czcionka).grid(row=6, column=0, sticky="w", pady=6)
        self.pole_koszt = tk.Entry(lewa, width=24, font=czcionka, bg="#343a46", fg="#f5f7fa", insertbackground="#f5f7fa", bd=0)
        self.pole_koszt.grid(row=6, column=1, pady=6, padx=(0, 6))

        tk.Label(lewa, text="NOTATKI", bg="#282c34", fg="#a3aab8", font=czcionka).grid(row=7, column=0, sticky="nw", pady=6)
        self.pole_opis = tk.Text(lewa, width=24, height=6, font=czcionka, bg="#343a46", fg="#f5f7fa", insertbackground="#f5f7fa", bd=0)
        self.pole_opis.grid(row=7, column=1, pady=6, padx=(0, 6))

        dodaj_button = tk.Button(lewa, text="DODAJ WIZYTE", bg="#61dafb", fg="#20232b", font=czcionka_bold, bd=0, activebackground="#4fb8e8", command=self.dodaj_wizyte)
        dodaj_button.grid(row=8, column=0, columnspan=2, pady=12, ipadx=10, ipady=6)

        # prawy panel - tabela
        prawa = tk.Frame(ramka_glowna, bg="#20232b")
        prawa.pack(side="left", fill="both", expand=True)

        podtytul = tk.Label(prawa, text="Zarzadzanie wizytami", font=czcionka_bold, bg="#20232b", fg="#e5e5e5")
        podtytul.pack(anchor="w", pady=(0, 8))

        # wyszukiwarka
        szukaj = tk.Frame(prawa, bg="#20232b")
        szukaj.pack(fill="x", pady=(0, 10))
        tk.Label(szukaj, text="Szukaj:", bg="#20232b", fg="#abb2bf", font=czcionka).pack(side="left")
        self.pole_szukaj = tk.Entry(szukaj, bg="#343a46", fg="#f5f7fa", insertbackground="#f5f7fa", bd=0, font=czcionka)
        self.pole_szukaj.pack(side="left", fill="x", expand=True, padx=(8, 0))
        self.pole_szukaj.bind("<KeyRelease>", self.filtruj_wizyty)

        # styl tabeli
        styl = ttk.Style()
        styl.theme_use("clam")
        styl.configure("Treeview", background="#1f242e", fieldbackground="#1f242e", foreground="#e5e5e5", rowheight=28, font=czcionka)
        styl.configure("Treeview.Heading", background="#282c34", foreground="#61dafb", font=czcionka_bold)
        styl.map("Treeview", background=[("selected", "#61dafb")], foreground=[("selected", "#20232b")])
        styl.configure("Vertical.TScrollbar", background="#282c34", troughcolor="#1f242e", arrowcolor="#61dafb")

        # tabela z wizytami
        kolumny = ("pesel", "imie", "terapia", "procedura", "telefon", "notatki", "koszt", "status")
        self.tabela = ttk.Treeview(prawa, columns=kolumny, show="headings")
        self.tabela.tag_configure("Oczekujace", background="#1f242e")
        self.tabela.tag_configure("Zakonczona", background="#2d4a38")

        # ustawienie szrokosci kolumn
        szerokosci = [100, 150, 110, 140, 110, 160, 90, 100]
        for i in range(len(kolumny)):
            self.tabela.heading(kolumny[i], text=kolumny[i].capitalize())
            self.tabela.column(kolumny[i], width=szerokosci[i], anchor="center")

        self.tabela.pack(fill="both", expand=True, side="left")

        # scrollbar
        scroll = ttk.Scrollbar(prawa, orient="vertical", command=self.tabela.yview, style="Vertical.TScrollbar")
        self.tabela.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

        # dolna stopka z przyciskami
        dolny = tk.Frame(self.okno, bg="#15181d")
        dolny.pack(fill="x", padx=0, pady=0)

        self.etykieta_info = tk.Label(dolny, text="Wszystkie: 0 | Zakonczone: 0 | Oczekujace: 0", font=czcionka, bg="#15181d", fg="#abb2bf")
        self.etykieta_info.pack(side="left", padx=20)

        btn1 = tk.Button(dolny, text="Zakoncz wizyte", bg="#61dafb", fg="#20232b", font=czcionka_bold, bd=0, activebackground="#4fb8e8", command=self.zakoncz_wizyte)
        btn1.pack(side="left", padx=12, pady=10, ipadx=10, ipady=6)
        btn2 = tk.Button(dolny, text="Usun wpis", bg="#ff6b6b", fg="#20232b", font=czcionka_bold, bd=0, activebackground="#ff8787", command=self.usun_wizyte)
        btn2.pack(side="left", padx=12, pady=10, ipadx=10, ipady=6)

        self.etykieta_suma = tk.Label(dolny, text="Suma: 0.00 zl", font=czcionka_bold, bg="#15181d", fg="#e5e5e5")
        self.etykieta_suma.pack(side="right", padx=20)

    # zmiana listy procedur po wybraniu terapii
    def zmien_terapie(self, event):
        wybrana = self.pole_terapia.get()
        if wybrana in TERAPIE:
            self.pole_procedura.config(values=TERAPIE[wybrana])
            self.pole_procedura.set("Wybierz procedure")

    # dodawanie nowej wizyty z walidacja
    def dodaj_wizyte(self):
        pesel = self.pole_pesel.get().strip()
        imie = self.pole_imie.get().strip()
        terapia = self.pole_terapia.get()
        procedura = self.pole_procedura.get()
        telefon = self.pole_telefon.get().strip()
        opis = self.pole_opis.get("1.0", tk.END).strip()
        koszt_str = self.pole_koszt.get().strip()

        # walidacja PESEL
        if len(pesel) == 0:
            messagebox.showwarning("Błąd!", "Pole PESEL jest puste!")
            return
        if len(pesel) != 11:
            messagebox.showwarning("Błąd!", "PESEL musi miec dokladnie 11 cyfr! (wpisano: " + str(len(pesel)) + ")")
            return
        if not pesel.isdigit():
            messagebox.showwarning("Błąd!", "PESEL moze zawierac tylko cyfry!")
            return

        # walidacja imienia i nazwiska
        if len(imie) == 0:
            messagebox.showwarning("Błąd!", "Pole Imie i Nazwisko jest puste!")
            return
        if len(imie) < 3:
            messagebox.showwarning("Błąd!", "Imie i Nazwisko musi miec co najmniej 3 znaki!")
            return
        if len(imie) > 50:
            messagebox.showwarning("Błąd!", "Imie i Nazwisko nie moze byc dluzsze niz 50 znakow!")
            return
        # sprawdzam kazda litere czy to litera lub spacja
        for i in range(len(imie)):
            znak = imie[i]
            if znak.isalpha() == False and znak != " ":
                messagebox.showwarning("Błąd!", "Imie i Nazwisko moze zawierac tylko litery i spacje! (znaleziono: '" + znak + "')")
                return

        # walidacja terapii
        if terapia == "Wybierz..." or terapia not in TERAPIE:
            messagebox.showwarning("Błąd!", "Wybierz terapie z listy!")
            return

        # walidacja telefonu - pole jest opcjonalne
        if len(telefon) > 0:
            if len(telefon) != 9:
                messagebox.showwarning("Błąd!", "Numer telefonu musi miec 9 cyfr! (wpisano: " + str(len(telefon)) + ")")
                return
            if not telefon.isdigit():
                messagebox.showwarning("Błąd!", "Numer telefonu moze zawierac tylko cyfry!")
                return

        # walidacja kosztu
        if len(koszt_str) == 0:
            messagebox.showwarning("Błąd!", "Pole Koszt jest puste!")
            return
        try:
            koszt = float(koszt_str.replace(",", "."))
            if koszt < 0:
                messagebox.showwarning("Błąd!", "Koszt nie moze byc ujemny!")
                return
        except:
            messagebox.showerror("Błąd!", "Koszt musi byc liczba! (np. 150 lub 99.50)")
            return

        # tworze nowa wizyte i dodaje do listy
        wizyta = Wizyta(pesel, imie, terapia, telefon, procedura + " | " + opis, koszt)
        self.wizyty.append(wizyta)

        # czyszcze pola formularza
        self.pole_pesel.delete(0, tk.END)
        self.pole_imie.delete(0, tk.END)
        self.pole_terapia.set("Wybierz terapie")
        self.pole_procedura.set("Najpierw wybierz terapie")
        self.pole_procedura.config(values=[])
        self.pole_telefon.delete(0, tk.END)
        self.pole_koszt.delete(0, tk.END)
        self.pole_opis.delete("1.0", tk.END)

        self.odswiez()
        self.zapisz()

    # odswiezenie tabeli
    def odswiez(self):
        # usuwam wszystkie wiersze z tabeli
        for w in self.tabela.get_children():
            self.tabela.delete(w)

        # pobieram tekst wyszukiwania jesli okno jest juz zbudowane
        filter_text = ""
        if self.okno_zbudowane == True:
            filter_text = self.pole_szukaj.get().strip().lower()

        suma = 0.0
        widoczne = 0
        zakonczone = 0
        oczekujace = 0

        for i in range(len(self.wizyty)):
            w = self.wizyty[i]

            # licze wizyty wg statusu
            if w.status == "Zakonczona":
                zakonczone = zakonczone + 1
            else:
                oczekujace = oczekujace + 1

            # rozdzielam procedure od notatek
            if " | " in w.opis:
                czesci = w.opis.split(" | ", 1)
                proc = czesci[0]
                notatki = czesci[1]
            else:
                proc = ""
                notatki = w.opis

            # filtrowanie - sprawdzam czy tekst wyszukiwania jest w danych wizyty
            tekst = w.pesel + " " + w.imie + " " + w.terapia + " " + proc + " " + notatki + " " + w.status
            tekst = tekst.lower()
            if filter_text != "" and filter_text not in tekst:
                continue

            koszt_tekst = str(round(w.koszt, 2))
            self.tabela.insert("", "end", values=(
                w.pesel, w.imie, w.terapia, proc,
                w.telefon, notatki, koszt_tekst, w.status
            ), tags=(w.status,))
            suma = suma + w.koszt
            widoczne = widoczne + 1

        suma_tekst = str(round(suma, 2))
        self.etykieta_suma.config(text="Suma: " + suma_tekst + " zl")

        if self.okno_zbudowane == True:
            info = "Wszystkie: " + str(len(self.wizyty)) + " | Zakonczone: " + str(zakonczone) + " | Oczekujace: " + str(oczekujace) + " | Pokazane: " + str(widoczne)
            self.etykieta_info.config(text=info)

    def filtruj_wizyty(self, event=None):
        self.odswiez()

    # zaznaczanie wizyty jako zakonczonej
    def zakoncz_wizyte(self):
        wybrany = self.tabela.selection()
        if not wybrany:
            messagebox.showinfo("Błąd!", "Zaznacz wizyte na liscie!")
            return
        idx = self.tabela.index(wybrany)
        self.wizyty[idx].status = "Zakonczona"
        self.odswiez()
        self.zapisz()

    # usuwanie wizyty z listy
    def usun_wizyte(self):
        wybrany = self.tabela.selection()
        if not wybrany:
            messagebox.showinfo("Błąd", "Zaznacz wizyte na liscie!")
            return
        idx = self.tabela.index(wybrany)
        del self.wizyty[idx]
        self.odswiez()
        self.zapisz()

    # zapis do pliku json
    def zapisz(self):
        dane = []
        for i in range(len(self.wizyty)):
            w = self.wizyty[i]
            slownik = {}
            slownik["pesel"] = w.pesel
            slownik["imie"] = w.imie
            slownik["terapia"] = w.terapia
            slownik["telefon"] = w.telefon
            slownik["opis"] = w.opis
            slownik["koszt"] = w.koszt
            slownik["status"] = w.status
            dane.append(slownik)

        plik = open(self.plik, "w", encoding="utf-8")
        json.dump(dane, plik, indent=2, ensure_ascii=False)
        plik.close()

    # wczytanie danych z pliku json
    def wczytaj(self):
        if os.path.exists(self.plik) == False:
            return
        try:
            plik = open(self.plik, "r", encoding="utf-8")
            dane = json.load(plik)
            plik.close()

            for i in range(len(dane)):
                d = dane[i]

                # sprawdzam czy klucz istnieje, jak nie to daje pusty string
                if "pesel" in d:
                    pesel = d["pesel"]
                else:
                    pesel = ""

                if "imie" in d:
                    imie = d["imie"]
                else:
                    imie = ""

                if "terapia" in d:
                    terapia = d["terapia"]
                else:
                    terapia = ""

                if "telefon" in d:
                    telefon = d["telefon"]
                else:
                    telefon = ""

                if "opis" in d:
                    opis = d["opis"]
                else:
                    opis = ""

                if "koszt" in d:
                    koszt = d["koszt"]
                else:
                    koszt = 0.0

                if "status" in d:
                    status = d["status"]
                else:
                    status = "Oczekuje"

                w = Wizyta(pesel, imie, terapia, telefon, opis, koszt, status)
                self.wizyty.append(w)
        except:
            pass


# uruchomienie programu
if __name__ == "__main__":
    okno = tk.Tk()
    app = Aplikacja(okno)
    okno.mainloop()
