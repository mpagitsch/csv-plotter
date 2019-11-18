# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 16:29:47 2019

@author: michael.pagitsch
"""

import os
import tkinter as tk
from tkinter import ttk
import pandas as pd
import numpy as np

import matplotlib.backends.backend_tkagg as tkagg
import matplotlib.pyplot as plt


###  GLOBALE DATENVARIABLE  ###################################################
#global data

###  CALLBACK-FUNKTIONEN  #####################################################
def load_data():
    # Prüfe, ob Datei vorhanden. Nein --> Fehlermeldung, fertig
    file_path = input_path.get()
    if os.path.isfile(file_path):  # Datei vorhanden
        sep = radio_sep.get()
        decimal = radio_decimal.get()
        try:
            global data
            global options
            status.set('Reading file...')
            data = pd.read_csv(file_path, sep=sep, decimal=decimal)
            reset_plot()
            reset_dropdown()
            status.set('Read file successfully: <{}>'.format(file_path))
            
            # Set dropdown menu
            options = list(data.columns)
            lst_dataselection.config(values=options)
            
            # Set fileinfo
            filesize_MB = os.path.getsize(file_path)/1048576
            filelength = len(data)
            number_of_cols = len(data.columns)
            file_name = os.path.split(file_path)[1]
            status_fileinfo.set('{} ({:.1f} MB / {} lines / {} columns)'.format(file_name, filesize_MB, filelength, number_of_cols))
        except:
            status.set('ERROR: Could not read file <{}>.'.format(file_path))
            reset_fileinfo()
    else:  # Datei nicht vorhanden
        status.set('ERROR: File <{}> does not exist!'.format(file_path))
        #lbl_status.config(fg='red')  # Nur zum Test: Schriftfarbe ändern
    
    return 0

def update_plot():
    #global option
    plot_series = lst_dataselection.get()
    if plot_series in options:
        global plot
        status.set('Plotting <{}>...'.format(plot_series))
        fig.clear()
        fig.add_subplot(111).plot(data[plot_series])
        canvas.draw()
        status.set('Ok')
    elif plot_series == '':
        status.set('ERROR: Please select variable to plot.')
    else:
        status.set('ERROR: Series <{}> not available.'.format(plot_series))


###  INIT-FUNKTIONEN  #########################################################
def set_status():
    status.set('Ok')

def reset_plot():
    fig.clear()
    canvas.draw()

def reset_dropdown():
    lst_dataselection.config(values=[])

def reset_fileinfo():
    status_fileinfo.set('No file loaded.')


###  GUI-Elemente definieren  #################################################

window = tk.Tk()
window.geometry(newGeometry='1365x780+0+0')
window.title('CSV-Viewer')
window.resizable(0, 0)
window.iconbitmap('./resources/csv.ico')

# Variablen
radio_sep = tk.StringVar(window)
radio_sep.set(',')  # Default value
radio_decimal = tk.StringVar(window)
radio_decimal.set('.')  # Default value
plotselection = tk.StringVar(window)
options = []
frm_plot = tk.Frame(master=window)
status = tk.StringVar(window)
status_fileinfo = tk.StringVar(window)
reset_fileinfo()

# Dateneingabe
frm_input = tk.Frame(master=window)
lbl_path = tk.Label(master=frm_input, text='Full path to data file:')
input_path = tk.Entry(master=frm_input, bd=1, width=70)
lbl_sep = tk.Label(master=frm_input, text='Column separator:')
lbl_dec = tk.Label(master=frm_input, text='Decimal:')
radio_sep1 = tk.Radiobutton(master=frm_input, variable=radio_sep, text=',', value=',')
radio_sep2 = tk.Radiobutton(master=frm_input, variable=radio_sep, text=';', value=';')
radio_sep3 = tk.Radiobutton(master=frm_input, variable=radio_sep, text='tab', value=r'\t')
radio_decimal1 = tk.Radiobutton(master=frm_input, variable=radio_decimal, text='.', value='.')
radio_decimal2 = tk.Radiobutton(master=frm_input, variable=radio_decimal, text=',', value=',')
btn_load_data = tk.Button(master=frm_input, text='Load data', command=load_data)

# Datenauswahl
frm_dataselection = tk.Frame(master=window)
lbl_dataselection = tk.Label(master=frm_dataselection, text='Select plot data:')
lst_dataselection = ttk.Combobox(master=frm_dataselection, values=options)
btn_dataselection = tk.Button(master=frm_dataselection, text='Update plot', command=update_plot)

# Plot
fig = plt.Figure(figsize=(13, 6), dpi=100)
t = np.arange(0, 3, .01)
fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
canvas = tkagg.FigureCanvasTkAgg(fig, master=window)
canvas.draw()

# Status
frm_status = tk.Frame(master=window, bg='#808080')
lbl_status = tk.Label(master=frm_status, textvariable=status, bg='#808080', fg='#ffffff')
lbl_status_fileinfo = tk.Label(master=frm_status, textvariable=status_fileinfo,  bg='#808080', fg='#ffffff')


###  GUI-Elemente platzieren  #################################################

# Dateneingabe
frm_input.pack(side='top', padx='7', pady='7', fill='x', anchor='w')
lbl_path.pack(side='left', padx='7')
input_path.pack(side='left', padx='7')
lbl_sep.pack(side='left', padx='7', anchor='e', expand=True)
radio_sep1.pack(side='left', padx='7')
radio_sep2.pack(side='left', padx='7')
radio_sep3.pack(side='left', padx='7')
lbl_dec.pack(side='left', padx='7', anchor='e', expand=True)
radio_decimal1.pack(side='left', padx='7')
radio_decimal2.pack(side='left', padx='7')
btn_load_data.pack(side='left', padx='7', anchor='e', expand=True)

# Datenauswahl
frm_dataselection.pack(side='top', padx='7', pady='7', fill='x', anchor='w')
lbl_dataselection.pack(side='left')
lst_dataselection.pack(side='left')
btn_dataselection.pack(side='left', padx='7')

# Plot
frm_plot.pack(side='top', padx='7', pady='7', fill='both')
canvas.get_tk_widget().pack(side='top', padx='7', pady='7', fill='both')
tkagg.NavigationToolbar2Tk(canvas, frm_plot)

# Status
frm_status.pack(side='bottom', padx='7', pady='7', fill='x', expand=True)
lbl_status.pack(side='left', padx='7')
lbl_status_fileinfo.pack(side='right', padx='7')

set_status()
reset_plot()
window.mainloop()

# https://pythonbuch.com/gui.html
# https://matplotlib.org/3.1.0/gallery/user_interfaces/embedding_in_tk_sgskip.html

# Ausrichtung der Objekte: https://www.inf-schule.de/software/gui/entwicklung_tkinter/layout/pack

# Z:/znobackup/ReStroK-Daten/Daten/bornevii/e824064.csv
# Z:/znobackup/ReStroK-Daten/Daten/distelrath/15697.csv