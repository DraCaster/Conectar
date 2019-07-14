#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  acomodo_y_formo_letras.py
#  
#  Copyright 2019 Author: Lujan Rojas {lujanrojas.informatica@gmail.com}
#  
#  
import time, Boton, suite
import sys
import pygame
from pygame.locals import *
from spriteImagen import *
from itertools import cycle
import random
import time
import json
 

ROJOCLARO = (255,   0,   0)
ROJO = (155,   0,   0)
VERDECLARO = (  0, 255,   0)
VERDE = (  0, 155,   0)
AZULCLARO = (  0,   0, 255)
AZUL = (  0,   0, 155)
BLANCO = (255, 255, 255)
NEGRO= (0, 0, 0)

colores=[ROJOCLARO,VERDECLARO,AZULCLARO,VERDE]

pygame.init()
pygame.display.set_icon(pygame.image.load("../imagenes/Letras/a_letra_A.png"))

ancho_ventana = 1320
alto_ventana = 720

pygame.display.set_caption("Conectar")

clock = pygame.time.Clock()

BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
BASICFONT_NOMBRE = pygame.font.Font('freesansbold.ttf', 30)

ANCHOBOTON=150
ALTOBOTON=50
ANCHOCENTROVENTANA= ancho_ventana / 2
ALTOCENTROVENTANA= alto_ventana / 2
FUENTEBOTON=pygame.font.SysFont("comicsansms", 25)
FUENTECONSIGNA = pygame.font.Font("../fuentes/Candy Beans.otf", 30)

screen = pygame.display.set_mode((ancho_ventana, alto_ventana))

DIRIMAGENES= "../imagenes/"

LISTA_DIR_IMAGENES= ["../imagenes/A/", "../imagenes/E/", "../imagenes/I/", "../imagenes/O/", "../imagenes/U/"] 


diccionario_imagenes= {}

pygame.mixer.music.set_volume(0.5)
sonidoBien = pygame.mixer.Sound('../sonidos/ok.wav')
sonidoMal = pygame.mixer.Sound('../sonidos/notok.wav')
pygame.mixer.music.load('../sonidos/Sand_Castle.mp3')
 

 
def main(nombre_usuario):	
	"""loop principal"""
	suite.cargarDiccionario(diccionario_imagenes)
	puntos= 0
	pygame.mixer.music.play(-1, 0.0)
	aux=0 # indice que hace referencia a la letra a usar del diccionario
	pygame.display.flip()
	time.sleep(1)
	while True and aux != 3:           
		dicc_actual= seleccionDeImagenes(diccionario_imagenes, aux)
		lista_sprites= suite.inicializarImagenesLetras(dicc_actual)
		puntos=correrJuego(random.choice(colores),lista_sprites[0][0], lista_sprites , puntos)
		time.sleep(0.5)
		screen.fill(random.choice(colores))
		pygame.display.flip()
		if aux!=2:
			suite.drawMensaje("MUY BIEN!", ancho_ventana/2.4, alto_ventana/3.5)
			suite.drawMensaje("SIGUIENTE NIVEL", ancho_ventana/2.4, alto_ventana/3)
			pygame.display.flip()
		time.sleep(1)
																						
		aux+=1		
	screen.fill(random.choice(colores))	
	suite.drawMensaje("FIN DEL JUEGO",((ancho_ventana/2)-ANCHOBOTON)+20,alto_ventana/3.5)	
	suite.drawMensaje("Tu puntaje fue: "+ str(puntos),(ancho_ventana/2)-ANCHOBOTON,alto_ventana/3)
	datosJson =[
					{
						"nombre": nombre_usuario,
						"puntaje_maximo": puntos,
						"fecha": time.strftime("%x"),
						"hora": time.strftime("%X")
					}
				]	
	suite.modificoArchivoLog(datosJson,"logs_acomodo_y_formo_con_letra.json")	
	suite.pantallaLeaderboard("logs_acomodo_y_formo_con_letra.json")
	suite.drawMensaje("apreta enter para continuar", ancho_ventana/2, alto_ventana - 50)
	pygame.display.flip()
	while True:
		for event in pygame.event.get():
			if (event.type == KEYUP):
				if event.key == K_RETURN:
					suite.pantallaInicio()																	
			if event.type == pygame.QUIT:
				suite.terminate()

