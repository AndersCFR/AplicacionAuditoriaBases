import tkinter as tk
from tkinter import*
from tkinter import ttk
from tkinter import messagebox
from turtle import bgcolor
from PIL import ImageTk, Image
from tkinter import PhotoImage
from PIL import Image,ImageTk
from hamcrest import empty
from datetime import datetime

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
        self.gestorDatos.borrarStoredProcedures()
        self.gestorDatos.crearStoredProcedures()

    # Verificaci??n de selecci??n de base
    def sinSeleccionarBase(self):
        if self.gestorDatos.baseActual == None:
            messagebox.showerror(message=f'No se ha seleccionado ninguna base de datos', title='Error')
            return True
        else: return False

    def escribirLog(self, titulo, encabezado, cuerpo):
        with open('log.txt', 'a') as file:
            file.write(f'''{'*'*50}
Fecha y hora del an??lisis: {datetime.now()}
Base de datos: {self.gestorDatos.baseActual}
Servidor: {self.gestorDatos.direccion_servidor}
Usuario: {self.gestorDatos.nombre_usuario}\n''')
            header = '-'*20 + titulo + '-'*20 + '\n'
            file.write(header)
            # Cabecera de la tabla
            for h in encabezado:
                file.write('{0: <35}'.format(h))
            file.write('\n')
            # Contenido de la tabla
            for fila in cuerpo:
                for dato in fila:
                    file.write('{0: <35}'.format(dato))
                file.write('\n')
            end = '-'*40 + '\n\n'
            file.write(end)
            messagebox.showinfo(message=f'Log generado correctamente', title='Log')


    def dibujar(self):
        ventana = tk.Tk()
        ventana.title('Auditor??a Bases de Datos')
        ventana.geometry(str(anchoVentana)+'x'+str(altoVentana))
        ventana.resizable(width=True ,height =True)
        ventana.configure(background=colorBlanco)
        ventana.resizable(0,0)
        ventana.iconbitmap('../img/icono.ico')
        center(ventana)

# -------  Creaci??n Frames   ------------------------
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

        btnRelInexistentes = Button(frameGlobal,text= 'Relaciones que deber??an existir',font=("Courie",9,'bold'),command=self.mostrarFrameRelInexistentes, width=26, height=2, bd= 2,bg=colorBlanco, relief=GROOVE, highlightbackground=colorNegro)
        btnRelInexistentes.place(x=240,y=140)

        btnRelInexistentes = Button(frameGlobal,text= 'Triggers deshabilitado',font=("Courie",9,'bold'),command=self.mostrarFrameTriggers, width=20, height=2, bd= 2,bg=colorBlanco, relief=GROOVE, highlightbackground=colorNegro)
        btnRelInexistentes.place(x=460,y=140)

        btnRelInexistentes = Button(frameGlobal,text= 'Datos An??malos',font=("Courie",9,'bold'),command=self.mostrarFrameDatosAnomalos, width=26, height=2, bd= 2,bg=colorBlanco, relief=GROOVE, highlightbackground=colorNegro)
        btnRelInexistentes.place(x=640,y=140)

# ----------------------------------------------------------------------- #
#                        Frame Relaciones deshabilitadas
# ------------------------------------------------------------------------ #

        style = ttk.Style(ventana)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background=colorCeleste, foreground=colorNegro)

        #Variables

        #Elementos GUI     
        label2 = ttk.Label(self.frameRelaDeshabilitadas, text="Relaciones existentes en la base de datos, pero que se encuentran deshabilitadas:",
                             background=colorBlanco, font=("Courie",10))
        label2.place(x=40, y=20)
               
        #tabla
        columnsT1 = ('Restricci??n de Clave For??nea','Nombre Tabla Hijo','Nombre Tabla Padre','??Est?? deshabilitado?')
        tabla1 = ttk.Treeview(self.frameRelaDeshabilitadas, height=15,columns=columnsT1,show='headings')
        tabla1.place(x=40,y=50)     

        for heading in columnsT1:            
            tabla1.heading(heading, text=heading)
            tabla1.column(heading,minwidth=0,width=180,stretch=NO)
        
        ladoy = Scrollbar(self.frameRelaDeshabilitadas, orient =VERTICAL, command = tabla1.yview)
        ladoy.place(x=765,y=50)
        ladoy.set(20,200)
        tabla1.configure(yscrollcommand=ladoy.set)

        def exportarLOGRelDeshabilitadas():
            data = self.gestorDatos.execRelacionesDeshabilitadas()
            if data == []:
                data = [['No se encontraron relaciones deshabilitadas']]
            self.escribirLog('Relaciones deshabilitadas',columnsT1,data)

        
        btnLogRelDeshabilitadas = Button(self.frameRelaDeshabilitadas,text= 'Generar LOG',font=("Courie",9,'bold'),command=exportarLOGRelDeshabilitadas, width=15, height=1, bd= 2,bg=colorCeleste, relief=GROOVE, highlightbackground=colorNegro)
        btnLogRelDeshabilitadas.config(state=tk.DISABLED)
        btnLogRelDeshabilitadas.place(x=700,y=20)

        def llenarData():
            if self.sinSeleccionarBase() == False:
                tabla1 = ttk.Treeview(self.frameRelaDeshabilitadas, height=15,columns=columnsT1,show='headings')
                tabla1.place(x=40,y=50)     
                for heading in columnsT1:            
                    tabla1.heading(heading, text=heading)
                    tabla1.column(heading,minwidth=0,width=180,stretch=NO)

                data = self.gestorDatos.execRelacionesDeshabilitadas()
                if data == []:
                    data = [['No se encontraron relaciones deshabilitadas']]
                    messagebox.showinfo(message=f'No existen relaciones deshabilitadas', title='Enhorabuena')
                else:                
                    for fila in data: 
                        tabla1.insert('', 'end', values =fila)
                # Habilitar boton log
                btnLogRelDeshabilitadas.config(state=tk.NORMAL)
                
        
      

        btnExecRelDeshabilitadas = Button(self.frameRelaDeshabilitadas,text= 'Analizar',font=("Courie",9,'bold'),command=llenarData, width=10, height=1, bd= 2,bg=colorCeleste, relief=GROOVE, highlightbackground=colorNegro)
        btnExecRelDeshabilitadas.place(x=600,y=20)

      

