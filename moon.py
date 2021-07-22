#!/usr/bin/python
# coding=UTF-8
import datetime
import time

now_time = time.mktime(time.localtime())

# constants
syn_moon_month = 29.530589  # synodaler Monat

# constants
#hist_fullmoon = 2018, 9, 25, 6, 1, 36, 0, 0, 1  # Historischer Vollmond als Strukturierte Zeit
hist_fullmoon = 2021,5,26,13,14,51,2,0,1


moon_time = time.mktime(hist_fullmoon)  # Historischer Vollmond umgerechnet als Sekunden seit Epoch
hist_fullmoon_days = moon_time / 86400  # Historischer Vollmond - in Tagen seit Epoch
# actuals
now_days = now_time / 86400  # Tage seit Epoch bis jetzt
days_since_hist_fullmoon = now_days - hist_fullmoon_days  # Differenz in Tagen: Jetzt - Historischer VM
print("Tage seit historischem Vollmond= ", days_since_hist_fullmoon)
full_moons_since = days_since_hist_fullmoon / syn_moon_month  # Anzahl Vollmondereignisse seit hist. VM
print("Anzahl Vollmonde seit hist. Vollmond =", full_moons_since)
phase = round(full_moons_since, 2)  # Abrunden auf 2 Nachkommastellen
phase = (phase - int(phase))  # Nachkommastellen = Mondphase

# calculate moon phase
if phase == 0: phase = 1
if phase < 0.25:
    ptext = "abnehmender Mond (drittes Viertel)"
elif phase == 0.25:
    ptext = "abnehmender Halbmond (letztes Viertel)"
elif 0.25 < phase < 0.50:
    ptext = "abnehmende Sichel"
elif phase == 0.50:
    ptext = "Neumond"
elif 0.50 < phase < 0.75:
    ptext = "zunehmende Sichel"
elif phase == 0.75:
    ptext = "zunehmender Halbmond (erstes Viertel)"
elif 0.75 < phase < 1:
    ptext = "zunehmender Mond (zweites Viertel)"
elif phase == 1:
    ptext = "Vollmond"

print(phase,"\n", ptext)

# Von Pamplelune - Eigenes Werk, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=4314744
