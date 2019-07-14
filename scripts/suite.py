
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  suite.py
#  
#  Copyright 2019 Author: Lujan Rojas {lujanrojas.informatica@gmail.com}
#  
#  

import come_vocales, pygame, el_entrometido, Boton, random, sys, cada_una_en_su_lugar, os,acomodo_y_formo_letras,acomodo_y_formo_con_silabas
import time, Boton, suite
import sys
import pygame
import string
from pygame.locals import *
from spriteImagen import *
from itertools import cycle
import random
import json
from spriteTexto import *
import separasilabas
ROJO = (255,   0,   0)
NARANJACLARO = (255, 172, 64)
VERDECLARO = (  0, 255,   0)
VERDE = (  0, 155,   0)
AZULCLARO = (  0,   0, 255)
AZUL = (  0,   0, 155)
BLANCO = (255, 255, 255)
NEGRO= (0, 0, 0)
CELESTE = (64, 137, 255)


colores=[CELESTE,VERDECLARO,NARANJACLARO,VERDE]
pygame.init()
pygame.display.set_icon(pygame.image.load("../imagenes/Letras/a_letra_A.png"))

ancho_ventana = 1320
alto_ventana = 720

pygame.display.set_caption("Conectar")

clock = pygame.time.Clock()

FUENTE_BASICA = pygame.font.Font('freesansbold.ttf', 18)
FUENTE_BASICA_2 = pygame.font.Font('freesansbold.ttf', 25)
FUENTE_BASICA_NOMBRE = pygame.font.Font('freesansbold.ttf', 30)

ANCHOBOTON=150
ALTOBOTON=50
ANCHOCENTROVENTANA= ancho_ventana / 2
ALTOCENTROVENTANA= alto_ventana / 2


FUENTEBOTON=pygame.font.SysFont("comicsansms", 25)
FUENTECONSIGNA = pygame.font.Font("../fuentes/Candy Beans.otf", 30)
screen = pygame.display.set_mode((ancho_ventana, alto_ventana))
DIRIMAGENES= "../imagenes/"
DIRGRABACIONES= "../sonidos/grabados/"


sonidoBien = pygame.mixer.Sound('../sonidos/ok.wav')
sonidoMal = pygame.mixer.Sound('../sonidos/notok.wav')

botonAcomodoYFormo = Boton.boton(ROJO, AZUL, screen, "Acomodo y formo", ANCHOCENTROVENTANA - (ANCHOBOTON / 2) - 55,
                            ALTOCENTROVENTANA - 240, ANCHOBOTON + 110, ALTOBOTON, BLANCO, -240, ANCHOCENTROVENTANA,
                            ALTOCENTROVENTANA, FUENTEBOTON)

botonComeVocales = Boton.boton(ROJO, AZUL, screen, "Come vocales", ANCHOCENTROVENTANA - (ANCHOBOTON / 2) - 55,
                            ALTOCENTROVENTANA - 30, ANCHOBOTON + 110, ALTOBOTON, BLANCO, -30, ANCHOCENTROVENTANA,
                            ALTOCENTROVENTANA, FUENTEBOTON)
botonConSilabas = Boton.boton(ROJO, AZUL, screen, "Con Silabas", ANCHOCENTROVENTANA - (ANCHOBOTON / 2) - 55,
                            ALTOCENTROVENTANA - 100, ANCHOBOTON + 110, ALTOBOTON, BLANCO, -100, ANCHOCENTROVENTANA,
                            ALTOCENTROVENTANA, FUENTEBOTON)

botonConLetras = Boton.boton(ROJO, AZUL, screen, "Con Letras", ANCHOCENTROVENTANA - (ANCHOBOTON / 2) - 55,
                            ALTOCENTROVENTANA - 0, ANCHOBOTON + 110, ALTOBOTON, BLANCO, 0, ANCHOCENTROVENTANA,
                            ALTOCENTROVENTANA, FUENTEBOTON)

botonEntrometido = Boton.boton(ROJO, AZUL, screen, "El entrometido", ANCHOCENTROVENTANA - (ANCHOBOTON / 2) - 55,
                            ALTOCENTROVENTANA - 100, ANCHOBOTON + 110, ALTOBOTON, BLANCO, -100, ANCHOCENTROVENTANA,
                            ALTOCENTROVENTANA, FUENTEBOTON)

