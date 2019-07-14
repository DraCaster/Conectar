#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  spriteImagen.py
#  
#  Copyright 2019 Author: Lujan Rojas {lujanrojas.informatica@gmail.com}
#  
#  
import suite
import pygame
import os
from pygame.locals import *
class Imagen(pygame.sprite.Sprite):
	
	"""Sprite de las imagenes en pantalla"""
	
	
	def __init__(self, position,imagen, nombre, path= os.getcwd()):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(imagen)
		self.rect = self.image.get_rect()
		self.rect_aux=position
		self.rect.topleft=position
		self.nombre= nombre
		self.arrastra=True
	
	def set_rect_aux(self,tupla):
		"""Setea la imagen en la posicion inicial"""
		self.rect_aux=tupla
		
	def toca(self, x, y):
		"""Verifica que el cursor del mouse se encuentre encima de la imagen"""
		return self.rect.collidepoint(x,y)
	
	def set_rect(self,ancho,alto):
		"""Setea el rectangulo"""
		self.rect.width=ancho
		self.rect.height=alto
	
	def get_rect(self):
		"""Retora el rectangulo"""
		return self.rect
		
	def update(self,pantalla):
		"""Mueve la imagen en pantalla"""
		if pygame.mouse.get_pressed()[0]:
			x,y =pygame.mouse.get_pos()
			x-=100
			y-=100	
			self.rect.x=x
			self.rect.y=y
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
		