# ----------------------------------------------------------------------- #
#                        Frame Relaciones inexistentes
# ------------------------------------------------------------------------ #

        #Variables

        #Elementos GUI     
        label3 = ttk.Label(self.frameRelaInexistentes, text='Posibles anomal??as entre tablas de la base de datos con relaciones no existentes:',
                             background=colorBlanco, font=("Courie",10))
        label3.place(x=40, y=20)
        
        #tabla
        columnsT2 = ('Tabla Analizada','Columna con Nombre Repetido','Posible Relaci??n que Deber??a Crearse')
        tabla2 = ttk.Treeview(self.frameRelaInexistentes, height=15,columns=columnsT2,show='headings')
        tabla2.place(x=40,y=50)
    
        for head in columnsT2:  
            tabla2.heading(head, text=head)
            tabla2.column(head,minwidth=0,width=240,stretch=NO)
        
        ladoy2 = Scrollbar(self.frameRelaInexistentes, orient =VERTICAL, command = tabla2.yview)
        ladoy2.place(x=765,y=50)
        ladoy2.set(20,200)
        tabla2.configure(yscrollcommand=ladoy2.set)

        def exportarLOGRelInexistentes():
            data = self.gestorDatos.execPosiblesRelaciones()
            if data == []:
                data = [['No se encontraron posibles relaciones inexistentes']]
            else:
                for fila in data:
                    if fila[2] == None:
                        fila[2] = 'Sin posible tabla de relaci??n'
            self.escribirLog('Relaciones inexistentes',columnsT2,data)

        btnLogRelInexistentes = Button(self.frameRelaInexistentes,text= 'Generar LOG',font=("Courie",9,'bold'),command=exportarLOGRelInexistentes, width=15, height=1, bd= 2,bg=colorCeleste, relief=GROOVE, highlightbackground=colorNegro)
        btnLogRelInexistentes.config(state=tk.DISABLED)
        btnLogRelInexistentes.place(x=700,y=20)

        def llenarData2():
            if self.sinSeleccionarBase() == False:
                tabla2 = ttk.Treeview(self.frameRelaInexistentes, height=15,columns=columnsT2,show='headings')
                tabla2.place(x=40,y=50)
                for head in columnsT2:  
                    tabla2.heading(head, text=head)
                    tabla2.column(head,minwidth=0,width=240,stretch=NO)

                data = self.gestorDatos.execPosiblesRelaciones()
                if data == []:
                    messagebox.showinfo(message=f'No se encontraron posibles relaciones inexistentes', title='Enhorabuena')
                for fila in data:             
                    dato = fila
                    if dato[2] == None:
                        dato[2] = 'Sin posible tabla de relaci??n'          
                    tabla2.insert('', 'end', values=dato)
                btnLogRelInexistentes.config(state=tk.NORMAL)

        btnExecRelInexistentes = Button(self.frameRelaInexistentes,text= 'Analizar',font=("Courie",9,'bold'),command=llenarData2, width=10, height=1, bd= 2,bg=colorCeleste, relief=GROOVE, highlightbackground=colorNegro)
        btnExecRelInexistentes.place(x=600,y=20)



