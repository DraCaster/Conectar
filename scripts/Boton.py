#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Boton.py
#  
#  Copyright 2019 Author: Lujan Rojas {lujanrojas.informatica@gmail.com}
#  
#  

class boton(object):
    """
    Esta clase boton contiene su inicializador, funciones de control, como si se pasa el cursor por el boton. Y tambien para colocar
    el boton en pantalla"""
    
    def __init__(self, color, colorSuave, display, texto, posIzquierda, posMedio, ancho, alto, colorTexto, posTexto, anchoCentroDisplay,
                 altoCentroDisplay, fuente):
        self.color=color
        self.colorSuave=colorSuave
        self.display=display
        self.texto=texto
        self.posIzquierda=posIzquierda
        self.posMedio=posMedio
        self.ancho=ancho
        self.alto=alto
        self.colorTexto=colorTexto
        self.posTexto=posTexto
        self.anchoCentroDisplay=anchoCentroDisplay
        self.altoCentroDisplay=altoCentroDisplay
        self.fuente=fuente
    
    def textoDisplay(self):
        """Coloca el texto sobre el boton en la pantalla"""
        textoDisplay = self.fuente.render(self.texto, True, self.colorTexto)
        self.display.blit(textoDisplay, [self.anchoCentroDisplay - (textoDisplay.get_rect().width / 2), self.altoCentroDisplay + (self.alto / 2) - (textoDisplay.get_rect().height / 2)+ self.posTexto])
        
    def mostrarBoton(self):
        """Coloca el boton en pantalla"""
        self.display.fill(self.color, (self.posIzquierda, self.posMedio, self.ancho, self.alto))
        self.textoDisplay()

    def toca(self, cursor):
        """Verifica si el cursor pasa por encima del boton"""
        if self.posIzquierda < cursor[0] < self.posIzquierda + self.ancho and self.posMedio < cursor[1] < self.posMedio + self.alto:
            self.display.fill(self.colorSuave, (self.posIzquierda, self.posMedio, self.ancho, self.alto))
            self.textoDisplay()
            return True
            
