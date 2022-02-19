import tkinter as tk
from tkinter import*
from tkinter import ttk
from tkinter import messagebox

global colorCeleste
colorCeleste = '#C6EBFF'
global colorBlanco
colorBlanco = '#F7F7F7'
global anchoVentana
anchoVentana = 900
global altoVentana
altoVentana = 600


def center(win):     
    win.update_idletasks() 
    width = win.winfo_width() 
    frm_width = win.winfo_rootx() - win.winfo_x() 
    win_width = width + 2 * frm_width 
    height = win.winfo_height() 
    titlebar_height = win.winfo_rooty() - win.winfo_y() 
    win_height = height + titlebar_height + frm_width 
    x = win.winfo_screenwidth() // 2 - win_width // 2 
    y = win.winfo_screenheight() // 2 - win_height // 2 
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y)) 
    win.deiconify()

class Interfaz:
    def __init__(self):
        self.frameRelaciones = None
        self.dibujar()       
    def dibujar(self):
        ventana = tk.Tk()
        ventana.title('Auditoría Bases de Datos')
        ventana.geometry(str(anchoVentana)+'x'+str(altoVentana))
        ventana.resizable(width=True ,height =True)
        ventana.configure(background=colorBlanco)
        ventana.resizable(0,0)
        #ventana.iconbitmap('img/icono.ico')  icono
        center(ventana)

        # Frame global
        frameGlobal = Frame(ventana, width=anchoVentana, height=altoVentana, bg=colorBlanco,relief='sunken')
        frameGlobal.place(x=0,y=0)

        # --- Encabezado

        # Variables
        basesDatos = ['A','B']

        # Elemntos Interfaz
        encabezado = Frame(ventana, width=anchoVentana, height=70, bg=colorCeleste,relief='sunken')
        encabezado.place(x=0,y=0)
        labelTitulo = ttk.Label(encabezado, text="Auditoria de Bases de Datos para SQL Server - Grupo 3", background=colorCeleste, font=("Courie",14,'bold'))
        labelTitulo.place(x=180, y=20)       
        label1 = ttk.Label(frameGlobal, text="Seleccione la Base de Datos a analizar:", background=colorBlanco, font=("Courie",10))
        label1.place(x=40, y=90)
        comboBases=tk.ttk.Combobox(frameGlobal,values=basesDatos,width=9)
        comboBases.place(x=300,y=90)


        ventana.mainloop()

interfaz = Interfaz()
