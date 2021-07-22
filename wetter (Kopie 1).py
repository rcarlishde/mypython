#!/usr/bin/python
"""
********************************
* Dateiname: einstellungen.py  *
*   Version: 2.1               *
*     Stand: 25.05.2021        *
*     Autor: Richard Carl      *
********************************

WETTERBERICHT
Programm zur Darstellung des aktuellen Wetters an einem beliebigen Ort auf der Erde

Wetter:
Darstellung der Wetterdaten für 5 Tage, aufgeteilt in Morgen, Mittag, Abend, Nacht

Quellen:
Die Koordinaten der Orte werden mit Hilfe von OpenStreetMap ermittelt. (Format Json)
Die Wetterdaten werden vom Meteorologisk Institutt (Norwegen) heruntergeladen. (Format Json)
Die Icons stammen ebenfalls von dort (liegen als png-Dateien vor: /images/)
"""


# Imports
# #######
import tkinter as tk            # GUI starten
from tkinter import *
from tkinter import messagebox  # MessageBoxen
import tkinter.ttk as ttk       # Tabs für die GUI
import tkinter.font as tkFont   # Schriften selbst definieren
import requests                 # ermöglicht das Einlesen von Daten via API
import datetime                 # Datums- und Zeitberechnung
import json                     # Daten im Format JSON verarbeiten
# eigene Module
from icons import *             # Liste der Wettericons erstellen und speichern


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
    wtag = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag']
    tag = wtag[dayno]
    return tag

def akt_monat(typ='l'):
    # typ = 'l' -> langer Monatsname (standard)
    # typ = 'k' -> kurzer Monatsname
    now = datetime.datetime.now()
    monthno = int(now.strftime('%m'))
    lmonatliste = ['', 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August', 'September', 'Oktober',
                   'November', 'Dezember']
    kmonatliste = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'Mai', 'Jun', 'Jul', 'Aug', 'Sep', 'Okt', 'Nov', 'Dez']
    if typ == 'l':
        monat = lmonatliste[monthno]
    else:
        monat = kmonatliste[monthno]
    return monat

def tstamp_to_date(time_stamp, t_zone=7200):
    # time_stamp    =   timestamp
    # t_zone        =   Zeitzone, für Neuss = 7200
    date = datetime.datetime.fromtimestamp(time_stamp-t_zone)
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

def umrechnen_temp(temp, unitTemp):
    # Umrechnen der Temperaturwerte passend zu den eingestellten Einheiten
    # Basis ist °Kelvin
    if unitTemp == '°C':
        temp = temp - 273.15
    elif unitTemp == '°F':
        temp = ((temp - 273.15)*9/5)+32
    temp = "{:.1f}".format(temp)
    return temp + " " + unitTemp

def umrechnen_wind(wind, unitWind):
    # Umrechnen der Windstärke passend zu den eingestellten Einheiten
    # Basis ist m/s
    if unitWind == 'Windstärken 0-12':
        unitWind = ''
    if unitWind == 'km/h':
        wind = wind*3.6
        wind = "{:.1f}".format(wind)
    elif unitWind == '':
        if wind < 0.3:
            wind = '0 (Windstille)'
        elif wind >=0.3 and wind < 1.6:
            wind = '1 (leiser Zug)'
        elif wind >=1.6 and wind < 3.4:
            wind = '2 (leichte Brise)'
        elif wind >= 3.4 and wind < 5.5:
            wind = '3 (schwache Brise)'
        elif wind >=5.5 and wind < 8.0:
            wind = '4 (mäßige Brise)'
        elif wind >=8.0 and wind < 10.8:
            wind = '5 (frische Brise)'
        elif wind >=10.8 and wind < 13.9:
            wind = '6 (starker Wind)'
        elif wind >=13.9 and wind < 17.2:
            wind = '7 (steifer Wind)'
        elif wind >=17.2 and wind < 20.8:
            wind = '8 (stürmischer Wind)'
        elif wind >=20.8 and wind < 24.5:
            wind = '9 (Sturm)'
        elif wind >=24.5 and wind < 28.5:
            wind = '10 (schwerer Sturm)'
        elif wind >=28.5 and wind < 32.7:
            wind = '11 (orkanartiger Sturm)'
        elif wind >=32.7:
            wind = '12 (Orkan)'
    return str(wind) + " " + unitWind



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

