#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  el_entrometido.py
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
import json
import time
import suite

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

pygame.display.set_caption("El entrometido")
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


def main():	
	"""loop principal"""
	suite.cargarDiccionario(diccionario_imagenes)
	nombre_usuario= suite.ingreso_usuario(13)
	tacho= Imagen((ANCHOCENTROVENTANA,50),DIRIMAGENES+"tacho.png","tacho")
	tacho.set_rect(200, 90)  
	puntos= 0
	pygame.mixer.music.play(-1, 0.0)
	aux=0 # indice que hace referencia a la letra a usar del diccionario
	screen.fill(random.choice(colores))
	suite.drawMensaje("HOLA "+nombre_usuario+ " !",ANCHOCENTROVENTANA-ANCHOBOTON,ALTOCENTROVENTANA-ALTOBOTON)
	pygame.display.flip()
	time.sleep(1)
	while True and aux!=5:           
		dicc_actual= seleccionDeImagenes(diccionario_imagenes, aux)
		lista_sprites= suite.inicializarImagenes(dicc_actual)
		copy = lista_sprites[1:]
		random.shuffle(copy)
		lista_sprites[1:] = copy
		tupla=tuple(lista_sprites[1:])
		puntos=correrJuego(tacho,random.choice(colores),lista_sprites[0], tupla , puntos)
		time.sleep(0.5)
		screen.fill(random.choice(colores))
		pygame.display.flip()
		if aux!=4:
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
	suite.modificoArchivoLog(datosJson,"logs_el_entrometido.json")	
	suite.pantallaLeaderboard("logs_el_entrometido.json")
	suite.drawMensaje("Apreta ENTER para continuar", ancho_ventana/2, alto_ventana - 50)
	pygame.display.flip()
	while True:
		for event in pygame.event.get():
			if (event.type == KEYUP):
				if event.key == K_RETURN:
					suite.pantallaInicio()																	


def correrJuego(tacho,color,letra,args,puntos):
	"""loop del juego al clickear en iniciar"""
	puntosAnt=0
	correcto=0
	consigna = '¿Cuales no empiezan con {}?'.format(os.path.splitext(letra.nombre)[0])
	msj = ""
	reproduccionMusica= True
	suite.drawScore(puntos)
	while True and correcto!=3:
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
					if objeto.toca(x,y):
						puntosAnt = puntos
						tupla=suite.evaluarTacho(tacho,objeto,letra,event,color,puntos,consigna,msj,correcto,True,args)
						puntos=tupla[0]
						correcto=tupla[1]
						if(puntosAnt>puntos):
							msj = 'UPS! Te equivocaste, {} empieza con {}!'.format(os.path.splitext(objeto.nombre)[0],letra.nombre)
							sonidoMal.play()
						elif(puntosAnt<puntos):
							msj = '¡Muy bien!, {} no empieza con {}!'.format(os.path.splitext(objeto.nombre)[0],letra.nombre)
							sonidoBien.play()		
		screen.fill(color)
		for objeto in args:
			if objeto.arrastra:
				screen.blit(objeto.image, objeto.rect)
		suite.drawScore(puntos)
		suite.drawMensaje("Tecla ESC: volver al menu, Tecla M: pausar musica", ancho_ventana-1280, alto_ventana-700)
		suite.drawMensaje(consigna, ancho_ventana-1250, alto_ventana-500)
		suite.drawMensaje(msj, 10, 300)
		screen.blit(tacho.image,tacho.rect)
		screen.blit(letra.image, (1000,100))
		
		clock.tick(60)
		pygame.display.flip()
	return puntos



def seleccionDeImagenes(dicc, aux):
	"""retorna diccionario cargado con 5 imagenes aleatorias"""
	dicc_aux={}
	if aux == 0:
		lis= random.sample(dicc["A"], 2)
		lis.append(random.sample(dicc["E"],1)[0])
		lis.append(random.sample(dicc["I"],1)[0])
		lis.append(random.sample(dicc["O"],1)[0])
		dicc_aux["A"]= lis
	elif aux == 1:
		lis= random.sample(dicc["E"], 2)
		lis.append(random.sample(dicc["A"],1)[0])
		lis.append(random.sample(dicc["O"],1)[0])
		lis.append(random.sample(dicc["I"],1)[0])
		dicc_aux["E"]= lis
	elif aux == 2:
		lis= random.sample(dicc["I"], 2)
		lis.append(random.sample(dicc["U"],1)[0])
		lis.append(random.sample(dicc["O"],1)[0])
		lis.append(random.sample(dicc["E"],1)[0])
		dicc_aux["I"]= lis
	elif aux == 3:
		lis= random.sample(dicc["O"], 2)
		lis.append(random.sample(dicc["A"],1)[0])
		lis.append(random.sample(dicc["E"],1)[0])
		lis.append(random.sample(dicc["I"],1)[0])
		dicc_aux["O"]= lis
	elif aux == 4:
		lis= random.sample(dicc["U"], 2)
		lis.append(random.sample(dicc["O"],1)[0])
		lis.append(random.sample(dicc["I"],1)[0])
		lis.append(random.sample(dicc["E"],1)[0])
		dicc_aux["U"]= lis
	return dicc_aux