botonSalir = Boton.boton(ROJO, AZUL, screen, "Salir", ANCHOCENTROVENTANA - (ANCHOBOTON / 2) - 55,
                           ALTOCENTROVENTANA + 50, ANCHOBOTON +110, ALTOBOTON, BLANCO, 50, ANCHOCENTROVENTANA,
                           ALTOCENTROVENTANA, FUENTEBOTON)
botonVolver = Boton.boton(ROJO, AZUL, screen, "Volver al menu", ANCHOCENTROVENTANA - (ANCHOBOTON / 2) - 55,
                            ALTOCENTROVENTANA +100, ANCHOBOTON + 110 , ALTOBOTON, BLANCO, 100, ANCHOCENTROVENTANA,
                            ALTOCENTROVENTANA, FUENTEBOTON)

botonCadaUnaEnSuLugar = Boton.boton(ROJO, AZUL, screen, "Cada uno en su lugar", ANCHOCENTROVENTANA - (ANCHOBOTON / 2) - 55,
                            ALTOCENTROVENTANA - 170, ANCHOBOTON + 110 , ALTOBOTON, BLANCO, -170, ANCHOCENTROVENTANA,
                            ALTOCENTROVENTANA, FUENTEBOTON)



def pantallaLeaderboard(nombre):
	"""muestra el puntaje maximo y quien lo realizo en pantalla""" 
	puntaje_maximo= -1
	nom_punt_max= ""
	archivo= open("../logs/"+nombre, "r")
	datos= json.load(archivo)
	for partida in datos:
		if partida["puntaje_maximo"] > puntaje_maximo:
			puntaje_maximo= partida["puntaje_maximo"]
			nom_punt_max= partida["nombre"]
	drawMensaje("puntaje mas alto "+str(puntaje_maximo)+", lo hizo "+'"'+nom_punt_max+'"', 290, 50)


def modificoArchivoLog(datosJson,nombre):
	"""actualiza o crea el archivo log del juego correspondiente"""
	try:
		ok= False
		aux= False    			         #para saber si el puntaje actual es menor
		archivo= open("../logs/"+nombre,"r")			#el archivo json debe tener por lo menos 1 dato
		datos_iguales= json.load(archivo)
		datos_viejos= datos_iguales.copy()
		for partida in datos_viejos:
			if partida["nombre"] == datosJson[0]["nombre"]:
				if partida["puntaje_maximo"] < datosJson[0]["puntaje_maximo"]:
					partida["puntaje_maximo"]= datosJson[0]["puntaje_maximo"]
					ok= True
				else: 
					aux= True                #significa que no supero su record
		archivo= open("../logs/"+nombre, "w")
		if ok:
			json.dump(datos_viejos, archivo)
		elif not(aux):
			datos_viejos.append(datosJson[0])
			json.dump(datos_viejos, archivo)
		else:
			json.dump(datos_iguales, archivo)
		archivo.close()
	except:
		archivo= open("../logs/"+nombre, "w")
		json.dump(datosJson,archivo)
		archivo.close()

def cargoGrabaciones():
	dicc_grabaciones={}
	for sonido in os.listdir(DIRGRABACIONES):
		dicc_grabaciones[sonido[:-4]]= pygame.mixer.Sound(DIRGRABACIONES+sonido)          
	return dicc_grabaciones