def correrJuego(color,letra,args,puntos):
	"""loop del juego al clickear en iniciar"""
	args[0][0].rect.topleft=(100,200)
	args[1][0].rect.topleft=(1040,200)
	puntosAnt=0
	correcto=0
	consigna = 'Coloca la palabra en su lugar'
	msj = ""
	total=0
	reproduccionMusica= True
	suite.drawScore(puntos)
	for valor in args:
		total=total+len(valor[0].nombre.replace('.png', ''))
	while True and correcto!=total:
		screen.fill(color)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				suite.terminate()
			if (event.type == KEYUP):
				if event.key == K_ESCAPE:
					suite.pantallaInicio()
				if event.key == K_m:
					if reproduccionMusica:
						pygame.mixer.music.pause()
						reproduccionMusica= False
					else:
						pygame.mixer.music.unpause()
						reproduccionMusica= True
			x,y=pygame.mouse.get_pos()
			if pygame.mouse.get_pressed()[0]:
				for objeto in args:
					valor_lis=0
					for valor in objeto[2]:
						if valor.toca(x,y):
							puntosAnt = puntos
							tupla=suite.evaluar_lugar_letra(valor,objeto[1][valor_lis],event,color,puntos,consigna,msj,correcto,True,args)
							puntos=tupla[0]
							correcto=tupla[1]
						valor_lis+=1
		for objeto in args:
			screen.blit(objeto[0].image, objeto[0].rect)
			for i in objeto[1]:
				screen.blit(i.image,i.rect)
		for objeto in args:
			for i in objeto[2]:
				screen.blit(i.texto,i.rect)
		suite.drawScore(puntos)
		suite.drawMensaje(consigna, ancho_ventana-1250, alto_ventana-600)
		suite.drawMensaje("Tecla ESC: volver al menu, Tecla M: pausar musica", ancho_ventana-1280, alto_ventana-700)
		
		clock.tick(60)
		pygame.display.flip()
	return puntos


def seleccionDeImagenes(dicc, aux):
	"""retorna diccionario cargado con 2 imagenes aleatorias"""
	lis_aux=["A","E","I","O","U"]
	lis=[]
	dicc_aux={}
	if aux == 0:
		for i in range(2):
			valor=random.choice(lis_aux)
			imagen=random.sample(dicc[valor],1)[0]
			lis.append(imagen)
			lis_aux.remove(valor)
			dicc[valor].remove(imagen)
			
		dicc_aux[1]= lis
	if aux == 1:
		for i in range(2):
			valor=random.choice(lis_aux)
			imagen=random.sample(dicc[valor],1)[0]
			lis.append(imagen)
			lis_aux.remove(valor)
			dicc[valor].remove(imagen)
			
		dicc_aux[1]= lis
	if aux == 2:
		for i in range(2):
			valor=random.choice(lis_aux)
			imagen=random.sample(dicc[valor],1)[0]
			lis.append(imagen)
			lis_aux.remove(valor)
			dicc[valor].remove(imagen)
			
		dicc_aux[1]= lis
	if aux == 3:
		for i in range(2):
			valor=random.choice(lis_aux)
			imagen=random.sample(dicc[valor],1)[0]
			lis.append(imagen)
			lis_aux.remove(valor)
			dicc[valor].remove(imagen)
			
		dicc_aux[1]= lis
	if aux == 4:
		for i in range(2):
			valor=random.choice(lis_aux)
			imagen=random.sample(dicc[valor],1)[0]
			lis.append(imagen)
			lis_aux.remove(valor)
			dicc[valor].remove(imagen)
			
		dicc_aux[1]= lis

	return dicc_aux                                   
