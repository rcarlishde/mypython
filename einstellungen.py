#!/usr/bin/python
"""
********************************
* Dateiname: einstellungen.py  *
*   Version: 2.2               *
*     Stand: 18.07.2021        *
*     Autor: Richard Carl      *
********************************

Einstellungen:

Hier werden die Grundeinstellungen des Projekts vorgenommen.
Ortswahl:   Auswahl des Ortes, dessen Wetter angezeigt werden soll
Ort:        Daten (Bez., Breiten- und Längengrad, Höhe, Zeitzone)
Einheiten:  Dimensionen der Wetterparameter die angezeigt werden.
Aussehen:   noch nicht definiert
Info:       Informationen zum Programm und den Quellen der Wetterdaten

Das Pflichtenheft hierzu findet man hier:
/home/ricki/Dokumente/Hobby/Python/Python Projekt Wetter.odt
"""

# Imports
# #######
import tkinter as tk                # GUI starten
from tkinter import *
from tkinter import messagebox      # MessageBoxen
# from tkinter import colorchooser  # Colorpicker package
import tkinter.font as tkFont       # Schriften selbst definieren
from tkinter.font import Font       # Systemfont importieren, kann nun variiert werden
import tkinter.ttk as ttk           # Tabs für die GUI
import datetime                     # Datums- und Zeitberechnung
import json                         # Daten im Format JSON verarbeiten
import requests                     # ermöglicht das Einlesen von Daten via API


# Funktionen #
# ########## #

# Datenbeschaffung
# ----------------

def ort_suchen(ort):
    """Den angegeben Ort bei OpenStreetMap suchen"""
    #
    # Variablen:
    #   ort = nach diesem Ortsnamen suchen
    #   orte = gefundene Daten auf OpenStreetMap
    #
    url = "https://nominatim.openstreetmap.org/search/{}?format=json&addressdetails=1".format(ort)
    r = requests.get(url)
    orte = r.json()
    # debugging
    """
    print("Orte von OpenStreetMap, Rohdaten:")
    for x in orte:
        print(x,"\n")   # x=Daten je Stadt
    """
    return orte


def ort_trefferliste(orte):
    """Reduzierung der Daten je Ort aus Funktion "ort_suchen() auf die Rückgabewerte
       treffer = [['id','name','lat', 'lon', 'sym', 'staat']]"""
    #
    # Variablen:
    #   orte    = Liste der Orte  aus Funktion: "ort_suchen()"
    #   breite  = Begrenzung der Anzahl der Zeichen je Zeile in Trefferliste
    #
    # Dict-Namen:
    #   id      = ID-Nummer vom Provider
    #   name    = Name des Orts
    #   lat     = Breitengrad
    #   lon     = Längengrad
    #   sym     = Kürzel des Staates ('de')
    #   staat   = Name des Staates
    #

    breite = 80

    ortstreffer = []
    for x in orte:
        y = {'id': str(x['place_id']),
             'name': x['display_name'][:breite],
             'lat': x['lat'],
             'lon': x['lon'],
             'sym': x['address']['country_code'],
             'staat': x['address']['country']
             }
        ortstreffer.append(y)
    # print("Trefferliste:\n", treffer)           # debugging
    return ortstreffer


def ort_hoehe(lat, lon):
    """Höhe des Ortes über NN ermitteln.
       Die Daten stammen vom Norwegian Meteorologisk Institutt"""
    #
    # Variablen
    #   lat     = Breitengrad
    #   lon     = Längengrad
    #   url     = webseite des Instituts
    #   headers = geänderter header
    #   daten   = Rohdaten vom Institut
    #
    # Rückgabewert:
    #   hoehe = Höhe des Ortes über NN in Meter
    #
    url = "https://api.met.no/weatherapi/locationforecast/2.0/complete?lat=" +\
          str(lat) + "&lon=" + str(lon)
    # header der url muss geändert werden wegen Fehler in " import requests",
    # webseite meldet sonst error 403
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64;"}
    r = requests.get(url, headers=headers)
    daten = r.json()
    # print("r.json => ", daten)                # debugging
    hoehe = (daten['geometry']['coordinates'][2])
    return hoehe


def time_zone(lat, lon):
    """Timezone zum Ort ermitteln
       Die Daten stammen von OpenWeatherMap - onecall"""
    #
    # Variablen:
    #   lat = Breitengrad
    #   lon = Längengrad
    #   url = Webseite von OpenWeatherMap
    # Rückgabewert:
    #   timezone = Zeitzone im Klartext
    #
    url = "https://api.openweathermap.org/data/2.5/onecall?lat=" + \
          str(lat) + "&lon=" \
          + str(lon) + "&lang=de&appid=e9795e0ea062e5a6b848c34b35313cb8"
    r = requests.get(url)
    # print("URL=", url)                # debugging
    daten = r.json()
    timezone = (daten['timezone'])
    return timezone


# Zeit Berechnungen
# -----------------
""" Datum / Zeit berechnen und anzeigen """

def aktDatum():
    now = datetime.datetime.now()
    now_date = now.strftime('%d.%m.%Y')
    return now_date