# Tooltipp
# --------
def tootipp_text(daten, einheiten):
    # Testfeld mit Text füllen (Versuch)

    print("TEST=", einheiten)

    text = "             STAND\nDaten gemeldet für: " + daten[10] + '\n\n'
    text += "       TEMPERATUREN\n"
    text += "       ------------\n"
    text += "         Temperatur: " + daten[0] + "\n"
    text += "         min. Temp.: " + daten[2] + "\n"
    text += "         max. Temp.: " + daten[3] + "\n"
    text += "     gefühlte Temp.: " + daten[1] + "\n\n"
    text += "         ATMOSPHÄRE\n"
    text += "         ----------\n"
    text += "          Luftdruck: " + str(daten[4]) + ' ' + einheiten['druck'] + "\n"
    text += "   rel. Luftfeuchte: " + str(daten[5]) + ' ' + einheiten['feuchte'] + "\n"
    text += "Windgeschwindigkeit: " + daten[6] + "\n"
    text += "   Windrichtung aus: " + str(daten[7]) + " °\n\n"
    text += "       NIEDERSCHLAG\n"
    text += "       ------------\n"
    text += "         Regenmenge: " + daten[8] + ' ' + einheiten['regen'] + "\n"
    text += "             Schnee: \n\n"
    text += "              WETTER\n"
    text += "              ------\n"
    text += "          Bewölkung: " + str(daten[9]) + ' ' + einheiten['wolken'] + "\n"
    text += "          Kommentar: " + daten[11] + "\n"
    return text

# ------------------------------------------------------------------------------



# Datenbeschaffung
# ================

def get_Wetterdaten(lat, lon, typ="onecall"):
    # Wetterdaten holen von OpenWeatherMap
    #   lat = Breitengrad
    #   lon = Längengrad
    #   typ = "onecall" oder "forecast"
    # Rückgabewert:
    #   daten = Alle Wetterdaten
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + \
          str(lat) + "&lon=" \
          + str(lon) + "&lang=de&appid=e9795e0ea062e5a6b848c34b35313cb8"
    url53 = "https://api.openweathermap.org/data/2.5/forecast?lat=" + \
            str(lat) + "&lon=" + \
            str(lon) + "&lang=de&appid=e9795e0ea062e5a6b848c34b35313cb8"
    if typ == "onecall":
        r = requests.get(url)
    else:
        r = requests.get(url53)
    daten = r.json()
    return daten

# TABS der Wettervohersage füllen
# ===============================

