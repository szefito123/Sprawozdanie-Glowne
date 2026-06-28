============================
Zapytania do bazy danych
============================


Stworzyłem funkcje w języku python obsługujące zapytania Postgres i SQLite

Lokalizacja
------------
* **Testowany Katalog:** Plik był testowany na serwerze Jupyterhub '/home/student08' oraz Postgres 'student08db1/student08@postgres'
* **Link do repozytorium:** Plik nazywa się "zapytania_kino.py"

Opis funkcji
-------------

Przygotowałem po 5 zapytań dla każdej bazy danych

1. **Selekcja danych i funkcje wierszowe:** Wykorzystano funkcje ``UPPER()`` oraz ``SUBSTR()`` w SQLite do transformacji tekstu i dat oraz``CASE WHEN`` w PostgreSQL do sprawdzania długości filmów.
2. **Funkcje agregujące:** Zastosowano operacje ``SUM()``, ``COUNT()``, ``MAX()`` oraz ``AVG()`` połączone ``GROUP BY`` oraz ``HAVING``.
3. **Połączenia:** Wykorzystano (``INNER JOIN``) do relacji między trzema tabelami (filmy, sale, seanse) oraz złączenia lewostronne (``LEFT JOIN``) wraz z funkcjami obsługi wartości pustych (``IFNULL()`` / ``COALESCE()``) do uwzględnienia rekordów pustych.
4. **Operatory zbiorowe:** Użyłem ``UNION``, ``EXCEPT`` oraz ``INTERSECT`` do filtrowania sal i repertuaru.
5. **Podzapytania:** Wprowadzono podzapytania skorelowane i nieskorelowane do porównywanie czasu trwania filmów ze średnią ``SELECT AVG()``. 


Dokumentacja kodu
--------------------

Dokumentacja jest generowana automatycznie na podstaiwe komentarzy przez rozszerzenie Sphinx

.. automodule:: zapytania_kino
   :members:
   :undoc-members:
   :show-inheritance:
