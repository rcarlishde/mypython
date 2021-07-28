# Programm erstellt die Datei eu.json neu, falls sie verloren gegangen ist
import json
# Daten der EU-Staaten
eu = {
    'Belgien': 'be',
    'Bulgarien': 'bg',
    'Dänemark': 'dk',
    'Deutschland': 'de',
    'Estland': 'ee',
    'Finnland': 'fi',
    'Frankreich': 'fr',
    'Griechenland': 'gr',
    'Irland': 'ie',
    'Italien': 'it',
    'Kroatien': 'hr',
    'Lettland': 'lv',
    'Litauen': 'lt',
    'Luxemburg': 'lu',
    'Malta': 'mt',
    'Niederlande': 'nl',
    'Österreich': 'at',
    'Polen': 'pl',
    'Portugal': 'pt',
    'Rumänien': 'ro',
    'Slowakei': 'sk',
    'Slowenien': 'si',
    'Schweden': 'se',
    'Tschechien': 'cz',
    'Ungarn': 'hu',
    'Zypern': 'cy'
}

# Datei eu.json neu anlegen

with open('../eu.json', 'w') as datei:
    # ensure_ascii=False ==> stellt sicher, dass Umlaute erhalten bleiben
    json.dump(eu, datei, ensure_ascii=False, indent=4)        # Daten in die Datei speichern

print("Erledigt")
