import os
import sys

sys.path.insert(0,os.path.abspath('.'))

project = 'Sprawozdanie'
copyright = '2026, Mateusz'
author = 'Mateusz'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode'
]

autodoc_mock_imports = ['psycopg2']

latex_engine = 'pdflatex'

latex_elements = {
    # Rozmiar strony i czcionka
    'papersize': 'a4paper',
    'pointsize': '12pt',
    
    'preamble': r'''
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
''',
    
    'extraclassoptions': 'openany,oneside',
}

latex_documents = [
    ('index', 'sprawozdanie_koncowe.tex', 'Sprawozdanie bazy danych',
     'Mateusz', 'manual'),
]

master_doc = 'index'
language = 'pl'
