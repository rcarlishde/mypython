#!/usr/bin/python
"""
********************************
* Dateiname: einstellungen.py  *
*   Version: 2.2               *
*     Stand: 26.07.2021        *
*     Autor: Richard Carl      *
********************************

WETTERBERICHT
Programm zur Darstellung des aktuellen Wetters an einem beliebigen Ort auf der Erde

Wetter:
Darstellung der Wetterdaten für 5 Tage, aufgeteilt in Morgen, Mittag, Abend, Nacht

Quellen:
Die Koordinaten der Orte werden mit Hilfe von OpenStreetMap ermittelt. (Format Json)
Die Wetterdaten werden vom Meteorologisk Institutt (Norwegen) heruntergeladen. (Form Json)
Die Icons stammen ebenfalls von dort (liegen als png-Dateien vor: /images/)
"""

# Imports
# #######
import tkinter as tk  # GUI starten
from tkinter import *
from tkinter import messagebox  # MessageBoxen
import tkinter.ttk as ttk  # Tabs für die GUI
import tkinter.font as tkFont  # Schriften selbst definieren
import requests  # ermöglicht das Einlesen von Daten via API
import datetime  # Datums- und Zeitberechnung
# from datetime import time
# import json                     # Daten im Format JSON verarbeiten
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# eigene Module
from icons import *  # Liste der Wettericons erstellen und speichern


# Farben bzw. Themes definieren
# -----------------------------
# Vorbereitung für eine Steuerung der Farben
# Standardwerte:
std_color = '#d9d9d9'  # Hintergrundfarbe aller Elemente
std_text_col = 'black'  # Schriftfarbe aller Elemente
std_white = 'white'  # Hintergrund der Tooltipps

# Alle Hintergrundfarben
col_lab_kopf = std_color  # Logo im Hauptfenster
col_gui_wetter = std_color  # Hauptfenster
col_lab_kopf123 = std_color  # Labels der Überschriften im Hauptfenster
col_f1 = std_color  # die einzelnen Seiten des Notebooks
col_f2 = std_color
col_f3 = std_color
col_f4 = std_color
col_btn_schliessen = std_color  # Button Schließen
col_tab = std_color  # die TABs im Notebook
col_tooltip_bg = std_white  # Tooltipps
col_ueber = std_white  # Überschriften in Vorhersage
col_cell = std_color  # alle Zellen der Vorhersage
col_cell_logo = std_color  # Logo-Hintergrund in allen Zellen der Vorhersage
col_alarm = std_color  # Alarmmeldung
col_alarm_icon = std_color  # Alarm-Icon
col_detail_ort = std_color  # TAB Detail Ortsdaten
col_detail_astro = std_color  # TAB Detail Astrologische Daten
col_detail_meteor = std_color  # TAB Detail Meteorologische Daten

# Alle Schriftfarben
col_text_kopf123 = std_text_col  # im Kopf der Hauptseite
col_text_tabs = std_text_col  # in den Tabs
col_text_schliessen = std_text_col  # Button Schließen
col_tooltip_txt = std_text_col  # Tooltipps
col_ueber_txt = std_text_col  # Überschriften in Vorhersage
col_cell_txt = std_text_col  # Texte in allen Zellen der Vorhersage
col_alarm_txt = std_text_col  # Alarmtext
col_detail_ort_txt = std_text_col  # TAB Detail Text Ortsdaten
col_detail_astro_txt = std_text_col  # TAB Detail Text Astrologische Daten
col_detail_meteor_txt = std_text_col  # TAB Detail Text Meteorologische Daten


# Funktionen #
# ########## #

# Funktionen auf Basis DATETIME
# #----------------------------

def akt_zeit():
    now = datetime.datetime.now()
    nowtime = now.strftime('%H:%M:%S')
    return nowtime


def akt_datum(now=datetime.datetime.now()):
    nowdate = now.strftime('%d.%m.%Y')
    return nowdate


def akt_tag(now, deltaTimezone=7200):
    # Berechnet den Wochentag
    # now = 0 -> Heute, sonst wird ein TimeStamp zu übergeben
    if now == 0:
        now = datetime.datetime.now()
    else:
        now = now - deltaTimezone
        now = datetime.datetime.fromtimestamp(now)
    dayno = int(now.strftime('%w'))
    wtag = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch',
            'Donnerstag', 'Freitag', 'Samstag']
    tag = wtag[dayno]
    return tag


def akt_monat(typ='l'):
    # typ = 'l' -> langer Monatsname (standard)
    # typ = 'k' -> kurzer Monatsname
    now = datetime.datetime.now()
    monthno = int(now.strftime('%m'))
    lmonatliste = ['', 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
                   'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember']
    kmonatliste = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
    if typ == 'l':
        monat = lmonatliste[monthno]
    else:
        monat = kmonatliste[monthno]
    return monat


def tstamp_to_date(time_stamp, t_zone=7200):
    # time_stamp    =   timestamp
    # t_zone        =   Zeitzone, für Neuss = 7200
    date = datetime.datetime.fromtimestamp(time_stamp - t_zone)
    return date


def tick():
    # liest je Sekunde die aktuelle Zeit und das aktuelle Datum
    # neu ein und aktualisiert die Anzeige
    neuesdatum = akt_datum()
    neuezeit = akt_zeit()
    lab_kopf_3.config(text=neuesdatum + '   ' + neuezeit)
    lab_kopf_3.after(1000, tick)


# Funktionen zur Umrechnung von Einheiten
# ---------------------------------------
def plus_unit(wert, unit):
    # Umrechnen der relativen Luftfeuchte passend zu den eingestellten Einheiten
    # Basis ist %
    wert = "{:.0f}".format(wert)
    return wert + " " + unit


def umrechnen_druck(druck, unitDruck, numeral=False):
    # Umrechnen des Luftdrucks passend zu den eingestellten Einheiten
    # Basis ist hPa

    if unitDruck == 'mmHG':
        druck = druck * 0.75006375541921
    druck = "{:.2f}".format(druck)
    if numeral is False:
        return druck + " " + unitDruck
    else:
        return float(druck)


def umrechnen_temp(temp, unitTemp, numeral=False):
    # Umrechnen der Temperaturwerte passend zu den eingestellten Einheiten
    # numeral   = True => Wert als float, False => als String mit Einheit
    # Basis ist °Kelvin
    if unitTemp == '°C':
        temp = temp - 273.15
    elif unitTemp == '°F':
        temp = ((temp - 273.15) * 9 / 5) + 32
    temp = round(temp, 1)
    temp = "{:.1f}".format(temp)
    if numeral is False:
        return str(temp) + " " + unitTemp
    else:
        return float(temp)