def aktZeit():
    now = datetime.datetime.now()
    now_time = now.strftime('%H:%M:%S')
    return now_time

def tick():
    """aktualisiert jede Sekunde die Zeit+Datum und aktualisiert
       sie in der Überschrift des Hauptfensters """
    datum = aktDatum()
    zeit = aktZeit()
    lab_kopf_3.config(text=datum)
    lab_kopf_4.config(text=zeit)
    lab_kopf_4.after(1000, tick)


def tab_aussehen():
    """ Einstellungen für das Aussehen des Wetterberichts vornehmen"""
    #
    # Variablen:
    #
    # fontlist  =   Liste der im PC verfügbaren Fonts
    # font_size =   Liste der zulässigen Schriftgrößen
    # myfont    =   Font für die aktuelle GUI

    # Fonts lesen und Duplikate eleminieren
    fontlist = sorted(set(tkFont.families()))
    # Size-Liste festlegen
    font_size = (8, 9, 10, 11, 12, 14, 16, 18)
    myfont = Font(family="Noto Sans",
                  size=11,
                  weight="normal",
                  slant="roman",
                  underline=0,
                  overstrike=0)

    def get_font(event):
        """Schriftart und Schriftgröße auswählen und im Beispieltext wiedergeben"""
        sel_font = 'Noto Sans'
        sel_size = 11
        if combo_fonts.get():
            sel_font = combo_fonts.get()
        if combo_size.get():
            sel_size = int(combo_size.get())
        myfont.configure(family=sel_font, size=sel_size)
        btn_uebernehmen['font'] = myfont

    def update_fonts(event):
        """Liste der Fonts nach erstem eingegebenen Buchstaben filtern und updaten"""
        eingabe = event.char        # eingegebener Buchstabe
        # Filter
        if (event.keycode >= 24) and (event.keycode <= 58):
            new_list = list(filter(lambda x: x[0].lower() in eingabe, fontlist))
            combo_fonts['values'] = new_list
        else:
            combo_fonts['values'] = fontlist

    def iconsatz(event):
        """Auswahl des Iconsatzes aus der Combobox"""
        #
        # Variablen:
        # logo  ⁼ Icon "02d.png" aus dem jeweilig ausgewählten Iconset
        # btn_uebernehmen   = Button zur Übernahme der getroffenen Auswahl
        #
        if combo_iconset.get() == "Standard Icons":
            logo = tk.PhotoImage(file=r"files/icons/02d.png")
        elif combo_iconset.get() == "Iconsatz 1":
            logo = tk.PhotoImage(file=r"files/icons1/02d.png")
        else:
            logo = tk.PhotoImage(file=r"files/icons2/02d.png")
        btn_uebernehmen.config(image=logo)  # Icon anzeigen
        btn_uebernehmen.photo = logo        # Fehlerkorrektur der Grafik
        return logo

    def uebernahme():
        """Übernahme der Aussehens-Auswahl und speichern in Datei 'aussehen.json'"""
        #
        # Variablen:
        # aussehen  = alle einstellbaren Font-Parameter
        aussehen = {'name_font':combo_fonts.get(), 'name_size':int(combo_size.get()),
                    'name_iconset':combo_iconset.get()}
        dateien('w', aussehen, 'aussehen')  # Daten schreiben
        set_aussehen()  # gespeicherte Font-Parameter in Ansicht übernehmen
        return

    # Inhalt der Datei 'aussehen.json' in Anzeige bringen

    # Muster-Icon gemäß Datei "aussehen.json" festlegen
    if aussehen['name_iconset'] == "Standard Icons":
        logo = tk.PhotoImage(file=r"files/icons/02d.png")
        index=0
    elif aussehen['name_iconset'] == "Iconsatz 1":
        logo = tk.PhotoImage(file=r"files/icons1/02d.png")
        index=1
    else:
        logo = tk.PhotoImage(file=r"files/icons2/02d.png")
        index=2

    # Iconsatz auswählen
    lab_iconset = tk.Label(f4, text='Iconsatz: ', padx=10, pady=20)
    lab_iconset.grid(column=0, row=0, sticky=E)
    combo_iconset = ttk.Combobox(f4, values=("Standard Icons",
                                             "Iconsatz 1", "Iconsatz 2"), width=30)
    combo_iconset.current(index)
    combo_iconset.grid(column=1, row=0)
    combo_iconset.bind('<<ComboboxSelected>>', iconsatz)
    combo_iconset.bind('<Key>', update_fonts)

    # Schriftart auswählen
    lab_fonts = tk.Label(f4, text='Schriftart: ', padx=10, pady=0)
    lab_fonts.grid(column=0, row=1, sticky=E)
    combo_fonts = ttk.Combobox(f4, values=fontlist, width=30)
    combo_fonts.current(53)
    combo_fonts.grid(column=1, row=1)
    combo_fonts.bind('<<ComboboxSelected>>', get_font)
    combo_fonts.bind('<Key>', update_fonts)

    # Schriftgröße auswählen
    lab_size = tk.Label(f4, text="Schriftgröße: ", padx=10, pady=5)
    lab_size.grid(column=0, row=2, sticky=E)
    combo_size = ttk.Combobox(f4, value=font_size, width=10, state='readonly')
    combo_size.current(3)
    combo_size.grid(column=1, row=2, sticky='w')
    combo_size.bind('<<ComboboxSelected>>', get_font)

    # Muster-Icon in Button 'uebernehmen' anzeigen
    btn_uebernehmen = Button(f4, text="Einstellungen\nübernehmen",
                             image=logo, compound=TOP, width='100', height='100',
                             cursor='hand2', command=uebernahme)
    btn_uebernehmen.photo = logo                # Fehlerkorrektur der Grafik
    btn_uebernehmen.grid(column=2, row=0, rowspan=4, padx=20)