def pantallaAcomodo():
    """Carga la pantalla de acomodo y formo para elegir o silabas o letras"""
    
    #imagen= Imagen((ancho_aux+ancho_ventana-resta_ancho, alto_aux), ruta, imagen)
    #imagen_rect=Imagen((ancho_aux+ancho_ventana-resta_ancho,alto_aux+200),DIRIMAGENES+"Letras/rect.jpg",imagen.nombre)
    pygame.display.flip()
    screen.fill(CELESTE)
    picture = pygame.image.load(DIRIMAGENES+'/monstruo_feliz.png')
    picture = pygame.transform.scale(picture, (150, 150))
    screen.blit(picture, (550,110))
    drawMensaje("ACOMODO Y FORMO", 530, 50)
    pygame.mixer.music.pause()
    drawMensaje("ELEGI UN NIVEL", 550, 80)

    while True:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
            if (event.type == KEYUP):
                if event.key == K_ESCAPE:
                    terminate()

        botonVolver.mostrarBoton()
        botonConLetras.mostrarBoton()
        botonConSilabas.mostrarBoton()
        
        if botonVolver.toca(getCursorPos()) and botonIzquierdoMouseClickeado():
            pantallaInicio()
        if botonConLetras.toca(getCursorPos()) and botonIzquierdoMouseClickeado():
            nombre_usuario= suite.ingreso_usuario(13)
            screen.fill(random.choice(colores))
            suite.drawMensaje("HOLA "+nombre_usuario+ " !",ANCHOCENTROVENTANA-ANCHOBOTON,ALTOCENTROVENTANA-ALTOBOTON)
            acomodo_y_formo_letras.main(nombre_usuario)
        if botonConSilabas.toca(getCursorPos()) and botonIzquierdoMouseClickeado():
            nombre_usuario= suite.ingreso_usuario(13)
            screen.fill(random.choice(colores))
            suite.drawMensaje("HOLA "+nombre_usuario+ " !",ANCHOCENTROVENTANA-ANCHOBOTON,ALTOCENTROVENTANA-ALTOBOTON)
            acomodo_y_formo_con_silabas.main(nombre_usuario)

        pygame.display.update()

def pantallaInicio():
    """Carga la pantalla inicial del juego"""
    screen.fill(NARANJACLARO)
    img_monstruo = pygame.image.load(DIRIMAGENES+'/menu.jpg')
    img_monstruo = pygame.transform.scale(img_monstruo, (450, 450))
    screen.blit(img_monstruo, (70,110))
    drawMensaje("CONECTAR - MINI JUEGOS EDUCATIVOS", 130, 50)
    pygame.mixer.music.pause()	
    while True:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                terminate()
            if (event.type == KEYUP):
                if event.key == K_ESCAPE:
                    terminate()

        botonComeVocales.mostrarBoton()
        botonEntrometido.mostrarBoton()
        botonCadaUnaEnSuLugar.mostrarBoton()
        botonSalir.mostrarBoton()
        botonAcomodoYFormo.mostrarBoton()
        
        if botonAcomodoYFormo.toca(getCursorPos()) and botonIzquierdoMouseClickeado():
            pantallaAcomodo()
			
        if botonComeVocales.toca(getCursorPos()) and botonIzquierdoMouseClickeado():
            come_vocales.main()
        if botonEntrometido.toca(getCursorPos()) and botonIzquierdoMouseClickeado():
        	el_entrometido.main()
        if botonCadaUnaEnSuLugar.toca(getCursorPos()) and botonIzquierdoMouseClickeado():
            nombre_usuario= suite.ingreso_usuario(13)
            screen.fill(random.choice(colores))
            suite.drawMensaje("HOLA "+nombre_usuario+ " !",ANCHOCENTROVENTANA-ANCHOBOTON,ALTOCENTROVENTANA-ALTOBOTON)
            cada_una_en_su_lugar.main(nombre_usuario)
        elif botonSalir.toca(getCursorPos()) and botonIzquierdoMouseClickeado():
            terminate()

        pygame.display.update()

def cargarDiccionario(dicc, ruta= DIRIMAGENES):
	"""carga diccionario con todas las imagenes de la ruta"""
	lista=[]
	for letra in os.listdir(ruta):
		if os.path.isdir(ruta+letra):
			for img in os.listdir(ruta+letra):
				lista.append(img)
			dicc[letra]= lista
			lista=[]
	return (dicc)

def botonIzquierdoMouseClickeado():
	"""retorna si el boton izquierdo del mouse esta presionado"""
	return pygame.mouse.get_pressed()[0]
		
def getCursorPos():
	"""retorna la posicion del mouse"""
	return pygame.mouse.get_pos()