def umrechnen_wind(wind, unitWind):
    # Umrechnen der Windstärke passend zu den eingestellten Einheiten
    # Basis ist m/s
    if unitWind == 'Windstärken 0-12':
        unitWind = ''
    if unitWind == 'km/h':
        wind = wind * 3.6
        wind = "{:.1f}".format(wind)
    elif unitWind == '':
        if wind < 0.3:
            wind = '0 (Windstille)'
        elif 0.3 <= wind < 1.6:
            wind = '1 (leiser Zug)'
        elif 1.6 <= wind < 3.4:
            wind = '2 (leichte Brise)'
        elif 3.4 <= wind < 5.5:
            wind = '3 (schwache Brise)'
        elif 5.5 <= wind < 8.0:
            wind = '4 (mäßige Brise)'
        elif 8.0 <= wind < 10.8:
            wind = '5 (frische Brise)'
        elif 10.8 <= wind < 13.9:
            wind = '6 (starker Wind)'
        elif 13.9 <= wind < 17.2:
            wind = '7 (steifer Wind)'
        elif 17.2 <= wind < 20.8:
            wind = '8 (stürmischer Wind)'
        elif 20.8 <= wind < 24.5:
            wind = '9 (Sturm)'
        elif 24.5 <= wind < 28.5:
            wind = '10 (schwerer Sturm)'
        elif 28.5 <= wind < 32.7:
            wind = '11 (orkanartiger Sturm)'
        elif wind >= 32.7:
            wind = '12 (Orkan)'
    return str(wind) + " " + unitWind


def umrechnen_windrichtung(winkel):
    # Umrechnen des Winkels in Himmelsrichtung
    richtung = ['N', 'NNO', 'NO', 'ONO',
                'O', 'OSO', 'SO', 'SSO',
                'S', 'SSW', 'SW', 'WSW',
                'W', 'WNW', 'NW', 'NNW']
    index = round(((winkel % 360) / 360) * 16) % 16
    result = str(winkel) + "° ⇒ " + richtung[index]
    return result


# Funktionen allgemeiner Art
# --------------------------

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


def alerts(daten_onecall):
    # Alarme anzeigen, sofern vorhanden
    #
    # Variablen:
    # ort   = Daten über den aktuell ausgewählten Ort
    # alarm = Text der Alarmmeldung (Unwetteralarm)
    # start = Startdatum und Startzeit des Alarms
    # ende  = Enddatum und Endzeit des Alarms

    # Prüfen, ob eine Alarmmeldung vorliegt
    if 'alerts' in daten_onecall.keys():
        daten = daten_onecall['alerts']  # Alarmdaten selektieren
        # Alarmtexte zusammenstellen
        alarm = "Alarmquelle\t\t: " + daten['sender_name'] + '\n'
        # Timestamps für Alarmstart und -ende auf deutsches Format bringen
        alarmstart = tstamp_to_date(daten['start'])

        start = alarmstart.strftime('%d%m.%Y um %H:%M Uhr\n')
        alarmende = tstamp_to_date(daten['end'])
        ende = alarmende.strftime('%d.%m.%Y um %H:%M Uhr\n')
        alarm += "Start des Alarms\t\t: " + start
        alarm += "Ende des Alarms\t\t: " + ende
        alarm += "Meldung\t\t:" + daten['description']
        # Alarm-Icon anzeigen
        photo = tk.PhotoImage(file=icon_path + "Icon_Unwetter.png")
        lab_image = tk.Label(gui_wetter, image=photo,
                             borderwidth=2, relief='groove', bg=col_alarm_icon)
        lab_image.photo = photo  # Fehlerkorrektur der Grafik
        lab_image.place(x=10, y=970)

        # Alarmtext ausgeben
        lab_alert = tk.Label(gui_wetter,
                             text=alarm,
                             font=('Noto Sans', 11, 'italic'),
                             height=5, width=70,
                             bg=col_alarm, fg=col_alarm_txt)
        lab_alert['padx'] = 10
        lab_alert['pady'] = 10
        lab_alert.place(x=75, y=970)
    return


# --------------------------
def btn_schliessenclick():
    gui_wetter.quit()  # Programm beenden


def mond_phase(phase):
    # Erittelt aus der Angabe (0 bis 1) die Darstellung der Mondphase
    # Gibt den Dateinamen der passenden Mondphase zurück
    ptext = ''
    if phase == 0:
        phase = 1  # Anfang und Ende gleichstellen
    if phase < 0.25:
        ptext = "moon5.png"
    elif phase == 0.25:
        ptext = "moon6.png"
    elif 0.25 < phase < 0.50:
        ptext = "moon7.png"
    elif phase == 0.50:
        ptext = "moon0.png"
    elif 0.50 < phase < 0.75:
        ptext = "moon1.png"
    elif phase == 0.75:
        ptext = "moon2.png"
    elif 0.75 < phase < 1:
        ptext = "moon3.png"
    elif phase == 1:
        ptext = "moon4.png"
    return ptext


# Tooltipp (TAB Vorhersage)
# --------
def tooltipp_text(daten):
    # Tooltipps mit Text und Daten füllen
    #
    # Variablen:
    #   daten       = Übergabe der Werte von OpenWeatherMap
    #   einheiten   = Übergabe der vordefinierten Einheiten
    #   datum       = Datum auf deutsches Format umgerechnet
    #   text        = Texte für den Tooltipp = Rückgabewert
    #
    # Datum in deutsche Schreibweise überführen
    datum = daten['dt_txt'][0:10]
    datum = datum[8:] + "." + datum[5:7] + "." + datum[0:4]
    # Texte holen und formatieren
    text = "             STAND\n Daten gemeldet für: " + datum + "\n"
    text += "      berechnet für: " + daten['dt_txt'][11:16] + ' Uhr\n\n'
    text += "       TEMPERATUREN\n"
    text += "       ------------\n"
    text += "         Temperatur: " + daten['main']['temp'] + "\n"
    text += "         min. Temp.: " + daten['main']['temp_min'] + "\n"
    text += "         max. Temp.: " + daten['main']['temp_max'] + "\n"
    text += "     gefühlte Temp.: " + daten['main']['feels_like'] + "\n\n"
    text += "         ATMOSPHÄRE\n"
    text += "         ----------\n"
    text += "          Luftdruck: " + daten['main']['pressure'] + "\n"
    text += "   rel. Luftfeuchte: " + daten['main']['humidity'] + "\n"
    text += "Windgeschwindigkeit: " + daten['wind']['speed'] + "\n"
    text += "           Windböen: " + daten['wind']['gust'] + '\n'
    text += "   Windrichtung aus: " + daten['wind']['deg'] + "\n\n"
    text += "       NIEDERSCHLAG\n"
    text += "       ------------\n"
    text += "         Regenmenge: " + daten['rain']['3h'] + "\n"
    text += "             Schnee: " + daten['snow']['3h'] + "\n\n"
    text += "              WETTER\n"
    text += "              ------\n"
    text += "          Bewölkung: " + daten['clouds']['all'] + "\n"
    text += "          Kommentar: " + daten['weather'][0]['description'] + "\n"
    return text