# ----------------------------------------------------------------------- #
#                        Frame Triggers
# ------------------------------------------------------------------------ #

        #Variables

        #Elementos GUI     
        label4 = ttk.Label(self.frameTriggers, text='Triggers existentes en la base de datos, pero que se encuentran deshabilitados:',
                             background=colorBlanco, font=("Courie",10))
        label4.place(x=40, y=20)

         #tabla
        columnsT3 = ('Nombre del Trigger','Acci??n','Tabla perteneciente','??Est?? Deshabilitado?')
        tabla3 = ttk.Treeview(self.frameTriggers, height=15,columns=columnsT3,show='headings')
        tabla3.place(x=40,y=50)
    
        for head in columnsT3:  
            tabla3.heading(head, text=head)
            tabla3.column(head,minwidth=0,width=200,stretch=NO)
        
        ladoy3 = Scrollbar(self.frameTriggers, orient =VERTICAL, command = tabla3.yview)
        ladoy3.place(x=850,y=50)
        ladoy3.set(20,200)
        tabla3.configure(yscrollcommand=ladoy3.set)

        def exportarLOGTrigger():
            data = self.gestorDatos.execTriggersDeshabilitados()
            if data == []:
                data = [['No se encontr?? ning??n trigger deshabilitado']]
            self.escribirLog('Triggers deshabilitados',columnsT3,data)

        btnLogTrigger = Button(self.frameTriggers,text= 'Generar LOG',font=("Courie",9,'bold'),command=exportarLOGTrigger, width=15, height=1, bd= 2,bg=colorCeleste, relief=GROOVE, highlightbackground=colorNegro)
        btnLogTrigger.config(state=tk.DISABLED)
        btnLogTrigger.place(x=700,y=20)

        def llenarData3():    
            if self.sinSeleccionarBase() == False:      
                tabla3 = ttk.Treeview(self.frameTriggers, height=15,columns=columnsT3,show='headings')
                tabla3.place(x=40,y=50)
        
                for head in columnsT3:  
                    tabla3.heading(head, text=head)
                    tabla3.column(head,minwidth=0,width=200,stretch=NO)

                data = self.gestorDatos.execTriggersDeshabilitados()
                if data == []:
                    messagebox.showinfo(message=f'No se encontr?? ning??n trigger deshabilitado', title='Enhorabuena')
                for fila in data:             
                    dato = fila           
                    tabla3.insert('', 'end', values=dato)
                # Habilitar boton log
                btnLogTrigger.config(state=tk.NORMAL)

        btnExecTrigger = Button(self.frameTriggers,text= 'Analizar',font=("Courie",9,'bold'),command=llenarData3, width=10, height=1, bd= 2,bg=colorCeleste, relief=GROOVE, highlightbackground=colorNegro)
        btnExecTrigger.place(x=600,y=20)




# ----------------------------------------------------------------------- #
#                        Frame Datos Anomalos
# ------------------------------------------------------------------------ #

        #Variables

        #Elementos GUI     
        label5 = ttk.Label(self.frameDatosAnomalos, text='Se encontraron los siguientes datos an??malos:',
                             background=colorBlanco, font=("Courie",10))
        label5.place(x=40, y=20)

                #tabla
        columnsT4 = ('Nombre de la Tabla','Restricci??n','Dato An??malo')
        tabla4 = ttk.Treeview(self.frameDatosAnomalos, height=15,columns=columnsT4,show='headings')
        tabla4.place(x=40,y=50)
    
        for head in columnsT4:  
            tabla4.heading(head, text=head)
            tabla4.column(head,minwidth=0,width=220,stretch=NO)
        
        ladoy4 = Scrollbar(self.frameDatosAnomalos, orient =VERTICAL, command = tabla4.yview)
        ladoy4.place(x=710,y=50)
        ladoy4.set(20,200)
        tabla4.configure(yscrollcommand=ladoy4.set)

        def exportarLOGDatosAnomalos():
            data = self.gestorDatos.execChequeoAutomatico()
            if data == []:
                data = [['No se encontraron datos an??malos']]
            self.escribirLog('Datos an??malos',columnsT4,data)

        btnLogDatosAnomalos = Button(self.frameDatosAnomalos,text= 'Generar LOG',font=("Courie",9,'bold'),command=exportarLOGDatosAnomalos, width=15, height=1, bd= 2,bg=colorCeleste, relief=GROOVE, highlightbackground=colorNegro)
        btnLogDatosAnomalos.config(state=tk.DISABLED)
        btnLogDatosAnomalos.place(x=700,y=20)

        def llenarData4():
            if self.sinSeleccionarBase() == False:
                tabla4 = ttk.Treeview(self.frameDatosAnomalos, height=15,columns=columnsT4,show='headings')
                tabla4.place(x=40,y=50)
                for head in columnsT4:  
                    tabla4.heading(head, text=head)
                    tabla4.column(head,minwidth=0,width=220,stretch=NO)
                data = self.gestorDatos.execChequeoAutomatico()
                if data == []:
                    messagebox.showinfo(message=f'No se encontraron datos an??malos', title='Enhorabuena')
                for fila in data:             
                    dato = fila                  
                    tabla4.insert('', 'end', values=dato)
                # Habilitar boton log
                btnLogDatosAnomalos.config(state=tk.NORMAL)

        btnExecTrigger = Button(self.frameDatosAnomalos,text= 'Analizar',font=("Courie",9,'bold'),command=llenarData4, width=10, height=1, bd= 2,bg=colorCeleste, relief=GROOVE, highlightbackground=colorNegro)
        btnExecTrigger.place(x=600,y=20)




# ------- Main loop --------------------#        
        ventana.mainloop()