# TAB Vorhersage füllen
# ---------------------
def tab_vorhersage():
    # Inhalt des TABs "Vorhersage" erstellen
    #
    # Variablen:
    # ort           = aktuelle Ortsdaten
    # dat_onecall   = komplette Wetterdaten von OpenWeatherMap typ=onecall
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
    ort = dateien('r', '', 'orte')
    # Einheiten einlesen
    einheiten = {}
    einheiten = dateien('r', einheiten, 'einheiten')
    # Die Wetterdaten des aktuellen Orts von OpenWeatherMap via forecast einlesen
    dat_forecast = get_Wetterdaten(ort['lat'], ort['lon'],'forecast')
    # print("Forecast =\n", dat_forecast)       # debugging

    # Pfad zu den Icons
    image_path = 'files/icons/'

    # Koordinaten für die ToolTipps
    detailKoord = [[35, 300], [225, 300], [415, 300], [520, 300],
                   [35, 450], [225, 450], [415, 450], [520, 450],
                   [35, 600], [225, 600], [415, 600], [520, 600],
                   [35, 177], [225, 177], [415, 177], [520, 177],
                   [35, 330], [225, 330], [415, 330], [520, 330]]





    # Funktionen für Tooltipps
    def detailOn(event, arg, detailKoord):
        # Variablen:
        # arg           = Nummer des aktuellen Logos in der Matrix
        # detailKoord   = Koordinaten für das Tooltippfenster
        #

        koord = detailKoord  # x,y Koordinaten für die Detailfenster
        detailInfo.place(x=koord[0], y=koord[1])
        tool_tipp = tootipp_text(dat_tooltip[arg], einheiten)
        labelDetailInfo = tk.Label(detailInfo, text=tool_tipp, borderwidth=2, relief='groove', justify=LEFT,
                                   bg='white', width=40, font=fontStyleHere)

        labelDetailInfo.grid(column=0, row=0)
        print('NrOn\n', koord[0], koord[1])  # debugging

    def detailOff(event):
        detailInfo.place_forget()
        print('NrOff')  # debugging

    # Reduzierung der Wetterdaten "forecast" auf die benötigten Parameter
    iconid, wolken, temp, windstaerke, f_zeit, wochentag, timestamp = {}, {}, {}, {}, {}, {}, {}
    feels, temp_min, temp_max, druck, feuchte, winddeg, regen, bewoelkung, stand = {}, {}, {}, {}, {}, {}, {}, {}, {}

    cnt = dat_forecast['cnt']               # Anzahl vorhandener Datensätze
    count = 0                               # Reset Zähler der zutreffenden Daten
    day_time = ['06', '12', '18', '00']
    day_time1 = ['03', '09', '15', '21']
    dat_tooltip = {}                        # Daten für die Tooltipps dict anlegen

    for anzahl in range(0, cnt):
        # aktuelle Zeit aus den Daten holen
        zeit = dat_forecast['list'][anzahl]['dt_txt']
        zeit = zeit[-8:-6]

        if anzahl != 0:
            if zeit in day_time:
                # Nur die Daten mit passenden Zeiten (day_time) speichern
                iconid[count] = dat_forecast['list'][anzahl]['weather'][0]['icon']
                wolken[count] = dat_forecast['list'][anzahl]['weather'][0]['description']
                temp[count] = dat_forecast['list'][anzahl]['main']['temp']
                temp[count] = umrechnen_temp(temp[count], einheiten['temp'])                    # Einheit umrechnen
                windstaerke[count] = dat_forecast['list'][anzahl]['wind']['speed']
                windstaerke[count] = umrechnen_wind(windstaerke[count], einheiten['speed'])     # Einheit umrechnen
                timestamp[count] = dat_forecast['list'][anzahl]['dt']
                if zeit =='00':      # Korrektur des Wochentages bei Datum um 0:00 Uhr
                    wochentag[count] = akt_tag(timestamp[count]-10)
                else:
                    wochentag[count] = akt_tag(timestamp[count])
                f_zeit[count] = zeit

                # Daten für die Tooltipps
                feels[count] = dat_forecast['list'][anzahl]['main']['feels_like']
                feels[count] = umrechnen_temp(feels[count], einheiten['temp'])                  # Einheit umrechnen
                temp_min[count] = dat_forecast['list'][anzahl]['main']['temp_min']
                temp_min[count] = umrechnen_temp(temp_min[count], einheiten['temp'])            # Einheit umrechnen
                temp_max[count] = dat_forecast['list'][anzahl]['main']['temp_max']
                temp_max[count] = umrechnen_temp(temp_max[count], einheiten['temp'])            # Einheit umrechnen
                druck[count] = dat_forecast['list'][anzahl]['main']['pressure']
                feuchte[count] = dat_forecast['list'][anzahl]['main']['humidity']
                winddeg[count] = dat_forecast['list'][anzahl]['wind']['deg']
                if 'rain' in dat_forecast['list'][anzahl].keys():
                    regen[count] = dat_forecast['list'][anzahl]['rain']['3h']
                else:
                    regen[count] = '0'
                bewoelkung[count] = dat_forecast['list'][anzahl]['clouds']['all']
                stand[count] = dat_forecast['list'][anzahl]['dt_txt']
                dat_tooltip[count] = [temp[count], feels[count], temp_min[count], temp_max[count], druck[count], \
                                     feuchte[count], windstaerke[count], winddeg[count], regen[count],
                                     bewoelkung[count], stand[count], wolken[count]]
                count += 1
        else:
            # Felder vor der aktuellen Zeit mit Standardinhalt füllen (Leer)
            # Anzahl einzufügender Leerfelder berechnen
            if zeit in day_time:
                ctr = day_time.index(zeit)  # für gültige Zeiten (6,12,18,0)
            else:
                ctr = day_time1.index(zeit) # für ungültige Zeiten (3,9,15,21)
            # Leerfelder einrichten
            for y in range(0, ctr):
                iconid[count] = 'unknown'
                wolken[count] = 'Bewölkung'
                temp[count] = 'Temperatur'
                windstaerke[count] = 'Windstärke'
                timestamp[count] = 0
                wochentag[count] = ''
                f_zeit[count] = '0'

                # Daten für die Tooltipps
                feels[count] = ''
                temp_min[count] = ''
                temp_max[count] = ''
                druck[count] = ''
                feuchte[count] = ''
                winddeg[count] = ''
                regen[count] = '0'
                bewoelkung[count] = ''
                stand[count] = ''
                dat_tooltip[count] = [temp[count], feels[count], temp_min[count], temp_max[count], druck[count], \
                                     feuchte[count], windstaerke[count], winddeg[count], regen[count],
                                     bewoelkung[count], stand[count], wolken[count]]
                count +=1

    # debugging für forecast
    # print("F_Iconid=", iconid)
    # print("F_Wolken=", wolken)
    # print("F_Temperatur = ", temp)
    # print("F_Windstärke=", windstaerke)
    # print("F_Datum = ", datum)
    # print('F_Zeit=', f_zeit)
    # print("F_Wochentag = ", wochentag)

    # Überschriften
    # -------------
    text_top = ('Morgens', 'Mittags', 'Abends', 'Nachts')
    text_left = ['Heute', 'Morgen']
    for day in range(11,22, 4):
        text_left.append(wochentag[day])
    # Obere Überschriften
    for x in range(0,4):
        c = Canvas(f1, width=186, height=22, bg='white')
        c.create_text(90, 10, text=text_top[x], fill='black', anchor='center', angle=0)
        c.grid(column=1+x, row=0)
    # Linke Überschriften
    for x in range(0,5):
        c = Canvas(f1, width=20, height=150, bg='white')
        c.create_text(10, 75, text=text_left[x], fill='black', anchor='center', angle=90)
        c.grid(column=0, row=1+x)

    # Alle Felder ausgeben
    # --------------------
    # Start-Koordinaten für Text und Bild je Feld
    x_text = 22     # Startkoordinate für x des ersten Textfeldes je Zeile
    y_text = 23     # Startkoordinate für y des ersten Textfeld je Spalte
    x_logo = 80     # Startkoordinate für x des ersten Icons je Zeile
    y_logo = 30     # Startkoordinate für y des ersten Icons je Spalte
    x_step = 188    # Addieren je Spalte
    y_step = 153    # Addieren je Zeile

    # Loop für die Tage (Zeilenzähler)
    for day in range(0, 5):
        # Loop für die Tageszeiten (Spaltenzähler)
        for day_time in range(0, 4):
            # Text anzeigen
            text1 = wolken[day*4 + day_time]          # Bewölkung
            text2 = temp[day*4 + day_time]            # Temperaturen
            text3 = windstaerke[day*4 + day_time]     # Windstärke
            text = text1 + '\n' + str(text2) + '\n' + str(text3) + "\n\n"
            lab = tk.Label(f1, text=text, width=27, height=9, borderwidth=2, relief='groove', font=('Noto Sans', 9), anchor='s')
            lab.place(x=x_text+day_time*x_step, y=y_text+day*y_step)
            # icon ermitteln
            icon = PhotoImage(file=image_path + iconid[day * 4 + day_time] + '.png')
            # Icon anzeigen
            lab_logo = Label(f1, image=icon, width=70, height=70)
            lab_logo.photo = icon
            lab_logo.place(x=x_logo+day_time*x_step, y=y_logo+day*y_step)

            # logo für tooltipp einrichten
            arg = day*4+day_time
            lab_logo.bind('<Enter>', lambda event, arg = arg: detailOn(event, arg, detailKoord[arg]))
            lab_logo.bind('<Leave>', detailOff)


    # Fenster für ToolTipps einrichten
    detailInfo = tk.Frame()
    fontStyleHere = tkFont.Font(family='Noto sans mono', size=9)



    return