# Datenbeschaffung
# ================

def get_Wetterdaten(lat, lon, typ="onecall"):
    # Wetterdaten holen von OpenWeatherMap, Standard = onecall
    #
    # Variablen:
    #   lat = Breitengrad
    #   lon = Längengrad
    #   typ = "onecall" oder "forecast"
    # Rückgabewert:
    #   daten = Alle Wetterdaten
    #
    # URL für onecall
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + \
          str(lat) + "&lon=" \
          + str(lon) + "&lang=de&exclude=minutely,hourly" \
                       "&appid=e9795e0ea062e5a6b848c34b35313cb8"
    # URL für forecast
    url53 = "https://api.openweathermap.org/data/2.5/forecast?lat=" + \
            str(lat) + "&lon=" + \
            str(lon) + "&lang=de&appid=e9795e0ea062e5a6b848c34b35313cb8"

    # debugging
    # print('URL = ', url)
    # print('URL53 = ', url53)

    # Daten lesen
    if typ == "onecall":
        r = requests.get(url)
    else:
        r = requests.get(url53)
    daten = r.json()
    return daten


def daten_selektieren(daten_forecast, einheiten):
    # Daten für die Anzeigematrix der Vorhersage aussuchen und aufbereiten
    #
    # Variablen:
    # ----------
    # Beim Aufruf:
    # daten_forecast= gesamte Daten von OpenWeatherMap forecast (OWM)
    # einheiten     = in Einstellungen definierte Einheiten aller Parameter
    #
    # daten         = Rohdaten nach einer ersten Reduktion
    # anz           = Zähler für die Datensätze
    # count         = Zähler für die gültigen Datensätze
    # cnt           = Gesamtzahl vorhandener Datensätze laut OWM
    # day_time      = Liste gültiger Zeiten (Datensatz wird angenommen)
    # day_time1     = Liste ungültiger Zeiten (Datensatz wird verworfen)
    # zeit          = aus timestamp ('dt') berechnete Zeit,
    #                 Basis zur Selektion der Datensätze
    #
    # Rückgabewert:
    # dat           = gültige Daten / Rückgabewerte der Funktion

    daten = daten_forecast['list']  # erste Datenreduzierung der Gesamtdaten
    dat = {}  # Dict zur Datenrückgabe
    cnt = daten_forecast['cnt']  # Gesamtzahl vorhandener Datensätze
    count = 0  # Zähler für die gültigen Daten
    day_time = ['03', '09', '15', '21']  # gültige Zeiten
    day_time1 = ['06', '12', '18', '00']  # ungültige Zeiten

    for anz in range(0, cnt):
        # aktuelle Zeit aus den Daten holen
        zeit = daten[anz]['dt_txt']
        zeit = zeit[-8:-6]

        # Alle Spalten sind für feste Zeiten vorgesehen --> day_time.
        # Um den ersten Datensatz passend zur aktuellen Zeit in die richtige Spalte zu
        # platzieren, werden genügend leere Datensätze für die vorherigen Spalten
        # generiert.
        if anz == 0:
            # Anzahl leerer Datensätze berechnen
            if zeit in day_time:
                ctr = day_time.index(zeit)  # für gültige Zeiten (3,9,15,21)
            else:
                ctr = day_time1.index(zeit)  # für ungültige Zeiten (6,12,18,0)
            # leere Datensätze generieren
            for y in range(0, ctr):
                dat.update({count: {'main': {
                                         'temp': 'Temperatur',
                                         'feels_like': '',
                                         'temp_min': '',
                                         'temp_max': '',
                                         'pressure': '',
                                         'humidity': ''
                                         }}})
                dat[count].update({'weather': {0: {'description': 'Bewölkung',
                                                   'icon': 'unknown'}}})
                dat[count].update({'clouds': {'all': ''}})
                dat[count].update({'wind': {'speed': 'Windstärke', 'deg': '', 'gust': ''}})
                dat[count].update({'rain': {'3h': ''}})
                dat[count].update({'snow': {'3h': ''}})
                dat[count].update({'dt_txt': ''})
                dat[count].update({'dt': daten[anz]['dt']})
                count += 1  # Datensatzzähler +1

            # Liegt der ungültige Datensatz innerhalb von +3h, kann er ausgegeben werden
            status = False  # Ausgabe sperren
            if day_time1[ctr] == zeit:
                status = True  # Prüfen und freigeben

        # Gültige Datensätze generieren
        if zeit in day_time or status is True:
            status = False  # ungültigen Datensatzes nur einmal ausgeben, reset status

            # Nur die Datensätze mit passenden Zeiten (day_time) speichern
            dat.update({count:
                {'main': {
                    'temp': umrechnen_temp(daten[anz]['main']['temp'], einheiten['temp']),
                    'feels_like': umrechnen_temp(
                        daten[anz]['main']['feels_like'], einheiten['temp']),
                    'temp_min': umrechnen_temp(daten[anz]['main']['temp_min'], einheiten['temp']),
                    'temp_max': umrechnen_temp(daten[anz]['main']['temp_max'], einheiten['temp']),
                    'pressure': umrechnen_druck(daten[anz]['main']['pressure'], einheiten['druck']),
                    'humidity': plus_unit(daten[anz]['main']['humidity'], einheiten['feuchte'])}}})
            dat[count].update({'weather': {0: {
                               'description': daten[anz]['weather'][0]['description'],
                               'icon': daten[anz]['weather'][0]['icon']}}})
            dat[count].update({'clouds': {'all': plus_unit(daten[anz]['clouds']['all'],
                                                           einheiten['wolken'])}})
            dat[count].update({'wind': {
                'speed': umrechnen_wind(daten[anz]['wind']['speed'], einheiten['speed']),
                'deg': umrechnen_windrichtung(daten[anz]['wind']['deg']),
                'gust': umrechnen_wind(daten[anz]['wind']['gust'], einheiten['speed'])}})
            # Niederschläge werden nur angegeben, wenn sie auch vorhanden sind
            if 'rain' in daten[anz].keys():
                dat[count].update({'rain': {'3h': plus_unit(daten[anz]['rain']['3h'],
                                                            einheiten['regen'])}})
            else:
                dat[count].update({'rain': {'3h': plus_unit(0, einheiten['regen'])}})
            if 'snow' in daten[anz].keys():
                dat[count].update({'snow': {'3h': plus_unit(daten[anz]['snow']['3h'],
                                                            einheiten['regen'])}})
            else:
                dat[count].update({'snow': {'3h': plus_unit(0, einheiten['regen'])}})
            dat[count]['dt_txt'] = daten[anz]['dt_txt']
            dat[count]['dt'] = daten[anz]['dt']
            dat[count]['wochentag'] = akt_tag(daten[anz]['dt'])  # Wochentag berechnen
            count += 1
    return dat  # Rückgabe der vollständigen Anzeige der Vorhersage


