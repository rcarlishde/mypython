#!/usr/bin/python
"""
********************************
* Dateiname: icons.py          *
*   Version: 1.0               *
*     Stand: 25.05.2021        *
*     Autor: Richard Carl      *
********************************

Erstellt eine JSON-Datei mit der Liste der Wetter-Icons
mit Bezug auf Nummer in den Wetterdaten und Tageszeiten.

"""

# IconListe definieren:
# ---------------------
# Dictionary ist wie folgt aufgebaut:
# {ID:[aktuell, Morgen, Tag, Abend, Nacht],...}
# Hinweis:  "aktuell" muss immer angegeben sein, andere nicht.
#           In der Liste stehen immer die Iconnamen mit Endungen
#

import json                     # Daten im Format JSON verarbeiten

def icons():
    def dateien(mod, daten, filename):
        # Aufbereitung und speichern bzw. lesen aller Dateien im Format JSON
        #
        # Variablen:
        # mod           = 'r'=lesen, 'w'= schreiben
        # daten         = Daten aus der Datei (Dictionary)
        # filename      = Name der Datei die gesichert bzw. gelesen wird, ohne Dateiendung!
        # file          = filename mit Pfad
        # message_text  = Fehlermeldung, falls Datei nicht existent
        #

        file = 'files/' + filename + ".json"
        # print("File = " + file)                           # debugging
        message_text = "Die Datei " + filename + ".json existiert nicht oder ist leer!"
        #
        # Datei bearbeiten:
        # -----------------
        try:  # Dateien lesen bzw. schreiben
            if mod == "w":  # Daten schreiben
                with open(file, 'w') as datei:
                    json.dump(daten, datei, ensure_ascii=False, indent=4)
            else:  # Daten einlesen
                with open(file, 'r') as datei:
                    daten = json.load(datei)
        except FileNotFoundError:  # Im Fehlerfall Standardwerte schreiben
            messagebox.showinfo('Fehler', message_text, icon='error')
        return daten

    iconlist = {
        200: ['lightrainshowersandthunder_day.png',
              'lightrainshowersandthunder_day.png',
              'lightrainshowersandthunder_polartwilight.png',
              'lightrainshowersandthunder_night.png'],
        201: ['rainshowersandthunder_day.png',
              'rainshowersandthunder_day.png',
              'rainshowersandthunder_polartwilight.png',
              'rainshowersandthunder_night.png'],
        202: ['heavyrainshowersandthunder_day.png',
              'heavyrainshowersandthunder_day.png',
              'heavyrainshowersandthunder_polartwilight.png',
              'heavyrainshowersandthunder_night.png'],
        210: ['lightrainandthunder.png'],
        211: ['rainandthunder.png'],
        212: ['heavyrainandthunder.png'],
        221: ['heavyrainandthunder.png'],
        230: ['lightsnowandthunder.png'],
        231: ['heavysleetshowersandthunder_day.png',
              'heavysleetshowersandthunder_day.png',
              'heavysleetshowersandthunder_polartwilight.png',
              'heavysleetshowersandthunder_night.png'],
        232: ['heavysleetshowersandthunder_day.png',
              'heavysleetshowersandthunder_day.png',
              'heavysleetshowersandthunder_polartwilight.png',
              'heavysleetshowersandthunder_night.png'],
        300: ['lightrain.png'],
        301: ['lightrain.png'],
        302: ['lightrain.png'],
        310: ['lightrain.png'],
        311: ['lightrain.png'],
        312: ['lightrain.png'],
        313: ['heavysleet.png'],
        314: ['heavysleetshowers_day.png',
              'heavysleetshowers_day.png',
              'heavysleetshowers_polartwilight.png',
              'heavysleetshowers_night.png'],
        321: ['heavysleetshowers_day.png',
              'heavysleetshowers_day.png',
              'heavysleetshowers_polartwilight.png',
              'heavysleetshowers_night.png'],
        500: ['lightrainshowers_day.png',
              'lightrainshowers_day.png',
              'lightrainshowers_polartwilight.png',
              'lightrainshowers_night.png'],
        501: ['lightrainshowers_day.png',
              'lightrainshowers_day.png',
              'lightrainshowers_polartwilight.png',
              'lightrainshowers_night.png'],
        502: ['rainshowers_day.png',
              'rainshowers_day.png',
              'rainshowers_polartwilight.png',
              'rainshowers_night.png'],
        503: ['heavyrain.png'],
        504: ['heavyrain.png'],
        511: ['sleetandthunder.png'],
        520: ['lightrainshowers_day.png',
              'lightrainshowers_day.png',
              'lightrainshowers_polartwilight.png',
              'lightrainshowers_night.png'],
        521: ['rainshowers_day.png',
              'rainshowers_day.png',
              'rainshowers_polartwilight.png',
              'rainshowers_night.png'],
        522: ['heavyrainshowers_day.png',
              'heavyrainshowers_day.png',
              'heavyrainshowers_polartwilight.png',
              'heavyrainshowers_night.png'],
        531: ['rainshowers_day.png',
              'rainshowers_day.png',
              'rainshowers_polartwilight.png',
              'rainshowers_night.png'],
        600: ['lightsnow.png'],
        601: ['snow.png'],
        602: ['heavysnow.png'],
        611: ['sleet.png'],
        612: ['lightssleetshowersandthunder_day.png',
              'lightssleetshowersandthunder_day.png',
              'lightssleetshowersandthunder_polartwilight.png',
              'lightssleetshowersandthunder_night.png'],
        613: ['sleetshowers_day.png',
              'sleetshowers_day.png',
              'sleetshowers_polartwilight.png',
              'sleetshowers_night.png'],
        615: ['sleetshowers_day.png',
              'sleetshowers_day.png',
              'sleetshowers_polartwilight.png',
              'sleetshowers_night.png'],
        616: ['sleet.png'],
        620: ['lightsnowshowers_day.png',
              'lightsnowshowers_day.png',
              'lightsnowshowers_polartwilight.png',
              'lightsnowshowers_night.png'],
        621: ['snowshowers_day.png',
              'snowshowers_day.png',
              'snowshowers_polartwilight.png',
              'snowshowers_night.png'],
        622: ['heavysnowshowers_day.png',
              'heavysnowshowers_day.png',
              'heavysnowshowers_polartwilight.png',
              'heavysnowshowers_night.png'],
        701: ['fog.png'],
        711: ['fog.png'],
        721: ['fog.png'],
        731: ['fog.png'],
        741: ['fog.png'],
        751: ['fog.png'],
        761: ['fog.png'],
        771: ['fog.png'],
        781: ['fog.png'],
        791: ['fog.png'],
        800: ['clearsky_day.png',
              'clearsky_day.png',
              'clearsky_polartwilight.png',
              'clearsky_night.png'],
        801: ['fair_day.png',
              'fair_day.png',
              'fair_polartwilight.png',
              'fair_night.png'],
        802: ['fair_day.png',
              'fair_day.png',
              'fair_polartwilight.png',
              'fair_night.png'],
        803: ['partlycloudy_day.png',
              'partlycloudy_day.png',
              'partlycloudy_polartwilight.png',
              'partlycloudy_night.png'],
        804: ['cloudy.png']
    }

    # Daten speichern
    # ---------------
    #datei_path = 'files/'       # Pfad zu den Einstelldaten
    dateien('w',iconlist, 'iconliste')
    print('Fertig!!')