import tkinter as tk
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from tkinter import PhotoImage
from PIL import Image,ImageTk

global colorCeleste
colorCeleste = '#C6EBFF'
global colorBlanco
colorBlanco = '#F7F7F7'
global colorNegro
colorNegro = '#000000'
global anchoVentana
anchoVentana = 900
global altoVentana
altoVentana = 600
global alotSubFrames
altoSubFrames = 400

posicionFrames = (0,200)

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

def cargarImg(root, file, size: tuple, place: tuple):
    img=Image.open(file)
    img=img.resize(size,Image.ANTIALIAS)
    img.save(file)
    img=PhotoImage(master=root,file=file)
    panel=ttk.Label(root,image=img)
    panel.image = img
    panel.place(x=place[0],y=place[1])

class Interfaz:
    def __init__(self):
        # Frames
        self.frameRelaDeshabilitadas = None            
        self.frameRelaInexistentes = None
        self.frameTriggers =  None
        self.frameDatosAnomalos = None
        # Modelo bases de datos
        self.gestorDatos = None    
        #self.dibujar()  

    def setGestorDatos(self, gestorDatos):
        self.gestorDatos = gestorDatos

    def mostrarFrameRelDeshabilitadas(self):
        self.ocultarOtrosFrames()
        self.frameRelaDeshabilitadas.place(x=posicionFrames[0], y=posicionFrames[1])
    
    def mostrarFrameRelInexistentes(self):
        self.ocultarOtrosFrames()
        self.frameRelaInexistentes.place(x=posicionFrames[0], y=posicionFrames[1])
    
    def mostrarFrameTriggers(self):
        self.ocultarOtrosFrames()
        self.frameTriggers.place(x=posicionFrames[0], y=posicionFrames[1])

    def mostrarFrameDatosAnomalos(self):
        self.ocultarOtrosFrames()
        self.frameDatosAnomalos.place(x=posicionFrames[0], y=posicionFrames[1])
    
    def ocultarOtrosFrames(self):                
        self.frameRelaDeshabilitadas.place_forget() 
        self.frameRelaInexistentes.place_forget() 
        self.frameTriggers.place_forget()
        self.frameDatosAnomalos.place_forget()

    def conectarBaseDatos(self, event):
        base = self.comboBases.get()
        self.gestorDatos.conectarConBase(base)

    def dibujar(self):
        ventana = tk.Tk()
        ventana.title('Auditoría Bases de Datos')
        ventana.geometry(str(anchoVentana)+'x'+str(altoVentana))
        ventana.resizable(width=True ,height =True)
        ventana.configure(background=colorBlanco)
        ventana.resizable(0,0)
        ventana.iconbitmap('../img/icono.ico')
        center(ventana)

# -------  Creación Frames   ------------------------
        frameGlobal = Frame(ventana, width=anchoVentana, height=altoVentana, bg='#FFFFFF',relief='sunken')
        frameGlobal.place(x=0,y=0)

        self.frameRelaInexistentes = Frame(frameGlobal, width = anchoVentana, height=altoSubFrames, 
                    bg= colorBlanco, relief ='sunken')
        self.frameRelaInexistentes.place(x=posicionFrames[0], y=posicionFrames[1])


        self.frameTriggers = Frame(frameGlobal, width = anchoVentana, height=altoSubFrames, 
                    bg= colorBlanco, relief ='sunken')
        self.frameTriggers.place(x=posicionFrames[0], y=posicionFrames[1])


        self.frameDatosAnomalos = Frame(frameGlobal, width = anchoVentana, height=altoSubFrames, 
                    bg= colorBlanco, relief ='sunken')
        self.frameDatosAnomalos.place(x=posicionFrames[0], y=posicionFrames[1])

        self.frameRelaDeshabilitadas = Frame(frameGlobal, width = anchoVentana, height=altoSubFrames, 
                    bg= colorBlanco, relief ='sunken')
        self.frameRelaDeshabilitadas.place(x=posicionFrames[0], y=posicionFrames[1])