# TABS der Wettervohersage füllen
# ===============================

# TAB Vorhersage füllen
# ---------------------
def tab_vorhersage(daten_forecast, einheiten, image_path):
    # Inhalt des TABs "Vorhersage" erstellen
    #
    # Variablen:
    # ort           = aktuelle Ortsdaten
    # dat_onecall   = komplette Wetterdaten von OpenWeatherMap typ=onecall
    #
    # Für jeweils 5 Tage:
    #   icon_id       = key für die Icons
    #   wolken        = Text zur Bewölkung bzw. Sicht auf den Himmel
    #   temperatur    = Temperaturen für Morgens, Mittags, Abends und Nachts
    #   windstaerke   = Windstärke
    #   datum         = Datum jedes angezeigten Tags
    #   wochentag     = Wochentag jedes angezeigten Tages
    #

    # Datenbeschaffung:
    # -----------------

    # Die Längen- und Breitengrad des aktuellen Orts aus Datei "orte.json" holen
    # ort = dateien('r', '', 'orte')

    # Koordinaten für die ToolTipps
    detailKoord = [[35, 300], [225, 300], [415, 300], [520, 300],
                   [35, 450], [225, 450], [415, 450], [520, 450],
                   [35, 600], [225, 600], [415, 600], [520, 600],
                   [35, 147], [225, 147], [415, 147], [520, 147],
                   [35, 290], [225, 290], [415, 290], [520, 290]]

    # Funktionen für Tooltipps
    # ------------------------
    #
    # Tooltipps einschalten bei Maus über Icon
    def detailOn(event, arg, detailKoord):
        # Variablen:
        # arg           = Nummer des aktuellen Logos in der Matrix
        # detailKoord   = Koordinaten für das Tooltippfenster
        #
        koord = detailKoord  # x,y Koordinaten für die Detailfenster
        detailInfo.place(x=koord[0], y=koord[1])
        tool_tipp = tooltipp_text(daten[arg])
        labelDetailInfo = tk.Label(detailInfo, text=tool_tipp, borderwidth=2,
                                   relief='groove', justify=LEFT,
                                   bg=col_tooltip_bg, fg=col_tooltip_txt,
                                   width=40, font=fontStyleHere)
        labelDetailInfo.grid(column=0, row=0)

    # Tooltipps ausschalten beim Verlassen der Icons
    def detailOff(event):
        detailInfo.place_forget()

    # Aus den Gesamtdaten nur die benötigten Datensätze auswählen
    daten = daten_selektieren(daten_forecast, einheiten)

    # Überschriften
    # -------------
    text_top = ('Nachts', 'Morgens', 'Mittags', 'Abends')
    # Bezeichnung der Zeilen
    text_left = ['Heute', 'Morgen']
    # Wochentage ermitteln
    for day in range(8, 17, 4):
        text_left.append(daten[day]['wochentag'])  # Wochentag

    # Obere Überschriften ausgeben
    for x in range(0, 4):
        c = Canvas(f1, width=186, height=22, bg=col_ueber)
        c.create_text(90, 10, text=text_top[x], fill=col_ueber_txt,
                      anchor='center', angle=0)
        c.grid(column=1 + x, row=0)
    # Linke Überschriften ausgeben
    for x in range(0, 5):
        c = Canvas(f1, width=20, height=150, bg=col_ueber)
        c.create_text(10, 75, text=text_left[x], fill=col_ueber_txt,
                      anchor='center', angle=90)
        c.grid(column=0, row=1 + x)

    # Alle Felder ausgeben
    # --------------------
    # Start-Koordinaten für Text und Bild je Feld
    x_text = 22  # Startkoordinate für x des ersten Textfeldes je Zeile
    y_text = 23  # Startkoordinate für y des ersten Textfeld je Spalte
    x_logo = 80  # Startkoordinate für x des ersten Icons je Zeile
    y_logo = 30  # Startkoordinate für y des ersten Icons je Spalte
    x_step = 188  # Addieren je Spalte
    y_step = 153  # Addieren je Zeile

    # Loop für die Tage
    for day in range(0, 5):  # Zeilenzähler
        # Loop für die Tageszeiten
        for day_time in range(0, 4):  # Spaltenzähler
            # Text anzeigen
            count = day * 4 + day_time  # Datensatzzähler

            # Texte für die Felder
            text1 = daten[count]['weather'][0]['description']  # Bewölkung
            text2 = daten[count]['main']['temp']  # Temperaturen
            text3 = daten[count]['wind']['speed']  # Windstärke
            text = text1 + '\n' + str(text2) + '\n' + str(text3) + "\n\n"
            # Textfelder platzieren und anzeigen
            lab = tk.Label(f1, text=text, width=27, height=9, borderwidth=2,
                           relief='groove', font=('Noto Sans', 9), anchor='s')
            lab['bg'] = col_cell
            lab['fg'] = col_cell_txt
            lab.place(x=x_text + day_time * x_step, y=y_text + day * y_step)

            # Icons ermitteln
            icon = PhotoImage(
                file=image_path + daten[count]['weather'][0]['icon'] + '.png')

            # Icon platziern und anzeigen
            lab_logo = Label(f1, image=icon, width=70, height=70, bg=col_cell_logo)
            lab_logo.photo = icon  # Fehlerkorrektur der Grafik
            lab_logo.place(x=x_logo + day_time * x_step, y=y_logo + day * y_step)

            # logo für die Steuerung von tooltipps einrichten
            arg = day * 4 + day_time
            lab_logo.bind('<Enter>', lambda event,
                          arg=arg: detailOn(event, arg, detailKoord[arg]))
            lab_logo.bind('<Leave>', detailOff)

    # Fenster für ToolTipps einrichten
    detailInfo = tk.Frame()
    fontStyleHere = tkFont.Font(family='Noto sans mono', size=9)

    # Alarm anzeigen
    alerts(dat_onecall)

    return


def tab_details(dat_onecall, daten_forecast, ort, einheiten, image_path):
    # Inhalt des TABs "Details" ermitteln und anzeigen
    #
    # Variablen:
    #   ort         =   Daten des aktuell ausgewählten Orts
    #   einheiten   =   eingestellte Einheiten aller Wetterparameter
    #   image_path  =   Pfad zu den Icons
    #   top_font    =   Font für die Überschriften
    #   text_font   =   Font für die Daten / Texte
    #   text        =   Liste der definierten Texte
    #   x           =   Zähler für die 3 Text-Fenster
    #   w_col       =   Farbe für die Hintergründe der Text-Fenster
    #   t_col       =   Textfarbe in den Text-Fenstern
    #   bild        =   Bilddatei für Icons, Flaggen, Mondphasen
    #   w_height    =   Höhe des jeweiligen Text-Fensters
    #   phasenbild  =   png-Datei für die Mondphasen
    #   icon_name   =   Dateiname des Wettericons
    #   box_text1   =   Überschrift jedes Textfensters
    #   box_text2   =   Text jedes Textfensters

    # Fonts für die Überschriften und Texte
    top_font = ('Noto Sans mono', 12, 'bold')  # Überschriften
    txt_font = ('Noto Sans mono', 10, 'normal')  # Texte

    text = []
    text.append('')
    # Texte für den TAB "Details" erstellen
    text1 = "ORTSDATEN\n"
    text2 = "             Name: " + daten_forecast['city']['name'] + "\n"
    text2 += "            Staat: " + ort['staat'] + ' ' + ort['sym'] + "\n\n"
    text2 += "KOORDINATEN:\n"
    text2 += "           Breite: " + ort['lat'] + '°\n'
    text2 += "            Länge: " + ort['lon'] + '°\n\n'
    text2 += "        Höhenlage: " + str(ort['hoehe']) + 'm über NN\n'
    text2 += "    Einwohnerzahl: " + str(daten_forecast['city']['population']) + '\n'
    text2 += "         Zeitzone: " + ort['zeitzone']

    text3 = "Astronomische Daten\n"
    text4 = "    Sonnenaufgang: " + str(tstamp_to_date(dat_onecall['current']
                                                       ['sunrise'], 0)) + '\n'
    text4 += "  Sonnenuntergang: " + str(tstamp_to_date(dat_onecall['current'][
                                                            'sunset'], 0)) + '\n\n'
    text4 += "      Mondaufgang: " + str(tstamp_to_date(dat_onecall['daily'][0][
                                                            'moonrise'], 0)) + '\n'
    text4 += "    Monduntergang: " + str(tstamp_to_date(dat_onecall['daily'][0][
                                                            'moonset'], 0)) + '\n\n'
    text4 += "        Mondphase: " + str(dat_onecall['daily'][0]['moon_phase'])

    text5 = "Weitere Meterologische Daten\n"
    text6 = "TEMTERATUREN: \n"
    text6 += "         Mittlere: " + umrechnen_temp(dat_onecall['current']['temp'],
                                                    einheiten['temp']) + '\n'
    text6 += "         Gefühlte: " + umrechnen_temp(dat_onecall['current']['feels_like'],
                                                    einheiten['temp']) + '\n'
    text6 += "          Minimal: " + umrechnen_temp(
        dat_onecall['daily'][0]['temp']['min'], einheiten['temp']) + '\n'
    text6 += "          Maximal: " + umrechnen_temp(
        dat_onecall['daily'][0]['temp']['max'], einheiten['temp']) + '\n'
    text6 += "         Taupunkt: " + umrechnen_temp(dat_onecall['current']['dew_point'],
                                                    einheiten['temp']) + '\n\n'
    text6 += "ATHMOSPHÄRE: \n"
    text6 += "   Windgeschwind.: " + umrechnen_wind(dat_onecall['current']['wind_speed'],
                                                    einheiten['speed']) + '\n'
    text6 += "     Aus Richtung: " + umrechnen_windrichtung(
        dat_onecall['current']['wind_deg']) + '\n'
    text6 += "        Luftdruck: " + umrechnen_druck(dat_onecall['current']['pressure'],
                                                     einheiten['druck']) + '\n'
    text6 += " Luftfeuchtigkeit: " + plus_unit(dat_onecall['current']['humidity'],
                                               '%') + '\n'
    text6 += "        Bewölkung: " + plus_unit(dat_onecall['current']['clouds'],
                                               '%') + '\n'
    text6 += "        Weitsicht: " + plus_unit(dat_onecall['current']['visibility'],
                                               'm') + '\n'
    text6 += "SonnenSchutz(UVI): " + plus_unit(dat_onecall['current']['uvi'], '') + '\n'

    text = [text1, text2, text3, text4, text5, text6]

    # obige Texte ausgeben
    w_height = 0
    w_col = std_color
    t_col = std_color
    for x in range(0, 6, 2):
        if x == 0:  # Ortsdaten
            w_height = 13
            w_col = col_detail_ort
            t_col = col_detail_ort_txt
            # Flagge anzeigen
            bild = tk.PhotoImage(file='files/flags/64x64/' + ort['sym'] + '.png')
            label_img = tk.Label(f2, image=bild)
            label_img.image = bild
            label_img.grid(column=2, row=x, padx=30, pady=30)
        elif x == 2:  # Astronomische Daten
            w_height = 10
            w_col = col_detail_astro
            t_col = col_detail_astro_txt
            # Bild zur aktuellen Mondphase
            phasenbild = mond_phase(dat_onecall['daily'][0]['moon_phase'])
            bild = tk.PhotoImage(file='files/mond/' + phasenbild)
            label_img = tk.Label(f2, image=bild, padx=30, pady=30)
            label_img.image = bild
            label_img.grid(column=2, row=x, padx=30, pady=30)
        elif x == 4:  # Weitere Meterologische Daten
            w_height = 20
            w_col = col_detail_meteor
            t_col = col_detail_meteor_txt
            # Wettericon holen
            icon_name = dat_onecall['current']['weather'][0]['icon'] + '.png'
            bild = tk.PhotoImage(file=image_path + icon_name)
            label_img = tk.Label(f2, image=bild, padx=30, pady=30)
            label_img.image = bild
            label_img.grid(column=2, row=x, padx=30, pady=30)
        # Texte zuordnen
        box_text1 = text[x]
        box_text2 = text[x + 1]
        # Textbox erstellen und anzeigen
        wordbox = Text(f2, wrap='word', width=60, height=w_height, padx=20, pady=10,
                       relief=RAISED, bg=w_col, fg=t_col)
        wordbox.grid(column=0, row=x, padx=15, pady=10)
        wordbox.insert('end', box_text1 + '\n')
        wordbox.insert('end', box_text2 + '\n')
        wordbox.configure(state='disabled')
        wordbox.tag_add('box_text1', 1.0, '1.end')
        wordbox.tag_config('box_text1', font=top_font)
        wordbox.tag_add('box_text2', 2.0, '2.end')
        wordbox.tag_config('box_text2', font=txt_font)
    return


def tab_diagramme(lat, lon, einheiten):
    # Erzeugung und Anzeige der Diagramme
    #
    # Themen der Diagramme:
    # ---------------------
    # Temperaturen
    #   Temperatur
    #   gefühlte Temp.
    #   min-max-Temp.
    # Luftdruck
    # Windstärke
    # Niederschlag (Regen/Schnee)
    # Luftfeuchte
    #
    # Zeitabschnitte der Diagramme:
    # -----------------------------
    # eine Stunde   - Interval Minuten      # nur Niederschläge (precipitation)
    # 48 Stunden    - Interval Stunden
    # eine Woche    - Interval Tage
    #
    diagram_type = StringVar()  # Variable für die Werte-Rückgabe der Radiobuttons
    #
    # Funktionen:
    # -----------

    def daten_lesen(lat, lon):
        # Vollständige Daten aus "onecall" lesen
        url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + \
              str(lat) + "&lon=" \
              + str(lon) + "&lang=de&appid=e9795e0ea062e5a6b848c34b35313cb8"
        r = requests.get(url)
        return r.json()

    def diagram_wahl():
        # Auswertung der Auswahl der Diagramme per Radiobutton
        #
        # Variablen:
        # wahl = String der Auswahl per Radiobutton
        # nsdaten   = Niederschlagsdaten aus dem Web
        # zeit_h    = Hilfsvariable zur Ermittlung aktuellen Zeit
        # zeit      = aktuelle Zeit als String
        # titel     = Titel des Plots
        # yWerte    = Niederschlagswerte
        # xWerte    = Minuten auf der x-Achse
        # zähler    = Anzahl der yWerte
        # index     = [einheit, yWerte[0], yWerte[][1], yWerte2[0], yWerte2[][1]]

        wahl = diagram_type.get()               # Auswahlstring lesen

        nsdaten = daten_lesen(lat, lon)         # Webdaten lesen
        xWerte, yWerte, yWerte2 = [], [], []    # x-y Listen init
        titel = ""                              # Diagrammtitel init
        xtitel, ytitel = "", ""                 # Titel der x- und Y-Achse
        leg1, leg2 = "", ""                     # Legendentext init
        leg = ['', '']
        einh = ""                               # Einheiten für Diagramm
        datenliste = []
        index = []

        # Startzeit des Grafen ermitteln
        zeit_h = datetime.datetime.fromtimestamp(nsdaten['hourly'][0]['dt'])
        # falls Minuten kleiner 10 eine führende 0 hinzufügen
        if zeit_h.minute < 10:
            zeit = str(zeit_h.hour) + ":0" + str(zeit_h.minute)
        else:
            zeit = str(zeit_h.hour) + ":" + str(zeit_h.minute)


        # Plot von Niederschlag in der nächsten Stunde
        if wahl == "niederschlag":
            titel = "Niederschlag in der nächsten Stunde   (Start um " + zeit + " Uhr)"
            ytitel = "Niederschläge in "
            xtitel = "Minuten"
            datenliste = nsdaten['minutely']
            index = ['regen', 'precipitation']
            datenstatus = 2

        # Plot von Temperaturen der nächsten 48h
        elif wahl == "temp48":
            titel = "Temperaturen der nächsten 48h (Start um " + zeit + " Uhr)"
            ytitel = "Temperaturen in "
            xtitel = "Stunden"
            datenliste = nsdaten['hourly']
            index = ['temp', 'temp']
            datenstatus = 1

        # Plot von gefühlten Temperaturen der nächsten 48h
        elif wahl == 'gtemp48':
            titel = "Gefühlte Temperaturen der nächsten 48h (Start um " + zeit + " Uhr)"
            ytitel = "Temperaturen in "
            xtitel = "Stunden"
            datenliste = nsdaten['hourly']
            index = ['temp', 'feels_like']
            datenstatus = 1

        # Plot vom Luftdruck der nächsten 48h
        elif wahl == "luft48":
            titel = "Luftdruck während der nächsten 48h (Start um " + zeit + " Uhr)"
            ytitel = "Luftdruck in "
            xtitel = "Stunden"
            datenliste = nsdaten['hourly']
            index = ['druck', 'pressure']
            datenstatus = 1

        # Plot von Luftfeuchte der nächsten 48h
        elif wahl == "luftf48":
            titel = "Luftfeuchte während der nächsten 48h (Start um " + zeit + " Uhr)"
            ytitel = "Luftfeuchte in "
            xtitel = "Stunden"
            datenliste = nsdaten['hourly']
            index = ['feuchte', 'humidity']
            datenstatus = 1

        # Plot der Windstärke der nächsten 48h
        elif wahl == "wind48":
            titel = "Windstärke während der nächsten 48h (Start um " + zeit + " Uhr)"
            ytitel = "Windstärke in "
            xtitel = "Stunden"
            datenliste = nsdaten['hourly']
            index = ['speed', 'wind_speed', '', 'wind_gust']
            leg = ['Windstärke', 'Windböen']
            datenstatus = 2

         # Plot der Niederschläge der nächsten 48h
        elif wahl == "nieder48":
            titel = "Niederschläge während der nächsten 48h (Start um " + zeit + " Uhr)"
            ytitel = "Niederschläge in "
            xtitel = "Stunden"
            zaehler = 0  # reset Datenzähler
            index = ['regen']                           # ??????????????????????
            leg = ['Regen', 'Schnee']
            datenstatus = 0
            for wert in nsdaten['hourly']:
                if 'rain' in wert:
                    yWerte.append(wert['rain']['1h'])
                else:
                    yWerte.append(0)
                if 'snow' in wert:
                    yWerte2.append(wert['snow']['1h'])
                else:
                    yWerte2.append(0)
                xWerte.append(zaehler)
                zaehler += 1
            einh = einheiten['regen']                   # ??????????????????????

        # Plot von Temperaturen der nächsten Woche
        elif wahl == "temp5":
            titel = "Temperaturen der nächsten Woche"
            ytitel = "Temperaturen in "
            xtitel = "Tage"
            datenliste = nsdaten['daily']
            index = ['temp', 'temp', 'day']
            datenstatus = 3

        # Plot von gefühlten Temperaturen der nächsten Woche
        elif wahl == "gtemp5":
            titel = "Gefühlte Temperaturen der nächsten Woche"
            ytitel = "Temperaturen in "
            xtitel = "Tage"
            datenliste = nsdaten['daily']
            index = ['temp', 'feels_like', 'day']
            datenstatus = 3

        # Plot von min-max Temperaturen der nächsten Woche
        elif wahl == "mmtemp5":
            titel = "Min-Max Temperaturen der nächsten Woche"
            ytitel = "Temperaturen in "
            xtitel = "Tage"
            datenliste = nsdaten['daily']
            index = ['temp', 'temp', 'min', 'temp', 'max']
            leg = ['min. Temp.', 'max. Temp']
            datenstatus = 4

        # Plot des Luftdrucks der nächsten Woche
        elif wahl == "luft5":
            titel = "Luftdruck während der nächsten Woche"
            ytitel = "Luftdruck in "
            xtitel = "Tage"
            datenliste = nsdaten['daily']
            index = ['druck', 'pressure']
            datenstatus = 1

        # Plot der Luftfeuchte der nächsten Woche
        elif wahl == "luftf5":
            titel = "Luftfeuchte während der nächsten Woche"
            ytitel = "Luftfeuchte in "
            xtitel = "Tage"
            datenliste = nsdaten['daily']
            index = ['feuchte', 'humidity']
            datenstatus = 1


        # Plot der Windstärke der nächsten Woche
        elif wahl == "wind5":
            titel = "Windstärke während der nächsten Woche"
            ytitel = "Windstärke in "
            xtitel = "Stunden"
            datenliste = nsdaten['daily']
            index = ['speed', 'wind_speed', 'wind_gust']
            leg = ['Windstärke', 'Windböen']
            datenstatus = 1


        # Plot der Niederschläge der nächsten Woche
        elif wahl == "nieder5":
            titel = "Niederschläge während der nächsten Woche"
            ytitel = "Niederschläge in "
            xtitel = "Tage"
            leg = ['Regen', 'Schnee']
            index = ['regen']
            datenstatus = 0

            zaehler = 0
            for wert in nsdaten['daily']:
                if 'rain' in wert:
                    yWerte.append(wert['rain'])
                else:
                    yWerte.append(0)
                if 'snow' in wert:
                    yWerte2.append(wert['snow'])
                else:
                    yWerte2.append(0)
                xWerte.append(zaehler)
                zaehler += 1

        einh = einheiten[index[0]]
        zaehler = 0

        # yWerte + yWerte2 mit umrechnen
        if datenstatus == 1:
            for wert in datenliste:
                yWerte.append(umrechnen_temp(wert[index[1]], einheiten[index[0]], True))
                if len(index) > 3:
                    yWerte2.append(umrechnen_temp(wert[index[3]], einheiten[index[0]], True))
                xWerte.append(zaehler)
                zaehler += 1

        elif datenstatus == 2:
            for wert in datenliste:
                yWerte.append(wert[index[1]])
                if len(index) > 3:
                    yWerte2.append(wert[index[3]])
                xWerte.append(zaehler)
                zaehler += 1

        elif datenstatus == 3:
            for wert in datenliste:
                yWerte.append(wert[index[1]][index[2]])
                if len(index) > 3:
                    yWerte2.append(wert[index[3]])
                xWerte.append(zaehler)
                zaehler += 1

        elif datenstatus == 4:
            for wert in datenliste:
                yWerte.append(umrechnen_temp(wert[index[1]][index[2]],
                                            einheiten[index[0]], True))
                if len(index) > 3:
                    yWerte2.append(umrechnen_temp(wert[index[3]][index[4]],
                                    einheiten[index[0]], True))
                xWerte.append(zaehler)
                zaehler += 1

        diagramm_show(titel, xtitel, ytitel + einh, xWerte, yWerte, leg[0], yWerte2,
                      leg[1])
        return

    def diagramm_show(text_Titel, text_xAchse, text_yAchse, xWerte,
                      yWerte1=None, leg1="", yWerte2=None, leg2=''):
        # Stellt einen Plot bzw. ein Diagramm dar
        # Es können 1 oder 2 Kurven gleichzeitig dargestellt werden
        #
        # Variablen:
        # text_Titel    = Titel über dem Diagramm
        # text_xAchse   = Beschriftung der X-Achse
        # text_yAchse   = Beschriftung der Y-Achse
        # xWerte        = Werte und Aufteilung der X-Achse
        # yWerte1       = Werte und Aufteilung der y-Achse Gruppe1
        # yWerte2       = Werte und Aufteilung der y-Achse Gruppe2
        # leg1          = Bezeichnung der Gruppe 1 in der Legende
        # leg2          = Bezeichnung der Gruppe 2 in der Legende
        #
        plt.close("all")                                # vorhandene Plots schließen
        plt.clf()
        plt.rcParams["figure.figsize"] = (7.4, 6)       # Größe des Plots
        figTemp = plt.figure()
        canvas = FigureCanvasTkAgg(figTemp, master=f3)  # TAB Diagramme auswählen
        canvas.get_tk_widget().place(x=15, y=20)        # Position des Plots im TAB
        # Beschriftung der Achsen und des Plotfensters
        plt.title(text_Titel)
        plt.ylabel(text_yAchse)
        plt.xlabel(text_xAchse)
        plt.grid(True)                      # Gitternetz ein
        # Plot ausgeben
        if leg1 == "h":                         # gilt nur für Niederschlag 1 Stunde
            plt.plot(xWerte, yWerte1, color='b', linestyle='-')
        else:
            if len(yWerte1) != 0:               # Ausgabe des 1.Grafen
                plt.plot(xWerte, yWerte1, color='b', linestyle='-', marker='.', label=leg1)
            if len(yWerte2) != 0:               # Ausgabe des 2.Grafen
                plt.plot(xWerte, yWerte2, color='m', linestyle='--', marker='.', label=leg2)
            if len(yWerte1) != 0 and len(yWerte2) != 0:   # Legende nur bei 2 Grafen
                plt.legend(loc='best')          # Position der Legende autom. festlegen
        return

    # Radiobutton für die Diagrammauswahl einrichten
    size = 10                           # Schriftgröße
    width = 11                          # Breite der Buttons

    # Beschriftung des Bereichs für die Radiobuttons (RB)
    yzeile0 = 630           # y-Position der Überschrift
    yzeile1 = 665           # y-Position der Zeile 1 der RBs
    yzeile2 = 695           # y-Position der Zeile 2 der RBs
    tk.Label(f3, text="Intervalle:", font=(font_name, 12, 'bold'),
             width=width).place(x=0, y=yzeile0)
    tk.Label(f3, text="48 Stunden:", font=(font_name, size),
             width=width, anchor=E).place(x=10, y=yzeile1)
    tk.Label(f3, text="5 Tage:", font=(font_name, size), width=width,
             anchor=E).place(x=10, y=yzeile2)

    # Liste der Radiobutton-Parameter
    # rbp = [text, value, width, x-koord, ykoord]
    rbp = [["Niederschlag in der nächsten Stunde", "niederschlag", 37, 110, 725],
           ["Temperatur", "temp48", 11, 110, yzeile1],
           ["Temperatur", "temp5", 11, 110, yzeile2],
           ["gef. Temp.", "gtemp48", 11, 203, yzeile1],
           ["gef. Temp.", "gtemp5", 11, 203, yzeile2],
           #["min-max Temp.", "mmtemp58", 14, 296, yzeile1],
           ["min-max Temp.", "mmtemp5", 14, 296, yzeile2],
           ["Luftdruck", "luft48", 10, 413, yzeile1],
           ["Luftdruck", "luft5", 10, 413, yzeile2],
           ["Luftfeuchte", "luftf48", 11, 498, yzeile1],
           ["Luftfeuchte", "luftf5", 11, 498, yzeile2],
           ["Wind", "wind48", 6, 591, yzeile1],
           ["Wind", "wind5", 6, 591, yzeile2],
           ["Niederschlag", "nieder48", 13, 645, yzeile1],
           ["Niederschlag", "nieder5", 13, 645, yzeile2]]

    # Radiobuttons für die Diagrammauswahl einrichten + platzieren
    for x in range(0, len(rbp)):
        Radiobutton(f3, text=rbp[x][0], value=rbp[x][1], indicatoron=0, font=(font_name, size),
                    width=rbp[x][2], height=1, variable=diagram_type,
                    command=diagram_wahl).place(x=rbp[x][3], y=rbp[x][4])
    diagram_type.set("niederschlag")
    diagram_wahl()
    return


# Start Hauptprogramm
# ###################

# Fonts für den Fensterkopf definieren
# ------------------------------------

# Fonts definieren
daten = {}
daten = dateien('r', daten, 'aussehen')
font_name = daten['name_font']
font_size = daten['name_size']
iconset = daten['name_iconset']
font_wb = "bold"  # Schrift - fett

# Fixwerte definieren
bg_col = 'white'  # Hintergrundfarbe für Überschriften der Vorhersage
datei_path = 'files/'  # Pfad zu den Einstelldaten
# Pfad zum zutreffenden Iconset definieren
if iconset == "Iconsatz 1":
    icon_path = datei_path + 'icons1/'  # Pfad zu den Icons
elif iconset == "Iconsatz 2":
    icon_path = datei_path + 'icons2/'  # Pfad zu den Icons
else:
    icon_path = datei_path + 'icons/'  # Pfad zu den Icons
# fixe Fensterparameter
frame_width = 860  # Fensterbreite
frame_height = 1110  # Fensterhöhe
frame_ypos = 50  # Leistenabstand

# Datenbeschaffung
# ----------------
# Ortsdaten lesen
orte = dateien('r', '', 'orte')
# print('Ort:\n', ort)          #debugging

# Einheiten einlesen
einheiten = {}
einheiten = dateien('r', einheiten, 'einheiten')

