# JSON aus String einlesen
import json

str_daten = """
{
    "ID": 1,
    "Vorname": "Max",
    "Nmane": "Mustermann",
    "Telefon": {
        "Mobil": "+49 123 4546 78",
        "Festnetz": "+49 987 654 32"
        }
}
"""

# Originalstring ausgeben
print("Originalstring:")
print(type(str_daten), str_daten)

# String im JSON Format (Dictionary) lesen + anzeigen
print("Daten mit json.loads eingelesen:")
python_daten = json.loads(str_daten)
print(type(python_daten), python_daten)
print("Nur die selektierte Mobilnr. ausgeben:")
print(python_daten["Telefon"]["Mobil"])
print()

# Json-Daten als String auf der Konsole ausgeben:
print("Json-Daten mit json.dumps als String ausgeben:")
json_dump = json.dumps(python_daten)
print(type(json_dump), json_dump)
print("Nur die selektierte Festnetznummer ausgeben:")
json_dump = json.dumps(python_daten['Telefon']['Festnetz'])
print(type(json_dump), json_dump)
print()

# Json-Daten als formatierten String auf der Konsole ausgeben
print("Json-Daten mit json.dumps als String formatiert auf Konsole ausgeben")
json_dump = json.dumps(python_daten, indent=4)
print(type(json_dump), json_dump)
print("\nNur das Objekt Telefon formatiert ausgeben:")
json_dump = json.dumps(python_daten['Telefon'], indent=4)
print(type(json_dump), json_dump)
print("\n\n")
print(30*'+', "\n")

# Json aus Datei lesen
print("Daten aus Json-Datei in eine Liste lesen:")
with open('data.json','r') as json_data:
    print(type(json_data), json_data)
    python_liste = json.load(json_data)     # Daten von Datei in Liste lesen
    print(type(python_liste), python_liste)
print("\nDie ganze Liste (Dict) des 2. Eintrags ausgeben:")
print(type(python_liste[1]), python_liste)
print("Nur den Vornamen des 2. Eintrags ausgeben:")
print(python_liste[1]['Vorname'])
print("\n\n")
print(30*'+', "\n")

# Daten in Json-Datei speichern
print("Daten aus Liste in Json-Datei speichern:")
with open('data_ziel.json', 'w') as json_ziel:
    json.dump(python_liste[1], json_ziel, indent=4)