# ----------------------------------------------------------------------- #
#                               Encabezado
# ------------------------------------------------------------------------ #

        # Variables
        basesDatos = self.gestorDatos.getBasesExistentes()

        # Elementos Interfaz
        encabezado = Frame(ventana, width=anchoVentana, height=70, bg=colorCeleste,relief='sunken')
        encabezado.place(x=0,y=0)
        labelTitulo = ttk.Label(encabezado, text="Auditoria de Bases de Datos para SQL Server - Grupo 3", background=colorCeleste, font=("Courie",14,'bold'))
        labelTitulo.place(x=180, y=20)       
        label1 = ttk.Label(frameGlobal, text="Seleccione la Base de Datos a analizar:", background='#FFFFFF', font=("Courie",10))
        label1.place(x=40, y=90)
        self.comboBases=tk.ttk.Combobox(frameGlobal,values=basesDatos,width=30)
        self.comboBases.place(x=300,y=90)
        self.comboBases.bind('<<ComboboxSelected>>', self.conectarBaseDatos)

        #logoEPN
        cargarImg(encabezado,'../img/logo-EPN.png',(50,50),(30,8))
        #logoFIS
        cargarImg(encabezado,'../img/logo-FIS.png',(50,50),(800,8))
        
        #botones
        btnRelDeshabilitadas = Button(frameGlobal,text= 'Relaciones deshabilitadas',font=("Courie",9,'bold'),command=self.mostrarFrameRelDeshabilitadas, width=22, height=2, bd= 2,bg=colorBlanco, relief=GROOVE, highlightbackground=colorNegro)
        btnRelDeshabilitadas.place(x=50,y=140)

        btnRelInexistentes = Button(frameGlobal,text= 'Relaciones que deberían existir',font=("Courie",9,'bold'),command=self.mostrarFrameRelInexistentes, width=26, height=2, bd= 2,bg=colorBlanco, relief=GROOVE, highlightbackground=colorNegro)
        btnRelInexistentes.place(x=240,y=140)

        btnRelInexistentes = Button(frameGlobal,text= 'Triggers deshabilitado',font=("Courie",9,'bold'),command=self.mostrarFrameTriggers, width=20, height=2, bd= 2,bg=colorBlanco, relief=GROOVE, highlightbackground=colorNegro)
        btnRelInexistentes.place(x=460,y=140)

        btnRelInexistentes = Button(frameGlobal,text= 'Datos Anómalos',font=("Courie",9,'bold'),command=self.mostrarFrameDatosAnomalos, width=26, height=2, bd= 2,bg=colorBlanco, relief=GROOVE, highlightbackground=colorNegro)
        btnRelInexistentes.place(x=640,y=140)

# ----------------------------------------------------------------------- #
#                        Frame Relaciones deshabilitadas
# ------------------------------------------------------------------------ #

        #Variables

        #Elementos GUI     
        label2 = ttk.Label(self.frameRelaDeshabilitadas, text="Relaciones existentes en la base de datos, pero que se encuentran deshabilitadas:",
                             background=colorBlanco, font=("Courie",10))
        label2.place(x=40, y=20)

# ----------------------------------------------------------------------- #
#                        Frame Relaciones inexistentes
# ------------------------------------------------------------------------ #

        #Variables

        #Elementos GUI     
        label3 = ttk.Label(self.frameRelaInexistentes, text='Posibles anomalías entre tablas de la base de datos con relaciones no existentes:',
                             background=colorBlanco, font=("Courie",10))
        label3.place(x=40, y=20)


# ----------------------------------------------------------------------- #
#                        Frame Triggers
# ------------------------------------------------------------------------ #

        #Variables

        #Elementos GUI     
        label4 = ttk.Label(self.frameTriggers, text='Triggers existentes en la base de datos, pero que se encuentran deshabilitados:',
                             background=colorBlanco, font=("Courie",10))
        label4.place(x=40, y=20)


# ----------------------------------------------------------------------- #
#                        Frame Datos Anomalos
# ------------------------------------------------------------------------ #

        #Variables

        #Elementos GUI     
        label5 = ttk.Label(self.frameDatosAnomalos, text='Se encontraron los siguientes datos anómalos::',
                             background=colorBlanco, font=("Courie",10))
        label5.place(x=40, y=20)


# ------- Main loop --------------------#        
        ventana.mainloop()

