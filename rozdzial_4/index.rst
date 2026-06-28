===========================================================
Definiowanie bazy danych i wprowadzanie danych
===========================================================

Autor: Mateusz Gałecki

Definiowanie struktury bazy danych
-----------------------------------------

Na podstawie modeli fizycznych z rozdziału 3 przygotowałem skrypt pozwalający na utworzenie struktury tabel.

**PostgreSQL:**

.. code-block:: sql

   CREATE TABLE filmy (
       id_filmu SERIAL PRIMARY KEY,
       tytul VARCHAR(255) NOT NULL,
       rok_produkcji INT,
       czas_trwania INT NOT NULL
   );

   CREATE TABLE sale (
       id_sali SERIAL PRIMARY KEY,
       nazwa_sali VARCHAR(50) NOT NULL,
       pojemnosc INT NOT NULL
   );

   CREATE TABLE seanse (
       id_seansu SERIAL PRIMARY KEY,
       id_filmu INT REFERENCES filmy(id_filmu),
       id_sali INT REFERENCES sale(id_sali),
       czas_rozpoczecia TIMESTAMP NOT NULL
   );


**SQLite:**

.. code-block:: sql

   CREATE TABLE filmy (
       id_filmu INTEGER PRIMARY KEY AUTOINCREMENT,
       tytul TEXT NOT NULL,
       rok_produkcji INTEGER,
       czas_trwania INTEGER NOT NULL
   );

   CREATE TABLE sale (
       id_sali INTEGER PRIMARY KEY AUTOINCREMENT,
       nazwa_sali TEXT NOT NULL,
       pojemnosc INTEGER NOT NULL
   );

   CREATE TABLE seanse (
       id_seansu INTEGER PRIMARY KEY AUTOINCREMENT,
       id_filmu INTEGER REFERENCES filmy(id_filmu),
       id_sali INTEGER REFERENCES sale(id_sali),
       czas_rozpoczecia DATETIME NOT NULL
   );

Wybór mechanizmów wsadowego wprowadzania danych
-----------------------------------------------------

Gotowe tabele musiałem uzupełnić danymi. Brałem pod uwage następujące mechanizmy wsadowego wprowadzania danych:

* **PostgreSQL:** Środowisko to oferuje bardzo dobry import danych z plików CSV za pomocą polecenia "COPY". Jest to najszybsza metoda ale wymaga ona kontroli na formatem pliku wsadowego. Drugą opcją jest funkcja "INSERT" która pozwala na wprowadzenie wielu wierszy jednym zapytaniem.
* **SQLite:** W SQlite najbardziej znaną i zalecaną formą wprowadzania danych jest instrukcja "INSERT".

Zdecydowałem sie na stworzenie skryptu w pythonie który na podstawie prototypowych danych generuje zapytania wykorzystujące funkcje "INSERT". Dzięki temu wygenerowany plik pasuje do baz danych


Komentarz do procesu wprowadzania danych
---------------------------------------------

1. W pierwszej kolejności zapełnione zostały tabele "filmy" oraz "sale" aby wygenerować na nich klucze główne.
2. Później dane są wprowadzane do tabeli "seanse" aby nie wystąpiła sytuacja z naruszeniem klucza obcego.
