=============================
Bezpieczeństwo
=============================

:Autor: Mateusz

Wstęp teoretyczny
=======================
Bezpieczeństwo danych jest jednym z kluczowych aspektów zarządzania systemami baz danych. Obejmuje ono ochronę przed nieuprawnionym dostępem, złośliwą modyfikacją lub utratą informacji, a także zapewnienie poufności, integralności i ciągłej dostępności usług. W zależności od wybranej architektury systemu, mechanizmy bezpieczeństwa mogą być wbudowane bezpośrednio w silnik bazy danych lub w całości delegowane do systemu operacyjnego oraz aplikacji klienckiej.

W niniejszym podrozdziale dokonano szczegółowej analizy porównawczej mechanizmów bezpieczeństwa zaimplementowanych w sieciowym systemie **PostgreSQL** oraz wbudowanym silniku bazodanowym **SQLite**.

Uwierzytelnianie i Kontrola Dostępu
=====================================

PostgreSQL
-----------
PostgreSQL oferuje wysoce elastyczny podsystem uwierzytelniania, którego konfiguracja opiera się na pliku ``pg_hba.conf`` (Host-Based Authentication). Pozwala on na precyzyjne określenie, jaki użytkownik, z jakiego adresu IP i do jakiej bazy danych może się zalogować. System wspiera liczne zaawansowane metody weryfikacji tożsamości:

* **SCRAM-SHA-256**: Nowoczesny i bezpieczny domyślny mechanizm oparty na protokole wyzwanie-odpowiedź, uniemożliwiający podsłuchanie haseł.
* **Uwierzytelnianie zewnętrzne**: Integracja z korporacyjnymi systemami zarządzania tożsamością, takimi jak LDAP, Kerberos, GSSAPI, PAM czy RADIUS.
* **Certyfikaty SSL**: Możliwość uwierzytelniania klientów wyłącznie na podstawie ważnych certyfikatów kryptograficznych x509.

SQLite
------------
W przeciwieństwie do systemów typu klient-serwer, SQLite nie posiada wbudowanego mechanizmu uwierzytelniania użytkowników. Wynika to bezpośrednio z jego architektury, gdzie baza danych jest po prostu pojedynczym plikiem na dysku.

* Kontrola dostępu do danych jest całkowicie zależna od uprawnień systemu operacyjnego.
* Każdy proces lub użytkownik systemu operacyjnego, który posiada uprawnienia systemowe do odczytu i zapisu pliku bazy danych, ma automatycznie pełny dostęp do wszystkich danych i struktur w niej zawartych.
* Istnieje oficjalne, opcjonalne rozszerzenie SQLite User Authentication, jednak nie jest ono częścią standardowej dystrybucji i zaprzecza podstawowej idei prostoty tego silnika.

Autoryzacja i Uprawnienia
===========================

PostgreSQL
---------------
Autoryzacja w PostgreSQL realizowana jest poprzez model kontroli dostępu oparty na rolach (RBAC – *Role-Based Access Control*). Za pomocą instrukcji ``GRANT`` i ``REVOKE`` administratorzy mogą szczegółowo definiować prawa:

* **Granularność uprawnień**: Uprawnienia mogą być nadawane na poziomie całych baz danych, schematów, tabel, widoków, a także konkretnych kolumn.
* **Row-Level Security (RLS)**: Zaawansowany mechanizm polityk bezpieczeństwa, który filtruje zwracane wiersze w zależności od tożsamości zalogowanego użytkownika.

SQLite
----------
Standardowy silnik SQLite nie obsługuje pojęcia ról ani wewnętrznych uprawnień.

* Po pomyślnym otwarciu pliku bazy danych, programista lub użytkownik może wykonać każdą operację (``SELECT``, ``INSERT``, ``DROP TABLE``).
* Jedyną formą ograniczenia uprawnień jest otwarcie bazy danych przez aplikację w trybie tylko do odczytu, użycie flagi wewnętrznej ``SQLITE_OPEN_READONLY`` podczas inicjalizacji połączenia w kodzie źródłowym.