# Start Hauptprogramm
# ###################
#
# Fixwerte definieren
bg_col     = 'white'            # Hintergrundfarbe für Überschriften der Vorhersage
icon_path  = 'files/icons/'     # Pfad zu den Icons
datei_path = 'files/'           # Pfad zu den Einstelldaten

# fixe Fensterparameter
frame_width = 860               # Fensterbreite
frame_height = 1110             # Fensterhöhe
frame_ypos = 50                 # Leistenabstand


# Hauptfenster erstellen
# ======================

gui_wetter = tk.Tk()                            # Fenster aktivieren

# eigenes Logo für das Hauptfenster festlegen
logo = tk.PhotoImage(file=icon_path + "fair_day.png")
gui_wetter.tk.call('wm', 'iconphoto', gui_wetter._w, logo)

# Bildschirmgröße und seine Position ermitteln
# --------------------------------------------
screen_width = gui_wetter.winfo_screenwidth()   # Breite des verwendeten Bildschirms
frame_xpos = screen_width-frame_width           # Parameter für Rechtsbündigkeit berechnen
# Hinweis: use width x height + x_offset + y_offset (no spaces!)
gui_wetter.geometry("%dx%d+%d+%d" % (frame_width, frame_height, frame_xpos, frame_ypos))

# Überschriften fürs Hauptfenster
# -------------------------------
gui_wetter.title('Wettervorhersage')         # Kopfzeile des Fensters

