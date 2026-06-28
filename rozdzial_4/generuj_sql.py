import csv

PLIK_WEJSCIOWY = 'filmy.csv'
PLIK_WYJSCIOWY = 'import_filmy.sql'


def generuj_zapytania_insert(plik_csv, plik_sql):
    with open(plik_csv, mode='r', encoding='utf-8') as plik:
        czytnik = csv.DictReader(plik)
        dane_wierszy = []

        for wiersz in czytnik:
            tytul = wiersz['tytul']
            rok = wiersz['rok_produkcji']
            czas = wiersz['czas_trwania']
            wartosci = f"('{tytul.replace(\"'\", \"''\")}', {rok}, {czas})"
            dane_wierszy.append(wartosci)

    if not dane_wierszy:
        print("Plik CSV jest pusty lub niepoprawny!")
        return

    kod_sql = "INSERT INTO filmy (tytul, rok_produkcji, czas_trwania) VALUES\n"
    kod_sql += ",\n".join(dane_wierszy) + ";"

    with open(plik_sql, mode='w', encoding='utf-8') as plik_out:
        plik_out.write(kod_sql)

    print(f"Zakończono sukcesem! Wygenerowano plik: {plik_sql}")


if __name__ == "__main__":
    generuj_zapytania_insert(PLIK_WEJSCIOWY, PLIK_WYJSCIOWY)