def set_aussehen():
    """Das gewählte Aussehen (Fonts usw.) in die Anzeige übernehmen"""
    #
    # Variablen:
    #
    # aussehen  = Dictionary mit Daten, eingestellt auf dem TAB "Aussehen"
    # font_name = ausgewählter Fontname
    # font_size = ausgewählte Fontgröße
    # font_wb   = Schrift fett schreiben
    aussehen = {}
    aussehen = dateien('r', aussehen, 'aussehen')       # daten lesen

    # print("Aussehen(set_aussehen)=", aussehen)        # debugging

    font_name = aussehen['name_font']
    font_size = aussehen['name_size']
    font_wb = "bold"  # Schrift - fett
    # Standardfonts festlegen
    ttk.Style().configure(".", font=(font_name, font_size, font_wb))
    default_font = tkFont.nametofont("TkTextFont")
    default_font.configure(family=font_name, size=font_size)
    default_font = tkFont.nametofont("TkDefaultFont")
    default_font.configure(family=font_name, size=font_size)

    # Fonts der GUI-Überschriften anpassen
    lab_kopf_1.configure(font=(font_name, 14), text="Wetterbericht")
    lab_kopf_2.configure(font=(font_name, 11))
    lab_kopf_3.configure(font=(font_name, 10))
    lab_kopf_4.configure(font=(font_name, 10))

    return aussehen