Szyfrowanie Danych
===================

PostgreSQL
-------------
PostgreSQL zapewnia ochronę danych zarówno w trakcie ich przesyłania, jak i podczas przechowywania na nośnikach:

* **Szyfrowanie w locie (Data-in-Transit)**: Pełne i natywne wsparcie dla protokołu SSL/TLS, co zapobiega podsłuchiwaniu ruchu sieciowego między aplikacją a serwerem bazy danych.
* **Szyfrowanie w spoczynku (Data-at-Rest)**: Standardowa wersja PostgreSQL nie posiada wbudowanego mechanizmu przezroczystego szyfrowania bazy danych (TDE). Bezpieczeństwo na dysku realizuje się za pomocą narzędzi systemowych lub poprzez wbudowane rozszerzenie ``pgcrypto``, pozwalające na szyfrowanie konkretnych wartości w kolumnach za pomocą algorytmu AES.

SQLite
----------
Ponieważ cała baza danych SQLite mieści się w jednym pliku, fizyczne skopiowanie tego pliku oznacza kradzież wszystkich danych. Szyfrowanie staje się więc kluczowe:

* **Brak szyfrowania w standardzie**: Domyślnie pliki bazy danych są zapisywane jawnym tekstem.
* **Szyfrowanie za pomocą rozszerzeń**: Aby zabezpieczyć bazę, stosuje się zewnętrzne biblioteki modyfikujące warstwę VFS (Virtual File System). Najpopularniejszym, otwartoźródłowym rozwiązaniem jest **SQLCipher** szyfrujący plik algorytmem AES-256 oraz oficjalne, komercyjne rozszerzenie **SEE** (*SQLite Encryption Extension*).

Audyt i Logowanie
==================

PostgreSQL
------------
System udostępnia zaawansowane mechanizmy śledzenia i rejestrowania operacji. Konfiguracja pozwala na logowanie błędów, prób uwierzytelnienia, a także pełnych zapytań SQL. W środowiskach wymagających rygorystycznego audytu stosuje się rozszerzenie **pgaudit**, które tworzy szczegółowe dzienniki zdarzeń zawierające informacje o tym, kto, kiedy i jakie dokładnie dane modyfikował lub przeglądał.

SQLite
----------
SQLite nie generuje własnych plików dziennika zdarzeń przeznaczonych do audytu bezpieczeństwa. Śledzenie aktywności musi zostać zaimplementowane w kodzie aplikacji klienckiej przy użyciu funkcji API udostępnianych przez bibliotekę SQLite, takich jak mechanizmy przechwytujące zapytania: ``sqlite3_trace_v2()`` lub filtry autoryzacyjne ``sqlite3_set_authorizer()``.

Podsumowanie
===============
Podsumowując, podejście do bezpieczeństwa w systemach DBMS zależy w głównej mierze od ich założeń architektonicznych. PostgreSQL, jako zaawansowany system typu klient-serwer, oferuje kompleksowy i scentralizowany zestaw narzędzi bezpieczeństwa na poziomie silnika. Dzięki separacji procesów, zaawansowanej kontroli dostępu oraz natywnej obsłudze szyfrowania sieciowego, stanowi on optymalne rozwiązanie dla środowisk wielodostępnych i rozproszonych. 

Z kolei SQLite jest minimalny i prosty. Jako bezserwerowy silnik osadzony, w całości deleguje zadania związane z uwierzytelnianiem i autoryzacją użytkowników do systemu operacyjnego lub samej aplikacji klienckiej. Bezpieczeństwo danych sprowadza się tu do ochrony fizycznego pliku bazy danych na dysku, a wdrożenie bardziej zaawansowanych mechanizmów, takich jak kryptograficzna ochrona danych w spoczynku, wymaga implementacji zewnętrznych nakładek programistycznych.