def evaluarTacho(tacho,objeto,objeto_destino,event,color,puntos,consigna,msj,correcto,reproduccionMusica, args):
	"""	evalua la condicion del tacho despues de arastrar el objeto"""
	while not tacho.rect.colliderect(objeto.rect) and pygame.mouse.get_pressed()[0]:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				come_vocales.terminate()
			if (event.type == KEYUP):
				if event.key == K_ESCAPE:
					come_vocales.terminate()
				if event.key == K_m:
					if reproduccionMusica:
						pygame.mixer.music.pause()
						reproduccionMusica= False
					else:
						pygame.mixer.music.unpause()
						reproduccionMusica= True
		screen.fill(color)
		for obj in args:
			if obj.arrastra:
				screen.blit(obj.image,obj.rect)
		drawScore(puntos)
		drawMensaje("Tecla ESC: volver al menu, Tecla M: pausar musica", ancho_ventana-1280, alto_ventana-700)
		drawMensaje(consigna, ancho_ventana-1250, alto_ventana-500)
		screen.blit(tacho.image,tacho.rect)
		screen.blit(objeto_destino.image, (1000,100))
		objeto.handle_event(event,screen)
		screen.blit(objeto.image,objeto.rect)
		pygame.display.flip()
		clock.tick(60)
	if tacho.rect.colliderect(objeto.rect):
		if objeto.arrastra:
			if objeto.nombre[0].upper() != objeto_destino.nombre:
				objeto.arrastra=False
				puntos+= 3
				correcto=correcto+1
			else:
				puntos-= 1
				objeto.rect.topleft=objeto.rect_aux
	return puntos,correcto

def evaluar_lugar(objeto,objeto_destino,event,color,puntos,consigna,msj,correcto,reproduccionMusica, args, dicc_grabaciones= cargoGrabaciones()):
	"""evalua si el texto colisiona con el rectangulo o no"""
	ok=True
	tocoImagen= False
	while not objeto_destino.rect.contains(objeto.rect) and pygame.mouse.get_pressed()[0]and ok:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminate()
			if (event.type == KEYUP):
				if event.key == K_ESCAPE:
					terminate()
				if event.key == K_m:
					if reproduccionMusica:
						pygame.mixer.music.pause()
						reproduccionMusica= False
					else:
						pygame.mixer.music.unpause()
						reproduccionMusica= True
		if ok:
			for dato in args:
				if dato[0].nombre!=objeto.nombre and ok: 
					if dato[1].rect.contains(objeto.rect)and pygame.mouse.get_pressed()[0] and ok:
						puntos-=1
						objeto.rect.topleft=objeto.rect_aux.topleft
						ok=False
						sonidoMal.play()
		screen.fill(color)
		for obj2 in args:
			x,y =pygame.mouse.get_pos()
			if obj2[0].toca(x,y) and botonIzquierdoMouseClickeado() and not tocoImagen:
				if not pygame.mixer.get_busy():
					dicc_grabaciones[obj2[0].nombre[:-4]].play()
				tocoImagen=True
		for obj in args:
			if obj[0].nombre!=objeto.nombre: 
				if obj[1].arrastra:
					screen.blit(obj[0].image,obj[0].rect)
					screen.blit(obj[1].image,obj[1].rect)
					screen.blit(obj[2].texto,obj[2].rect)
		drawScore(puntos)
		drawMensaje("Tecla ESC: volver al menu, Tecla M: pausar musica", ancho_ventana-1280, alto_ventana-700)
		drawMensaje(consigna, ancho_ventana-1250, alto_ventana-600)
		screen.blit(objeto_destino.image, objeto_destino.rect)
		if objeto.arrastra and ok:
			objeto.handle_event(event,screen)
		screen.blit(objeto.texto,objeto.rect)
		pygame.display.flip()
		clock.tick(60)
	if objeto_destino.rect.contains(objeto.rect):
		if objeto.arrastra:
			objeto.arrastra=False
			puntos+= 3
			correcto=correcto+1
			sonidoBien.play()
	return puntos,correcto

