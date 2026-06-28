import sqlite3
import psycopg2

def sqlite_pojemnosc_sal_dla_dlugich_filmow(db_path: str) -> list:
    """
    Pokazuje wszystkie sale w których filmy są dłuższe niż średni czas trwania wszystkich filmów
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
        SELECT s.nazwa_sali, SUM(s.pojemność) 
        FROM sale s 
        JOIN seanse se ON s.id_sali = se.id_sali 
        JOIN filmy f ON f.id_filmu = se.id_filmu 
        WHERE f.czas_trwania > (SELECT AVG(czas_trwania) FROM filmy) 
        GROUP BY s.nazwa_sali;
    """
    cursor.execute(query)
    wyniki = cursor.fetchall()
    conn.close()
    return wyniki

def sqlite_seanse_wielkie_litery(db_path: str) -> list:
    """
    Wyświetla wszystkie seanse po 2026 roku zmieniając tytuły na wielkie litery
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
        SELECT UPPER(f.tytuł), s.nazwa_sali, se.czas_rozpoczecia 
        FROM filmy f 
        JOIN seanse se ON f.id_filmu = se.id_filmu 
        JOIN sale s ON s.id_sali = se.id_sali 
        WHERE SUBSTR(se.czas_rozpoczecia, 1, 4) = '2026';
    """
    cursor.execute(query)
    wyniki = cursor.fetchall()
    conn.close()
    return wyniki

def sqlite_filmy_archiwalne_i_premium(db_path: str) -> list:
    """
    Pokazuje liste filmów które został zrobione przed 2000 rokiem oraz były wyświetlane w sali o pojemności większej niż 100
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
        SELECT tytuł FROM filmy WHERE rok_produkcji < 2000 
        UNION 
        SELECT f.tytuł FROM filmy f 
        JOIN seanse se ON f.id_filmu = se.id_filmu 
        JOIN sale s ON s.id_sali = se.id_sali 
        WHERE s.pojemność > 100;
    """
    cursor.execute(query)
    wyniki = cursor.fetchall()
    conn.close()
    return wyniki

def sqlite_raport_popularnosci_filmow(db_path: str) -> list:
    """
    Tworzy raport zawierający tytuł, liczcbę seansów i największą sale w której był pokazany
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
        SELECT f.tytuł, COUNT(se.id_seansu) AS liczba_seansow, IFNULL(MAX(s.pojemność), 0) 
        FROM filmy f 
        LEFT JOIN seanse se ON f.id_filmu = se.id_filmu 
        LEFT JOIN sale s ON se.id_sali = s.id_sali 
        GROUP BY f.tytuł;
    """
    cursor.execute(query)
    wyniki = cursor.fetchall()
    conn.close()
    return wyniki

def sqlite_puste_sale(db_path: str) -> list:
    """
    Pokazuje w jakich salach nie odbył się żaden seans
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = """
        SELECT nazwa_sali FROM sale 
        EXCEPT 
        SELECT s.nazwa_sali FROM sale s 
        JOIN seanse se ON s.id_sali = se.id_sali;
    """
    cursor.execute(query)
    wyniki = cursor.fetchall()
    conn.close()
    return wyniki

def _get_pg_connection(conn_params: dict):
    """
    Tworzy połączenie z bazą
    """
    return psycopg2.connect(**conn_params)

def pg_zaawansowane_zestawienie_filmow(conn_params: dict) -> list:
    """
    Wyświetla tutuł, liczbę seansów, średnią pojemnośc sal w którch był wyświetlany oraz pokazuje tylko filmy z przynajmniej jednym seansem
    """
    conn = _get_pg_connection(conn_params)
    cursor = conn.cursor()
    query = """
        SELECT f.tytuł, COALESCE(COUNT(se.id_seansu), 0), ROUND(AVG(s.pojemność), 2) 
        FROM filmy f 
        LEFT JOIN seanse se ON f.id_filmu = se.id_filmu 
        LEFT JOIN sale s ON s.id_sali = se.id_sali 
        GROUP BY f.tytuł 
        HAVING COUNT(se.id_seansu) > 0;
    """
    cursor.execute(query)
    wyniki = cursor.fetchall()
    conn.close()
    return wyniki

def pg_najnowsze_filmy_w_malych_salach(conn_params: dict) -> list:
    """
    Pokazuje najnowsze filmy które są grane w salach mających mniej niż 50 miejsc
    """
    conn = _get_pg_connection(conn_params)
    cursor = conn.cursor()
    query = """
        SELECT f.tytuł, s.nazwa_sali 
        FROM filmy f 
        JOIN seanse se ON f.id_filmu = se.id_filmu 
        JOIN sale s ON s.id_sali = se.id_sali 
        WHERE f.rok_produkcji = (SELECT MAX(rok_produkcji) FROM filmy) 
        AND s.pojemność < 50;
    """
    cursor.execute(query)
    wyniki = cursor.fetchall()
    conn.close()
    return wyniki

def pg_kategoryzacja_filmow(conn_params: dict) -> list:
    """
    Daje każdemu filmowi kategorie powyżej i poniżej 120 minut i pokazuje w jakiej sali był seans
    """
    conn = _get_pg_connection(conn_params)
    cursor = conn.cursor()
    query = """
        SELECT f.tytuł, 
               CASE WHEN f.czas_trwania > 120 THEN 'Długi' ELSE 'Krótki' END as kategoria, 
               s.nazwa_sali 
        FROM filmy f 
        JOIN seanse se ON f.id_filmu = se.id_filmu 
        JOIN sale s ON s.id_sali = se.id_sali;
    """
    cursor.execute(query)
    wyniki = cursor.fetchall()
    conn.close()
    return wyniki

def pg_wspolne_seanse_intersect(conn_params: dict) -> list:
    """
    Pokazuje seanse w którch film trwa ponad 150 minut oraz filmy zrobione przed 2005 rokiem
    """
    conn = _get_pg_connection(conn_params)
    cursor = conn.cursor()
    query = """
        SELECT s.nazwa_sali FROM sale s 
        JOIN seanse se ON s.id_sali = se.id_sali 
        JOIN filmy f ON f.id_filmu = se.id_filmu WHERE f.czas_trwania > 150
        INTERSECT
        SELECT s.nazwa_sali FROM sale s 
        JOIN seanse se ON s.id_sali = se.id_sali 
        JOIN filmy f ON f.id_filmu = se.id_filmu WHERE f.rok_produkcji < 2005;
    """
    cursor.execute(query)
    wyniki = cursor.fetchall()
    conn.close()
    return wyniki

def pg_szczegoly_najdluzszego_filmu(conn_params: dict) -> list:
    """
    Pokazuje informacje o filmach którch czas trwania jest większy niż globalna średnia innych filmów
    """
    conn = _get_pg_connection(conn_params)
    cursor = conn.cursor()
    query = """
        SELECT f.tytuł, f.czas_trwania, s.nazwa_sali, s.pojemność 
        FROM filmy f 
        JOIN seanse se ON f.id_filmu = se.id_filmu 
        JOIN sale s ON s.id_sali = se.id_sali 
        WHERE f.czas_trwania > (SELECT AVG(czas_trwania) FROM filmy) 
        ORDER BY s.pojemność DESC;
    """
    cursor.execute(query)
    wyniki = cursor.fetchall()
    conn.close()
    return wyniki