# Die Wetterdaten des aktuellen Orts von OpenWeatherMap einlesen
dat_forecast = get_Wetterdaten(orte['lat'], orte['lon'], 'forecast')
dat_onecall = get_Wetterdaten(orte['lat'], orte['lon'])

# Hauptfenster erstellen
# ======================

gui_wetter = tk.Tk()  # Fenster aktivieren
gui_wetter['bg'] = col_gui_wetter  # Hintergrundfarbe des Hauptfensters

# eigenes Logo für das Hauptfenster festlegen
logo = tk.PhotoImage(file=icon_path + "fair_day.png")
gui_wetter.tk.call('wm', 'iconphoto', gui_wetter._w, logo)

# Bildschirmgröße und seine Position ermitteln
# --------------------------------------------
screen_width = gui_wetter.winfo_screenwidth()  # Breite des verwendeten Bildschirms
frame_xpos = screen_width - frame_width  # Parameter für Rechtsbündigkeit berechnen
# Hinweis: use width x height + x_offset + y_offset (no spaces!)
gui_wetter.geometry("%dx%d+%d+%d" % (frame_width, frame_height, frame_xpos, frame_ypos))

# Überschriften fürs Hauptfenster
# -------------------------------
gui_wetter.title('Wettervorhersage')  # Kopfzeile des Fensters

fontStyle = tkFont.Font(family=font_name, size=font_size)  # Font für Button auf TABs
ttk.Style().configure(".", font=(font_name, font_size, font_wb))  # Font für die Tabs
# Standard-Fonts anpassen
default_font = tkFont.nametofont("TkTextFont")
default_font.configure(family=font_name, size=font_size)
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(family=font_name, size=font_size)

# Logo anzeigen
lab_kopf = tk.Label(gui_wetter, image=logo, borderwidth=2, relief='groove', bg=col_lab_kopf)
# Ortsnamen holen und verkürzen
# ort = dateien('r', '', 'orte')              # Ortsdaten aus Datei 'orte.json' holen
ort = orte['name']  # beschränken auf den Ortsnamen
ort_index = 0
for x in range(0, 3):
    ort_index = ort.find(',', ort_index) + 1  # 3 x finden eines Kommas im String
ort = ort[:ort_index - 1]  # Verkürzen des Ortsnamens für Überschrift

# Überschriften ausgeben
lab_kopf_1 = tk.Label(gui_wetter, text="Wettervorhersage", font=(font_name, 18, font_wb),
                      bg=col_lab_kopf123, fg=col_text_kopf123)
lab_kopf_2 = tk.Label(gui_wetter, text=ort, font=(font_name, 14, font_wb),
                      bg=col_lab_kopf123, fg=col_text_kopf123)
kopf_zeit = akt_zeit()
lab_kopf_3 = tk.Label(gui_wetter, text=kopf_zeit, font=(font_name, 10),
                      bg=col_lab_kopf123, fg=col_text_kopf123)

# Logo und Überschriften im Kopf positionieren
lab_kopf.place(x=50, y=20)
lab_kopf_1.place(x=200, y=25)
lab_kopf_2.place(x=200, y=65)
lab_kopf_3.place(x=200, y=100)

# TABS einrichten
# ---------------
nb = ttk.Notebook(gui_wetter)
nb.place(x=10, y=150)  # Startposition der Tabs

f1 = tk.Frame(bg=col_f1)
f2 = tk.Frame(bg=col_f2)
f3 = tk.Frame(bg=col_f3)
f4 = tk.Frame(bg=col_f4)

# TABs beschriften
nb.add(f1, text=' Vorhersage ')
nb.add(f2, text=' Details ')
nb.add(f3, text=' Diagramme ')
nb.add(f4, text=' Infos ')

# Start des Hauptprogramms
# ========================

# Button zum Beenden des Programms (Schließen)
btn_schliessen = tk.Button(gui_wetter, text='Schließen', command=btn_schliessenclick)
btn_schliessen.place(x=685, y=970)
btn_schliessen['bg'] = col_btn_schliessen
btn_schliessen['fg'] = col_text_schliessen

# TAB Vorhersage füllen
tab_vorhersage(dat_forecast, einheiten, icon_path)

# TAB Details füllen
tab_details(dat_onecall, dat_forecast, orte, einheiten, icon_path)

# TAB Diagramme füllen
tab_diagramme(orte['lat'], orte['lon'], einheiten)

tick()  # Uhr Ticker
gui_wetter.mainloop()