def evaluar_lugar_letra(objeto,objeto_destino,event,color,puntos,consigna,msj,correcto,reproduccionMusica, args):
	"""evalua si la letra colisiona con el rectangulo o no"""
	ok=True
	while pygame.mouse.get_pressed()[0]and ok:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminate()
			if (event.type == KEYUP):
				if event.key == K_ESCAPE:
					terminate()
				if event.key == K_m:
					if reproduccionMusica:
						pygame.mixer.music.pause()
						reproduccionMusica= False
					else:
						pygame.mixer.music.unpause()
						reproduccionMusica= True
		if ok:
			for dato in args:
				for valor in dato[1]:
					if valor.rect.contains(objeto.rect)and pygame.mouse.get_pressed()[0] and ok and str(valor.nombre).lower()!=str(objeto.nombre).lower():
						puntos-=1
						objeto.rect.topleft=objeto.rect_aux.topleft
						ok=False
						sonidoMal.play()
					elif valor.rect.contains(objeto.rect) and pygame.mouse.get_pressed()[0] and ok and str(valor.nombre).lower()==str(objeto.nombre).lower():
						if objeto.arrastra:
							objeto.arrastra=False
							puntos+= 3
							correcto=correcto+1
							sonidoBien.play()
		screen.fill(color)
		
		for obj in args:
			screen.blit(obj[0].image,obj[0].rect)
			for dato in obj[1]:
				screen.blit(dato.image,dato.rect)
		for obj in args:
			for dato in obj[2]:
				screen.blit(dato.texto,dato.rect)
		screen.blit(objeto.texto,objeto.rect)
		drawScore(puntos)
		drawMensaje("Tecla ESC: volver al menu, Tecla M: pausar musica", ancho_ventana-1280, alto_ventana-700)
		drawMensaje(consigna, ancho_ventana-1250, alto_ventana-600)
		if objeto.arrastra and ok:
			objeto.handle_event(event,screen)
		clock.tick(260)
		pygame.display.flip()
		
	return puntos,correcto