# Logo anzeigen
lab_kopf = tk.Label(gui_wetter, image=logo, borderwidth=2, relief='groove')
# Ortsnamen holen und verkürzen
ort = dateien('r', '', 'orte')              # Ortsdaten aus Datei 'orte.json' holen
ort = ort['name']                           # beschränken auf den Ortsnamen
ort_index = 0
for x in range(0,3):
    ort_index = ort.find(',', ort_index)+1  # 3 x finden eines Kommas im String
ort = ort[:ort_index-1]                     # Verkürzen des Ortsnamens für Überschrift

# Überschriften ausgeben
lab_kopf_1 = tk.Label(gui_wetter, text="Wettervorhersage", font=('Noto Sans', 18, 'bold'))
lab_kopf_2 = tk.Label(gui_wetter, text=ort, font=('Noto Sans', 14, 'bold'))
kopf_zeit = akt_zeit()
lab_kopf_3 = tk.Label(gui_wetter, text = kopf_zeit, font=('Noto Sans', 10))

# Logo und Überschriften im Kopf positionieren
lab_kopf.place(x=50, y=20)
lab_kopf_1.place(x=200, y=25)
lab_kopf_2.place(x=200, y=65)
lab_kopf_3.place(x=200, y=100)

# TABS einrichten
# ---------------
nb = ttk.Notebook(gui_wetter)
nb.place(x=10, y=150)                   # Startposition der Tabs
f1 = tk.Frame()
f2 = tk.Frame()
f3 = tk.Frame()
f4 = tk.Frame()
# TABs beschriften
nb.add(f1, text=' Vorhersage ')
nb.add(f2, text=' Details ')
nb.add(f3, text=' Diagramme ')
nb.add(f4, text=' Infos ')

# Fonts für den Fensterkopf definieren
# ------------------------------------
fontStyle = tkFont.Font(family="Noto Sans", size=11)        # Schrift für Button auf TABs
ttk.Style().configure(".", font=("Noto Sans", 11, 'bold'))  # Schrift für die Tabs
# Standard-Fonts anpassen
default_font = tkFont.nametofont("TkTextFont")
default_font.configure(family="Noto Sans", size=11)
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(family="Noto Sans", size=11)

# Start des Hauptprogramms
# ========================

icons()                 # Liste der Wettericons erstellen und speichern


#path = 'files/icons/'
#bild = PhotoImage(file=path + "fair_day.png")
#lab_logo = tk.Label(f1, image=bild)
#lab_logo.place(x=80, y=30)


# TAB Vorhersage füllen
tab_vorhersage()

#print("Zeit=", tstamp_to_date(1622127600))


tick()      # Uhr Ticker
gui_wetter.mainloop()