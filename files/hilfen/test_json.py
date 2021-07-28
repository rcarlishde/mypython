"""
import json

with open("files/world.json") as file:
    data = json.load(file)

print(type(data), data)
print(len(data))
test = {}
test1={}
for i in range(0, len(data)):
    test[(data[i]['alpha2'])]=data[i]['name']
    test1[(data[i]['name'])]=data[i]['alpha2']

print("TEST= ", test1)
print(test1['Deutschland'])

# test1.get('search', 'errortext')
print("get=", test1.get('Deutschlan', "not found"))

dict = {
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
with(open('files/eu.json','w') as file):
    dict = json.dump(dict, file, ensure_ascii=False)
"""
import json
import requests


url = "https://nominatim.openstreetmap.org/search/{}?format=json&addressdetails=1".format("Neuss")
r = requests.get(url)
orte = r.json()

print(type(orte))
print("Orte: ", orte)
print(len(orte))
ort = orte[0]

print(type(ort), ort)

print("Adresse: ",ort['address'])