def evaluar(objeto,objeto_destino,event,color,puntos,consigna,msj,correcto,reproduccionMusica, args, dicc_grabaciones= cargoGrabaciones()):
	"""evalua si la imagen colisionada corresponde con la letra o no"""
	tocoImagen= False
	while not objeto_destino.rect.colliderect(objeto.rect) and pygame.mouse.get_pressed()[0]:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				terminate()
			if (event.type == KEYUP):
				if event.key == K_ESCAPE:
					terminate()
				if event.key == K_m:
					if reproduccionMusica:
						pygame.mixer.music.pause()
						reproduccionMusica= False
					else:
						pygame.mixer.music.unpause()
						reproduccionMusica= True
		screen.fill(color)
		for obj in args:
			if obj.toca(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and botonIzquierdoMouseClickeado() and not tocoImagen:
				if not pygame.mixer.get_busy():
					dicc_grabaciones[obj.nombre[:-4]].play()
				tocoImagen= True
			if obj.arrastra:
				screen.blit(obj.image,obj.rect)
		drawScore(puntos)
		drawMensaje("Tecla ESC: volver al menu, Tecla M: pausar musica", ancho_ventana-1280, alto_ventana-700)
		drawMensaje(consigna, ancho_ventana-1250, alto_ventana-600)
		screen.blit(objeto_destino.image, objeto_destino.rect)
		objeto.handle_event(event,screen)
		screen.blit(objeto.image,objeto.rect)
		pygame.display.flip()
		clock.tick(60)
	if objeto_destino.rect.colliderect(objeto.rect):
		if objeto.arrastra:
			if objeto.nombre[0].upper() == objeto_destino.nombre:
				objeto.arrastra=False
				puntos+= 3
				correcto=correcto+1
			else:
				puntos-= 1
				objeto.rect.topleft=objeto.rect_aux
	return puntos,correcto

def drawMensaje(msj, x, y):
	"""dibuja el puntaje correspondiente"""
	msjSurf = FUENTECONSIGNA.render(msj, True, NEGRO)
	screen.blit(msjSurf, (x, y))

def ingreso_usuario(largo_max, lower = False, upper = False, title = False):
	"""metodo para ingresar un nombre de usuario al iniciar la partida"""
	FUENTE_NOMBRE_2 = pygame.font.Font("../fuentes/Candy Beans.otf", 30)
	cadena = ""
	fin = False
	valores_permitidos= [i for i in range(97, 123)] + [i for i in range(48,58)]
	EVENT_PARPADEO = pygame.USEREVENT + 0
	pygame.time.set_timer(EVENT_PARPADEO, 800)
	ciclo_parpadeo = cycle(["_", " "])
	siguiente_parpadeo = next(ciclo_parpadeo)
	while not fin:
		screen.fill(VERDE)
		pygame.draw.rect(screen, AZUL, (ancho_ventana/2-150, alto_ventana/2-50, 300, 80)) #coordenadas de rectangulo azul
		imprimo_texto(FUENTE_BASICA_NOMBRE, ancho_ventana/2-150, alto_ventana/2-100, "TU NOMBRE: ")

		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == EVENT_PARPADEO:					#controla parpadeos
				siguiente_parpadeo = next(ciclo_parpadeo)
			
			elif event.type == KEYUP and event.key in valores_permitidos and len(cadena) < largo_max:     #si el caracter cumple
				
				if pygame.key.get_mods() & KMOD_SHIFT or pygame.key.get_mods() & KMOD_CAPS:        #si se ingresa en mayusculas
					cadena += chr(event.key).upper()
				else:														#si es minuscula
					cadena += chr(event.key)
			elif event.type == KEYUP:											
				if event.key == K_BACKSPACE:						
					cadena = cadena[:-1]
				elif event.key == K_SPACE:
					cadena += " "
				elif event.key == K_RETURN:
					fin = True
		if len(cadena) < largo_max:
			imprimo_texto(FUENTE_NOMBRE_2, ancho_ventana/2-145, alto_ventana/2-25, cadena + siguiente_parpadeo)
		else:
			imprimo_texto(FUENTE_NOMBRE_2, ancho_ventana/2-145, alto_ventana/2-25, cadena + siguiente_parpadeo)
		pygame.display.update()
	return cadena

def imprimo_texto(fuente, x, y, texto, color = (255,255,255)):
	"""imprime texto en pantalla dada ua posicion determinada"""
	texto_imagen = fuente.render(texto, True, color)
	screen.blit(texto_imagen, (x,y))

def drawScore(score):
    """muestra y actualiza la puntuacion del juego"""
    scoreSurf = FUENTE_BASICA.render('puntos: {}'.format(score), True, BLANCO)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (ancho_ventana - 120, 10)
    screen.blit(scoreSurf, scoreRect)

def inicializarImagenes(dicc):
	"""iniciaiza todos los sprites en pantalla y retorna una lista de sprites"""
	ancho_aux= 0
	alto_aux= 50
	resta_ancho= ancho_ventana
	lista_sprites=[]	#lista de los sprites para poder controlar los eventos
	letra= list(dicc.keys())[0]     # almacena en letra la letra del direc.
	lis= dicc[letra]				
	copy = lis[:]					# mezclo la lista para que las imagenes incorrctas no vayan siempre al final de la pantalla
	random.shuffle(copy)		
	lis = copy[:]	
	imagen= Imagen((ancho_aux+ancho_ventana/2.4, alto_aux+30), DIRIMAGENES+"Letras"+"/"+letra.lower()+"_letra_"+letra+".png", letra)
	lista_sprites.append(imagen)
	imagen.set_rect(200, 90)        # mod. rectangulo de letra
	alto_aux=500
	for imagen in lis:
		char= imagen[0].upper()                #agarro la primera letra de la imagen, para saber en q directorio buscar
		ruta= DIRIMAGENES+char+"/"+imagen        #modifico directorio pq sino no encuentra la imagen, 
		imagen= Imagen((ancho_aux+ancho_ventana-resta_ancho, alto_aux), ruta, imagen)
		resta_ancho-= 280 
		lista_sprites.append(imagen)
	
	return lista_sprites

def inicializarImagenesCadaUno(dicc):
	"""iniciaiza todos los sprites en pantalla y retorna una lista de sprites, donde cada elemento es una lista con 3 objetos"""
	ancho_aux= 300
	alto_aux= 50
	resta_ancho= ancho_ventana
	lista_sprites=[]	#lista de los sprites para poder controlar los eventos
	letra= list(dicc.keys())[0]     # almacena en letra la letra del direc.
	lis= dicc[letra]				
	alto_aux=300
	valores=[]
	for imagen in lis:
		valores.append((20+ancho_aux+ancho_ventana-resta_ancho,alto_aux+300))
		resta_ancho-= 280 
	resta_ancho=ancho_ventana
	for imagen in lis:
		lista_datos=[]
		valor=random.choice(valores)
		valores.remove(valor)
		palabra=Texto(valor, FUENTE_BASICA_2,imagen.replace('.png', '').upper(), imagen.replace('.png', '').upper())
		char= imagen[0].upper()                #agarro la primera letra de la imagen, para saber en q directorio buscar
		ruta= DIRIMAGENES+char+"/"+imagen        #modifico directorio pq sino no encuentra la imagen, 
		imagen= Imagen((ancho_aux+ancho_ventana-resta_ancho, alto_aux), ruta, imagen)
		imagen_rect=Imagen((ancho_aux+ancho_ventana-resta_ancho,alto_aux+200),DIRIMAGENES+"Letras/rect.jpg",imagen.nombre)
		#imagen_rect.set_rect(ancho_aux+ancho_ventana-resta_ancho-130,80)
		lista_datos.append(imagen)
		lista_datos.append(imagen_rect)
		lista_datos.append(palabra)
		resta_ancho-= 280 
		lista_sprites.append(lista_datos)
	return lista_sprites
def inicializarImagenesConSilabas(dicc):
	"""retorna una lista con las imagenes del directorio"""
	silabas = separasilabas.silabizer()
	ancho_aux= (ancho_ventana/2)-300
	alto_aux= 50
	resta_ancho= ancho_ventana
	lista_sprites=[]	#lista de los sprites para poder controlar los eventos
	letra= list(dicc.keys())[0]     # almacena en letra la letra del direc.
	lis= dicc[letra]				
	alto_aux=300
	valores=[]
	dicc_aux={}
	for imagen in lis:
		dicc_aux[imagen]=[]
		for dato in silabas(imagen.replace('.png', '')):
			dicc_aux[imagen].append((50+ancho_aux+ancho_ventana-resta_ancho,alto_aux+300))
			resta_ancho-= 70 
	resta_ancho=ancho_ventana
	resta_ancho_aux=resta_ancho
	variable=1
	for imagen in lis:
		num_aux=0
		lista_datos=[]
		lis_letras=[]
		lis_letras_rect=[]
		if variable==1:
			var=100
			for dato in silabas(imagen.replace('.png', '')):
				valor=random.choice(dicc_aux[imagen])
				dicc_aux[imagen].remove(valor)
				letra=Texto(valor, FUENTE_BASICA_2,str(dato), str(dato))
				letra_rect=	Imagen((var,alto_aux+200),DIRIMAGENES+"Letras/silaba_rect.jpg",dato)
				lis_letras.append(letra)
				lis_letras_rect.append(letra_rect)
				resta_ancho_aux-=40
				var+=80
		else:
			if variable==2:
				if len(imagen.replace('.png', ''))<5:
					var=1050
					for dato in silabas(imagen.replace('.png', '')):
						valor=random.choice(dicc_aux[imagen])
						dicc_aux[imagen].remove(valor)
						letra=Texto(valor, FUENTE_BASICA_2,str(dato), str(dato))
						letra_rect=	Imagen((var,alto_aux+200),DIRIMAGENES+"Letras/silaba_rect.jpg",dato)
						lis_letras.append(letra)
						lis_letras_rect.append(letra_rect)
						resta_ancho_aux-=40
						var+=80
				else:
					var=910
					for dato in silabas(imagen.replace('.png', '')):
						valor=random.choice(dicc_aux[imagen])
						dicc_aux[imagen].remove(valor)
						letra=Texto(valor, FUENTE_BASICA_2,str(dato), str(dato))
						letra_rect=	Imagen((var,alto_aux+200),DIRIMAGENES+"Letras/silaba_rect.jpg",dato)
						lis_letras.append(letra)
						lis_letras_rect.append(letra_rect)
						resta_ancho_aux-=40
						var+=80
					
		variable+=1
		resta_ancho_aux-=130
		char= imagen[0].upper()                #agarro la primera letra de la imagen, para saber en q directorio buscar
		ruta= DIRIMAGENES+char+"/"+imagen        #modifico directorio pq sino no encuentra la imagen, 
		if len(imagen.replace('.png', '')) >5:
			imagen= Imagen((num_aux/2+ancho_aux+ancho_ventana-resta_ancho, alto_aux - 100), ruta, imagen)
		else:
			imagen= Imagen((ancho_aux+ancho_ventana-resta_ancho, alto_aux - 100), ruta, imagen)
		lista_datos.append(imagen)
		lista_datos.append(lis_letras_rect)
		lista_datos.append(lis_letras)
		resta_ancho-= 250 
		lista_sprites.append(lista_datos)
	return lista_sprites


def inicializarImagenesLetras(dicc):
	"""retorna una lista con las imagenes del directorio, donde cada elemento es una lista con 3 elementos"""
	ancho_aux= (ancho_ventana/2)-300
	alto_aux= 50
	resta_ancho= ancho_ventana
	lista_sprites=[]	#lista de los sprites para poder controlar los eventos
	letra= list(dicc.keys())[0]     # almacena en letra la letra del direc.
	lis= dicc[letra]				
	alto_aux=300
	valores=[]
	dicc_aux={}
	for imagen in lis:
		dicc_aux[imagen]=[]
		for dato in imagen.replace('.png', ''):
			dicc_aux[imagen].append((50+ancho_aux+ancho_ventana-resta_ancho,alto_aux+300))
			resta_ancho-= 40 
	resta_ancho=ancho_ventana
	resta_ancho_aux=resta_ancho
	variable=1
	for imagen in lis:
		num_aux=0
		lista_datos=[]
		lis_letras=[]
		lis_letras_rect=[]
		if variable==1:
			var=100
			for dato in imagen.replace('.png', ''):
				valor=random.choice(dicc_aux[imagen])
				dicc_aux[imagen].remove(valor)
				letra=Texto(valor, FUENTE_BASICA_2,dato.upper(), dato.upper())
				letra_rect=	Imagen((var,alto_aux+200),DIRIMAGENES+"Letras/letra_rect.jpg",dato)
				lis_letras.append(letra)
				lis_letras_rect.append(letra_rect)
				resta_ancho_aux-=40
				var+=40
		else:
			if variable==2:
				if len(imagen.replace('.png', ''))<5:
					var=1050
					for dato in imagen.replace('.png', ''):
						valor=random.choice(dicc_aux[imagen])
						dicc_aux[imagen].remove(valor)
						letra=Texto(valor, FUENTE_BASICA_2,dato.upper(), dato.upper())
						letra_rect=	Imagen((var,alto_aux+200),DIRIMAGENES+"Letras/letra_rect.jpg",dato)
						lis_letras.append(letra)
						lis_letras_rect.append(letra_rect)
						resta_ancho_aux-=40
						var+=40
				else:
					var=910
					for dato in imagen.replace('.png', ''):
						valor=random.choice(dicc_aux[imagen])
						dicc_aux[imagen].remove(valor)
						letra=Texto(valor, FUENTE_BASICA_2,dato.upper(), dato.upper())
						letra_rect=	Imagen((var,alto_aux+200),DIRIMAGENES+"Letras/letra_rect.jpg",dato)
						lis_letras.append(letra)
						lis_letras_rect.append(letra_rect)
						resta_ancho_aux-=40
						var+=40
					
		variable+=1
		resta_ancho_aux-=130
		char= imagen[0].upper()                #agarro la primera letra de la imagen, para saber en q directorio buscar
		ruta= DIRIMAGENES+char+"/"+imagen        #modifico directorio pq sino no encuentra la imagen, 
		if len(imagen.replace('.png', '')) >5:
			imagen= Imagen((num_aux/2+ancho_aux+ancho_ventana-resta_ancho, alto_aux - 100), ruta, imagen)
		else:
			imagen= Imagen((ancho_aux+ancho_ventana-resta_ancho, alto_aux - 100), ruta, imagen)
		lista_datos.append(imagen)
		lista_datos.append(lis_letras_rect)
		lista_datos.append(lis_letras)
		resta_ancho-= 250 
		lista_sprites.append(lista_datos)
	return lista_sprites


def terminate():
	"""finaliza ejecucion y cierra el programa"""
	pygame.quit()
	sys.exit()

if __name__ == "__main__":
	cargoGrabaciones()
	screen.fill(random.choice(colores))
	pygame.mixer.music.play(-1, 0.0)
	pantallaInicio()
