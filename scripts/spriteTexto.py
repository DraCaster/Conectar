#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  spriteTexto.py
#  
#  Copyright 2019 Author: Lujan Rojas {lujanrojas.informatica@gmail.com}
#  
#  
import suite
import pygame
import os
from pygame.locals import *
class Texto(pygame.sprite.Sprite):
	
	"""Sprite de los textos en pantalla"""
	
	
	def __init__(self, position,fuente,msj, nombre):
		self.position=position
		pygame.sprite.Sprite.__init__(self)
		self.texto = fuente.render(msj, True, (255,255,255))
		self.rect = self.texto.get_rect()
		self.rect_aux=self.texto.get_rect()
		self.rect_aux.topleft=position
		self.rect.topleft=position
		self.nombre= nombre
		self.arrastra=True
	
	def set_rect_aux(self,tupla):
		"""Setea el texto en la posicion inicial"""
		self.rect_aux=tupla
		
	def toca(self, x, y):
		"""Verifica que el cursor del mouse se encuentre encima del texto"""
		return self.rect.collidepoint(x,y)
	
	def set_rect(self,ancho,alto):
		"""Setea el rectangulo"""
		self.rect.width=ancho
		self.rect.height=alto
	
	def get_rect(self):
		"""Retora el rectangulo"""
		return self.rect
		
	def update(self,pantalla):
		"""Mueve el texto en pantalla"""
		if pygame.mouse.get_pressed()[0]:
			x,y =pygame.mouse.get_pos()
			#x-=self.position[0]
			#y-=self.position[1]
			self.rect.x=x-70
			self.rect.y=y-10
			if len(self.nombre)<5:
				self.rect.x=x-30
				self.rect.y=y-10
			if len(self.nombre)<=3:
				self.rect.x=x-15
				self.rect.y=y-10
			if len(self.nombre)==1:
				self.rect.x=x-5
				self.rect.y=y-10
		if self.rect.left < 0:
			self.rect.left = 0
		elif self.rect.right > 1320:
			self.rect.right = 1320
		if self.rect.top <= 0:
			self.rect.top = 0
		elif self.rect.bottom >= 720:
			self.rect.bottom = 720  
			
	def handle_event(self, event,pantalla):
		"""Maneja el metodo update y verifica que no termine el progama"""
		if event.type == pygame.QUIT:
			suite.terminate()
		
		if event.type == pygame.MOUSEMOTION:
			self.update(pantalla)
		
