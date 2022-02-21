# Inicialización objeto interfaz

from interfaz import Interfaz
from baseDatos import BaseDatos

interfaz = Interfaz()

bd = BaseDatos()
bd.conectarSinBase()
interfaz.setGestorDatos(bd)

interfaz.dibujar()