def dateien(mod, daten, filename):
    """ Aufbereitung, speichern und/oder lesen aller Dateien im Format JSON """
    #
    # Variablen:
    # mod           = 'r'=lesen, 'w'= schreiben
    # filename      = Name der Datei die gesichert bzw. gelesen wird, ohne Dateiendung!
    # file          = filename mit Pfad
    # daten         = Daten aus der Datei (Dictionary)
    # message_text  = Fehlermeldung, falls Datei nicht existent
    # std_ort       = Standardort
    # std_einheiten = Standardeinheiten
    #

    # Standardwerte / Standarddaten setzen:
    # -------------------------------------
    # Standardwerte für die Datei "orte.json"
    std_ort = {
        'name': 'Neuss, Rhein-Kreis Neuss, Regierungsbezirk Düsseldorf, Nordrhein-Westfalen, Deutschland',
        'lat': '51.1981778',
        'lon': '6.6916476',
        'hoehe': 43,
        'zeitzone': 'Europe/Berlin',
        'sym': 'de',
        'staat': 'Deutschland'}
    # Standardwerte für die Datei "einheiten.json"
    std_einheiten = {
        'temp': 'Celsius (°C)',
        'druck': 'Hekto Pascal (hPa)',
        'speed': 'm/s',
        'regen': 'mm',
        'hoehe': 'Meter (m)',
        'feuchte': 'in Prozent (%)',
        'wolken': 'in Prozent (%)',
        'uvi': 'von 1 bis 11+'}
    # Standardwerte für die Datei "eu.json"
    eu_staaten = {
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
    # Standardwerte für die Datei "aussehen.json"
    std_aussehen = {
        'name_font': 'Noto Sans',
        'name_size': 11,
        'name_iconset': 'Standard Icons'
    }

    file = 'files/' + filename + ".json"
    # print("File = " + file)                           # debugging
    message_text = "Die Datei " + filename + ".json existiert nicht oder ist leer!\n\n"
    message_text += "Die Datei wird nun mit Standardwerten neu erstellt."
    #
    # Datei bearbeiten:
    # -----------------
    try:  # Dateien lesen bzw. schreiben
        if mod == "w":  # Daten schreiben
            with open(file, 'w') as datei:
                json.dump(daten, datei, ensure_ascii=False, indent=4)
        else:           # Daten einlesen
            with open(file, 'r') as datei:
                daten = json.load(datei)
    except FileNotFoundError:  # Im Fehlerfall Standardwerte schreiben
        if filename == 'orte':                                  # Standard-Orte
            daten = std_ort
        elif filename == 'einheiten':                           # Standard-Einheiten
            daten = std_einheiten
        elif filename == 'aussehen':                            # Standard-Aussehen
            daten = std_aussehen
        elif filename == 'eu' or filename == 'world':           # Falls world.json fehlt, umstellen auf EU-Staaten
            daten = eu_staaten
            file = 'files/eu.json'
            message_text = "Die Liste aller Staaten (" + filename + \
                           ".json) existiert nicht oder ist leer!\n\n"
            message_text += "Es stehen daher nur die Daten der EU-Staaten zur Verfügung!"
        with open(file, 'w') as datei:                          # Standardwerte schreiben
            json.dump(daten, datei, ensure_ascii=False, indent=4)
        messagebox.showinfo('Fehler', message_text, icon='error')
    return daten


def tab_ortswahl(ort_in):
    """ Den TAB "Ortswahl" füllen"""

    def ortswahl(event):
        """Gefundene Treffer aus dem Internet in die Listbox
           (nur Ortsbezeichnung) eintragen"""
        # Variablen:
        #   treffer = Liste der gefundenen Daten
        #   index   = Zähler bzw. Index der Listbox.Position
        #   staat   =
        #   ort_in =
        #   orte
        global treffer
        global staat
        # print('Staat=', staat)            # debugging
        # print('Treffer= \n", treffer      # debugging
        listbox_ort.delete(0, "end")        # alten Inhalt der Listbox löschen
        ort_eingabe = ein_such.get()        # aktuellen Suchbegriff (Stadt) holen

        if staat:  # ggf. Filter Staat hinzufügen
            ort_eingabe += ',' + staat
        # print('Ortswahl = ', ort_eingabe) # debuggin

        orte = ort_suchen(ort_eingabe)      # Ort suchen + Rohdaten aus URL lesen
        treffer = ort_trefferliste(orte)    # Umwandlung in Trefferliste
        # print('Treffer:\n', treffer)      # debugging

        # Trefferliste ins Fenster der Listbox übertragen
        index = -1
        for x in treffer:
            index += 1
            listbox_ort.insert(index, x['name'])
        # print('index=', index)      # debugging

    def ort_selected(event):
        """Alle Daten des ausgesuchten Orts im TAB "Ortswahl" für den Tab:"ORT"
           vorbereiten und anzeigen"""
        #
        # Variablen:
        #   treffer     = (global) Daten der Trefferliste
        #   nb          = Kürzel für das tkinter-notebook (TAB-Auswahl)
        #   sel_index   = Index des ausgewählten Ortes in der Listbox
        #   sel_treffer = Detaillierte Daten zum ausgewählten Ort
        #   hoehe       = extern ermittelte Höhenlage des ausgewählten Orts
        #   zeitzone    = extern ermittelte Zeitzone des ausgewählten Ortes

        # print('Treffer = \n', treffer)            # debugging

        # Listenbox-Index des ausgewählten Orts identifizieren
        sel_index = listbox_ort.curselection()  # Liste mit Index der Position in listbox
        sel_index = sel_index[0]  # Position (int) in listbox

        # vollstänge Daten des ausgewählten Orts zusammenstellen
        hoehe = ort_hoehe(treffer[sel_index]['lat'], treffer[sel_index]['lon'])
        zeitzone = time_zone(treffer[sel_index]['lat'], treffer[sel_index]['lon'])
        sel_treffer = {'name': treffer[sel_index]['name'],
                       'lat': treffer[sel_index]['lat'],
                       'lon': treffer[sel_index]['lon'],
                       'hoehe': hoehe,
                       'zeitzone': zeitzone,
                       'sym': treffer[sel_index]['sym'],
                       'staat': treffer[sel_index]['staat']
                       }
        # print("Sel_Treffer = ", sel_treffer)          # debugging

        # Daten in TAB "Ort" anzeigen
        tab_ort(sel_treffer)  # Datensatz im Tab "Ort" ausgeben
        # print('sel_treffer = \n', sel_treffer)       # debugging
        nb.select(f2)  # TAB "ORT" aktivieren
        return sel_treffer

    def read_world(staaten):
        """Die Daten der Staaten (world.json) lesen
           Die Keys in world.json sind:
           'id', 'name', 'alpha2' und 'alpha3'
           Sie werden reduziert auf die Keys:
           'name' und 'alpha2'"""
        #
        # Variablen:
        # staaten = dictionary für die Liste der Staaten
        # reader = Zwischenspeicher für die Daten beim Einlesen der Dateien
        #
        reader = {}                                      # Zwischenspeicher initialisieren
        reader = dateien('r', reader, 'world')           # Datei "world.json" einlesen
        # print("READER = \n", reader, len(reader))      # debugging

        # Falls "world.json" existiert, Daten einlesen und reduzieren
        if len(reader) > 99:                                   # Mehr Staaten als die EU hat = world.json
            for x in reader:
                staaten[x['name']] = x['alpha2']               # reduzieren auf Felder 'name' + 'alpha2'
        # Falls nicht, Daten direkt aus "eu.json" übernehmen
        else:
            staaten = reader                                   # EU-Staaten einlesen
        # print('staaten  Type=', type(staaten), ':\n', staaten)        # debugging
        return staaten

    # Button "Staat" (kleines Dreick am Pulldownfeld
    def set_staat(event):
        """Funktion des Buttons "Staat" (kleines Dreieck an Combobox)
           ausgewählten Staat in Variable staat setzen """
        global staat
        staat = world_dict[combo_staat.get()]

    def update_values(event):
        """Liste der Staaten nach erstem eingegebenen Buchstaben filtern und updaten"""
        global staat
        eingabe = event.char  # eingebener Buchstabe
        # Filter
        if (event.keycode >= 24) and (event.keycode <= 58):
            new_list = list(filter(lambda x: x[0].lower() in eingabe, box_values))
            # print(new_list)                   # debugging
            combo_staat['values'] = new_list  # update values
        else:  # reset Filter
            staat = ""
            combo_staat['values'] = box_values

    # Button "suchen"
    btn_ortswahl = tk.Button(f1, text="suchen", cursor='hand2')
    btn_ortswahl.grid(column=9, row=1, padx=5, pady=5)
    btn_ortswahl.bind('<Button-1>', ortswahl)  # Mausklick

    # PullDown-Feld für die Auswahl der Staaten einrichten
    world_dict = {}  # Dictionary für alle Staaten der Welt vormerken
    world_dict = read_world(world_dict)  # Daten der Staaten aus JSON-Datei lesen
    breite = 15  # Feldbreite
    box_values = list(world_dict.keys())  # Inhalte auf Länderbezeichnung reduzieren

    combo_staat = ttk.Combobox(f1, values=box_values,
                               textvariable=staat,
                               width=breite,
                               style='TCombobox')
    combo_staat.grid(column=8, row=1)  # Position des Combofeldes
    combo_staat.bind('<<ComboboxSelected>>', set_staat)  # Auswahl in "staat" sichern
    combo_staat.bind('<Key>', update_values)  # Eingabefeld erhält den Namen des Landes/Staates

    # Suchfeld einrichten
    lab_ortssuche = tk.Label(f1, text='Suche nach:')
    lab_ortssuche.grid(column=1, row=1, padx=8, pady=8, sticky=E)
    ein_such = tk.Entry(f1, textvariable=ort_in, width=40)
    ein_such.insert(0, ort_in)
    ein_such.grid(column=2, row=1, padx=8, pady=8)
    ein_such.bind('<Return>', ortswahl)  # Taste <enter>

    # Listbox
    listbox_ort = tk.Listbox(f1, bd=2, width=70, height=11, selectmode='single')
    listbox_ort.grid(columnspan=10, column=1, row=2, padx=8, pady=8, sticky=W)
    listbox_ort.bind('<Return>', ort_selected)  # Taste <enter>
    listbox_ort.bind('<Double-Button-1>', ort_selected)  # Maus Doppelklick


def tab_ort(daten):
    """Den TAB "ORT" ausgeben"""
    #
    # Variablen:
    # "ortsdaten" enthält:
    #   [name]      = Ortsname
    #   [lat]       = Breitengrad
    #   [lon]       = Längengrad
    #   [hoehe]     = Höhe des Ortes über NN
    #   [zeitzone]  = Zeitzone des Ortes
    #   [sym]       = Kürzel des Staates
    #   [staat]     = Name des Staates
    #
    # Beschriftungen durchführen
    lab_bez = tk.Label(f2, text='Bezeichnung:')
    lab_lat = tk.Label(f2, text='Breitengrad:')
    lab_lon = tk.Label(f2, text='Längengrad:')
    lab_hoh = tk.Label(f2, text='Höhe (NN):')
    lab_zz = tk.Label(f2, text='Zeitzone:')
    px, py = 5, 5  # Abstände der Labels
    lab_bez.grid(column=1, row=0, padx=px, pady=py, sticky=E)
    lab_lat.grid(column=1, row=1, padx=px, pady=py, sticky=E)
    lab_lon.grid(column=1, row=2, padx=px, pady=py, sticky=E)
    lab_hoh.grid(column=1, row=3, padx=px, pady=py, sticky=E)
    lab_zz.grid(column=1, row=4, padx=px, pady=py, sticky=E)

    # Daten ausgeben
    label_bez = tk.Label(f2, text=daten['name'], borderwidth=1,
                         relief="ridge", width=60, height=1, anchor=W)
    label_lat = tk.Label(f2, text=str(daten['lat']) + "°", borderwidth=1,
                         relief="ridge", width=20, height=1, anchor=W)
    label_lon = tk.Label(f2, text=str(daten['lon']) + "°", borderwidth=1,
                         relief="ridge", width=20, height=1, anchor=W)
    label_hoh = tk.Label(f2, text=str(daten['hoehe']) + " m", borderwidth=1,
                         relief="ridge", width=10, height=1, anchor=W)
    label_zz = tk.Label(f2, text=daten['zeitzone'], borderwidth=1,
                        relief="ridge", width=20, height=1, anchor=W)
    label_st = tk.Label(f2, text=daten['staat'], borderwidth=0,
                        width=12, height=1, anchor=E)

    px, py = 5, 8  # Abstände der Labels
    label_bez.grid(column=2, row=0, padx=px, pady=5)
    label_lat.grid(column=2, row=1, padx=px, pady=py, sticky=W)
    label_lon.grid(column=2, row=2, padx=px, pady=py, sticky=W)
    label_hoh.grid(column=2, row=3, padx=px, pady=py, sticky=W)
    label_zz.grid(column=2, row=4, padx=px, pady=py, sticky=W)
    label_st.grid(column=2, row=3, sticky=E)

    # Flagge anzeigen
    bild = tk.PhotoImage(file='files/flags/64x64/' + daten['sym'] + '.png')
    label_img = tk.Label(f2, image=bild, borderwidth=2)
    label_img.image = bild
    label_img.grid(column=2, row=2, sticky=E)

    # print('Ortsdaten =\n', ortsdaten) # debugging

    dateien('w', daten, 'orte')     # Ortsdaten in Datei 'orte.json' speichern


def tab_einheiten(sel_einheiten):
    """Den TAB "EINHEITEN" ausgeben und Auswahl treffen"""
    #
    # Variablen:
    # sel_einheiten = Dictionary der aktuellen, bereits ausgewählten Einheiten
    # std_einheiten = Dictionary der Standardeinstellungen
    # all_einheiten = Dictionary mit allen, zur Auswahl stehenden Einheiten
    #   temp    = Einheit für Temperaturen
    #   druck   = Einheit für Luftdruck
    #   speed   = Einheit für Windgeschwindigkeit und Windstärke
    #   regen   = Einheit für Niederschlag
    #   hoehe   = Einheit für die Höhe des Ortes über NN
    #   feuchte = Einheit für die rel. Luftfeuchte
    #   wolken  = Einheit für die Bewölkungsdichte
    #   uvi     = Einheit für den UV-Index

    all_einheiten = {
        'temp': ["°C", "°K", "°F"],
        'druck': ["hPa", "mmHG"],
        'speed': ["km/h", "m/s", "Windstärken 0-12"],
        'regen': ["ltr/m²", "mm"],
        'hoehe': ['m'],
        'feuchte': ['%'],
        'wolken': ['%'],
        'uvi': ['von 1 bis 11+']
        }

    std_einheiten = {
        'temp': '°C',
        'druck': 'hPa',
        'speed': 'm/s',
        'regen': 'mm',
        'hoehe': 'm',
        'feuchte': '%',
        'wolken': '%',
        'uvi': 'von 1 bis 11+'
        }

    def aktualisiere_einheiten(event):
        """aktuelle Daten (Einheiten) in Datei sichern
           temp,druck,speed und regen sind wählbar, der Rest ist fix"""
        sel_einheiten['temp'] = combo_temp.get()
        sel_einheiten['druck'] = combo_druck.get()
        sel_einheiten['speed'] = combo_speed.get()
        sel_einheiten['regen'] = combo_regen.get()
        dateien('w', sel_einheiten, 'einheiten')  # Daten speichern
        # print('akt_einheiten', sel_einheiten)          # debugging

    def set_temp(tmp_einheiten):
        """ausgewählte Einheit für temp setzen"""
        temperatur = tmp_einheiten['temp']
        if temperatur == all_einheiten['temp'][1]:
            combo_temp.current(1)
        elif temperatur == all_einheiten['temp'][2]:
            combo_temp.current(2)
        else:
            combo_temp.current(0)

    def set_druck(druck_einheiten):
        """ausgewählte Einheit für druck setzen"""
        luftdruck = druck_einheiten['druck']
        if luftdruck == all_einheiten['druck'][1]:
            combo_druck.current(1)
        else:
            combo_druck.current(0)

    def set_speed(speed_einheiten):
        """ausgewählte Einheit für speed (Windgeschwindigkeit) setzen"""
        wind_speed = speed_einheiten['speed']
        if wind_speed == all_einheiten['speed'][0]:
            combo_speed.current(0)
        elif wind_speed == all_einheiten['speed'][2]:
            combo_speed.current(2)
        else:
            combo_speed.current(1)

    def set_regen(regen_einheiten):
        """ausgewählte Einheit für regen setzen"""
        rain = regen_einheiten['regen']
        if rain == all_einheiten['regen'][0]:
            combo_regen.current(0)
        else:
            combo_regen.current(1)

    def set_standard(event):
        """Alle Einheiten auf Standardwerte setzen"""
        akt_einheiten = std_einheiten
        set_temp(akt_einheiten)
        set_druck(akt_einheiten)
        set_regen(akt_einheiten)
        set_speed(akt_einheiten)
        dateien('w', akt_einheiten, 'einheiten')    # Standardwerte in Datei speichern
        # print('TEST:', akt_einheiten)             # debugging

    # Beschriftungen durchführen
    lab_temp = tk.Label(f3, text='Temperaturen:', height=1)
    lab_druck = tk.Label(f3, text='Luftdruck:', height=1)
    lab_wind = tk.Label(f3, text='Windgeschwindigkeit:')
    lab_regen = tk.Label(f3, text='Niederschläge:')
    lab_hoehe = tk.Label(f3, text='Höhen:')
    lab_feuchte = tk.Label(f3, text='Feuchte:')
    lab_wolken = tk.Label(f3, text='Bewölkung:')
    lab_uvi = tk.Label(f3, text='UV-Index:')

    px, py = 5, 7  # Abstände der Labels
    lab_temp.grid(column=1, row=0, padx=px, pady=py, sticky=E)
    lab_druck.grid(column=1, row=1, padx=px, pady=py, sticky=E)
    lab_wind.grid(column=1, row=2, padx=px, pady=py, sticky=E)
    lab_regen.grid(column=1, row=3, padx=px, pady=py, sticky=E)
    lab_hoehe.grid(column=1, row=4, padx=px, pady=py, sticky=E)
    lab_feuchte.grid(column=1, row=5, padx=px, pady=py, sticky=E)
    lab_wolken.grid(column=1, row=6, padx=px, pady=py, sticky=E)
    lab_uvi.grid(column=1, row=7, padx=px, pady=py, sticky=E)

    # Einheiten auswählen: Temperatur
    breite = 25
    temp = sel_einheiten['temp']
    combo_temp = ttk.Combobox(f3, values=all_einheiten['temp'],
                              textvariable=temp, width=breite)
    combo_temp.grid(column=2, row=0, padx=px, pady=py, sticky=W)
    set_temp(sel_einheiten)  # Auswahl 'temp' setzen
    combo_temp.bind('<<ComboboxSelected>>', aktualisiere_einheiten)

    # Einheiten auswählen: Druck
    druck = sel_einheiten['druck']
    combo_druck = ttk.Combobox(f3, values=all_einheiten['druck'],
                               textvariable=druck, width=breite)
    combo_druck.grid(column=2, row=1, padx=px, pady=py, sticky=W)
    set_druck(sel_einheiten)  # Auswahl 'druck' setzen
    combo_druck.bind('<<ComboboxSelected>>', aktualisiere_einheiten)

    # Einheiten auswählen: Windgeschwindigkeit
    speed = sel_einheiten['speed']
    combo_speed = ttk.Combobox(f3, values=all_einheiten['speed'],
                               textvariable=speed, width=breite)
    combo_speed.grid(column=2, row=2, padx=px, pady=py, sticky=W)
    set_speed(sel_einheiten)  # Auswahl 'speed' setzen
    combo_speed.bind('<<ComboboxSelected>>', aktualisiere_einheiten)

    # Einheiten auswählen: Niederschläge
    regen = sel_einheiten['regen']
    combo_regen = ttk.Combobox(f3, values=all_einheiten['regen'],
                               textvariable=regen, width=breite)
    combo_regen.grid(column=2, row=3, padx=px, pady=py, sticky=W)
    set_regen(sel_einheiten)
    combo_regen.bind('<<ComboboxSelected>>', aktualisiere_einheiten)

    # restliche Einheiten sind fix:
    breite = 20
    hoehe = all_einheiten['hoehe'][0]
    lab_einheit_hoehe = tk.Label(f3, borderwidth=1, relief="ridge",
                                 width=breite, anchor=W, text=hoehe)
    feuchte = all_einheiten['feuchte'][0]
    lab_einheit_feucht = tk.Label(f3, borderwidth=1, relief="ridge",
                                  width=breite, anchor=W, text=feuchte)
    wolken = all_einheiten['wolken'][0]
    lab_einheit_wolken = tk.Label(f3, borderwidth=1, relief="ridge",
                                  width=breite, anchor=W, text=wolken)
    uvi = all_einheiten['uvi'][0]
    lab_einheit_uvi = tk.Label(f3, borderwidth=1, relief="ridge",
                                   width=breite, anchor=W, text=uvi)
    lab_einheit_hoehe.grid(column=2, row=4, padx=px, pady=py, sticky=W)
    lab_einheit_feucht.grid(column=2, row=5, padx=px, pady=py, sticky=W)
    lab_einheit_wolken.grid(column=2, row=6, padx=px, pady=py, sticky=W)
    lab_einheit_uvi.grid(column=2, row=7, padx=px, pady=py, sticky=W)

    btn_standard = tk.Button(f3, text="Standardwerte", cursor='hand2')
    # btn_standard.grid(column=9, row=0, padx=5, pady=5)
    btn_standard.place(x=525, y=5)
    btn_standard.bind('<Button-1>', set_standard)  # Mausklick

    # aktuelle Daten sichern
    sel_einheiten = {'temp': temp,
                     'druck': druck,
                     'speed': speed,
                     'regen': regen,
                     'hoehe': hoehe,
                     'feuchte': feuchte,
                     'wolken': wolken,
                     'uvi': uvi}
    dateien('w', sel_einheiten, 'einheiten')

    # debugging
    """
    temp = std_einheiten['temp']
    lab_test = tk.Label(f3, textvariable=temp)
    lab_test.grid(column=1, row=8, padx=px, pady=py, sticky=E)
    """


# Den TAB "Info" füllen
# ---------------------
def tab_info():
    """Den TAB "Info" füllen"""
    # Infotext aus Datei lesen
    text = open("files/info_einstellungen.txt", 'r')
    text_info = text.read()
    # Scrollbar einrichten und einschalten
    scroll = Scrollbar(f5)
    info = Text(f5, borderwidth=2, relief="ridge", height=20, width=90)
    # Scrollbar -> rechts außen, volle Höhe (sticky=NS)
    scroll.grid(column=3, row=0, sticky=NS)
    info.grid(column=2, row=0, padx=5, pady=5)
    scroll.config(command=info.yview)
    info.config(yscrollcommand=scroll.set)
    info.insert(END, text_info)


# Reaktionen auf die Buttons
# --------------------------
def btn_schliessenclick():
    """Programm beenden"""
    gui_einstellungen.quit()


# Start Hauptprogramm
# ###################
#

# Hauptfenster erstellen
# ----------------------
# Hauptfenster soll oben, rechtsbündig im aktuellen Bildschirm mit eigenem Icon angezeigt werden

gui_einstellungen = Tk()  # init Fenster "Einstellungen"

# eigenes Icon/Logo (.png,.gif) festlegen (50*50)
logo = tk.PhotoImage(file="files/icons/fair_day.png")
gui_einstellungen.tk.call('wm', 'iconphoto', gui_einstellungen, logo)

# Dimensionen des Hauptfensters festlegen
frame_width = 775       # Fensterbreite in px (775)
frame_height = 475      # Fensterhöhe in px (475)
frame_ypos = 44         # Höhe der Taskleiste oben (44)
frame_xpos_right = 0    # Breite der Taskleiste rechts (53)

# Fenster-Geometrie berechnen
# Breite Bildschirm ermitteln in px
screen_width = gui_einstellungen.winfo_screenwidth()
# X-Position des Fensters berechnen
frame_xpos = screen_width - frame_width - frame_xpos_right
# Hinweis:     use width x height + x_offset + y_offset (no spaces!)
gui_einstellungen.geometry("%dx%d+%d+%d" % (frame_width, frame_height, frame_xpos, frame_ypos))
# Überschrift des Hauptfenters festlegen
gui_einstellungen.title('Wetterbericht - Einstellungen')

# Fonts definieren
font_name = "Noto Sans"  # Standard-Schriftart
font_size = 11  # Standard-Schriftgröße
font_wb = "bold"  # Schrift - fett

fontStyle = tkFont.Font(family=font_name, size=font_size)  # Font für Button auf TABs
ttk.Style().configure(".", font=(font_name, font_size, font_wb))  # Font für die Tabs
# Standard-Fonts anpassen
default_font = tkFont.nametofont("TkTextFont")
default_font.configure(family=font_name, size=font_size)
default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(family=font_name, size=font_size)

# Überschrift des Hauptfensters
lab_kopf = tk.Label(image=logo)
lab_kopf_1 = tk.Label(gui_einstellungen, text="Wetterbericht", font=(font_name, 14))
lab_kopf_2 = tk.Label(gui_einstellungen, text="Einstellungen", font=(font_name, 11))
lab_kopf_leer = tk.Label(gui_einstellungen)
lab_kopf_3 = tk.Label(gui_einstellungen, font=(font_name, 10))
lab_kopf_4 = tk.Label(gui_einstellungen, font=(font_name, 10))

lab_kopf.grid(column=0, row=0, rowspan=2, sticky=W)  # Logo
lab_kopf_1.grid(column=1, row=0, sticky=W)  # Überschrift1
lab_kopf_2.grid(column=1, row=1, sticky=W)  # Überschrift2
lab_kopf_leer.grid(column=2, row=0, padx=200)  # Leerspalte
lab_kopf_3.grid(column=3, row=0, padx=10, sticky=E)  # Datum
lab_kopf_4.grid(column=3, row=1, padx=10, sticky=E)  # Zeit


aussehen = {}
aussehen = set_aussehen()


# Einrichten der TABs im Hauptfenster
nb = ttk.Notebook(gui_einstellungen)


nb.grid(column=0, row=3, columnspan=4, padx=10, pady=10)
f1 = tk.Frame(nb)
f2 = tk.Frame(nb)
f3 = tk.Frame(nb)
f4 = tk.Frame(nb)
f5 = tk.Frame(nb)
# TABs beschriften
nb.add(f1, text=' Ortswahl ')
nb.add(f2, text=' Ort      ')
nb.add(f3, text=' Einheiten ')
nb.add(f4, text=' Aussehen ')
nb.add(f5, text=' Info     ')

# TABs füllen
# +++++++++++

# TAB: "Ortswahl" einrichten
# --------------------------
staat = ''
tab_ortswahl('')

# TAB "Ort" füllen
# ----------------
# Daten über den vorher ausgewählten Ort aus Datei lesen
ortsdaten = {}
ortsdaten = dateien('r', ortsdaten, 'orte')
# print('ortsdaten gelesen:\n', ortsdaten)  # debugging
tab_ort(ortsdaten)

# TAB "Einheiten" füllen
# ----------------------
einheiten = {}
einheiten = dateien('r', einheiten, 'einheiten')
tab_einheiten(einheiten)

# TAB "Aussehen" füllen
tab_aussehen()

# TAB "Info" füllen
# -----------------
tab_info()

# Button zum Beenden des Programms (Schließen)
btn_schliessen = tk.Button(gui_einstellungen, cursor='hand2',
                           text="Schließen", command=btn_schliessenclick)
btn_schliessen.grid(column=3, row=4)

tick()  # Uhrzeit und Datum anzeigen
gui_einstellungen.mainloop()  # Hauptfenster aktivieren / einschalten
