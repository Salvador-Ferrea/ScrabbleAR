import PySimpleGUI as sg

from pattern.es import spelling,lexicon,tag,parse

import itertools as it

import random

import os.path as path

import json

import time

import sys

from datetime import datetime

import puntajesTP

import turnoComputadora

import turnoJugador

sg.theme('DarkAmber')
color_button = ('white','blue')
tam_button = 5,2
#-----------------------------------------------------------------
def fichas(letras_total):#<-----consigo letra de las fichas disponible
	if letras_total:
		letra=random.choice(list(letras_total.keys()))	
		letras_total[letra]= letras_total[letra] - 1
		if letras_total[letra] == 0:
			del letras_total[letra]
	else:
		letra=''	
	return letra
#-------------------------------------------------------------------
def calcular(i,j,naranja,verde,azul,rojo):
	if(i,j) in naranja: 
		return("white", "orange")        
	elif(i,j) in verde:        
		return("white", "green")        
	elif (i,j) in azul:        
		return("white", "blue")        
	elif (i,j) in rojo:                   
		return("white", "red")        
	else:        
		return("white", "lightblue") 

def puntaje_casillero(i,j,nivel,naranja,verde,azul,rojo):#<---- devuelve el valor del casillero
		
		if(i,j) in naranja:
			stringC='Px3'
			if nivel =='Dificil' :
				if (i,j) == (1,1) or (i,j) == (1,15) or (i,j) == (15,1) or (i,j) == (15,15):
					stringC='Des3'			       
			return stringC		 
			
		elif(i,j) in verde:
			stringC='Lx2'
			if nivel =='Medio' or nivel =='Dificil' :
				if (i,j) == (4,8) or (i,j) == (12,8) or (i,j) == (8,4) or (i,j) == (8,12):
					stringC='Des2'	       
			return stringC
			        
		elif (i,j) in azul:        
			return 'Lx3'        
		elif (i,j) in rojo:
			stringC='Px2'			
			if (i,j) == (6,6) or (i,j) == (6,10) or (i,j) == (10,10) or (i,j) == (10,6):
				stringC='Des1'          
			return stringC
			
		else:
			return''
		
def leerTopTen(archiv):#<---leo el archivo de las partidas guardadas
	with open(archiv, 'r') as archivo:
		datos = json.load(archivo)
	return datos

def escribirTopTen(jugadores,archiv):#<---escribo en el archivo  las partidas guardadas
	with open(archiv, 'w') as archivo:
		json.dump(jugadores, archivo,indent=4)	
				
def leerPartidasGuardadas():#<---leo el archivo de las partidas guardadas
	with open('partidasGuardadas.json', 'r') as archivo:
		datos = json.load(archivo)
	return datos

def escribirPartidasGuardadas(jugadores):#<---escribo en el archivo  las partidas guardadas
	with open('partidasGuardadas.json', 'w') as archivo:
		json.dump(jugadores, archivo,indent=4)
		
def guardarTopTen(nivel,totalJug):
	if nivel == 'Facil':
		archivo ='archivoTopTen.json'
	elif nivel == 'Medio': 
		archivo ='archivoTopTenMedio.json'
	else:
		archivo ='archivoTopTenDificil.json'
		
	if path.exists(archivo):
		jugTopTen = leerTopTen(archivo)
		jugad = sorted(jugTopTen.items(), key = lambda jug: jug[1]['puntaje'])
		if len(jugad) == 10:
			if jugad[1][1]['puntaje'] < totalJug :
				dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
				nombTopTen = sg.popup_get_text('ingrese nombre ', '')
				if nombTopTen != None:
					while nombTopTen == '':
						sg.popup('no ingreso ningun nombre')
						nombTopTen = sg.popup_get_text('ingrese nombre ', '')
					jugTopTen[dt_string]= {'nombre': nombTopTen, 'puntaje': totalJug}
					del jugTopTen[jugad[1][0]]
					sg.popup('ingreso al top ten')
			else:
				sg.popup('no ingreso al top ten')	
		else:
			dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
			nombTopTen = sg.popup_get_text('ingrese nombre ', '')
			if nombTopTen != None:
				while nombTopTen == '':
					sg.popup('no ingreso ningun nombre')
					nombTopTen = sg.popup_get_text('ingrese nombre ', '')
				jugTopTen[dt_string]= {'nombre': nombTopTen, 'puntaje': totalJug}
				sg.popup('ingreso al top ten')
					
	else:
		jugTopTen={}
		dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		nombTopTen = sg.popup_get_text('ingrese nombre ', '')
		jugTopTen[dt_string]= {'nombre': nombTopTen, 'puntaje': totalJug}
			
			
	escribirTopTen(jugTopTen,archivo)

def evaluarGanador(totalJug,totalComp,nivel):
	if totalJug > totalComp:
		sg.popup('Felicitaciones!!gano el juego')
	elif totalJug < totalComp:
		sg.popup('Perdio el juego')	
	else:
		sg.popup('Empato el juego')
			
	guardarTopTen(nivel,totalJug)		
	puntajesTP.main(nivel)
	
def clasificar(palabra,nivel,clasificacionAleatoria):#<--- evalua si la palabra es correcta, segun el nivel 
	esValida = False
	if palabra in spelling.keys() and palabra in lexicon.keys():
		if nivel == 'Facil':
			esValida = True
		elif nivel == 'Medio':	
			lista = (tag(palabra, tokenize=True, encoding='utf-8'))
			if lista[0][1] == 'NN' or lista[0][1] == 'VB':
				esValida = True
		else:
			lista = (tag(palabra, tokenize=True, encoding='utf-8'))
			if lista[0][1] == clasificacionAleatoria:
				esValida = True		
	return esValida

def evaluarUbi(ubicacion):
	incorrecto=True
	if all(ubicacion[i][0]==ubicacion[i+1][0] for i in range(len(ubicacion)-1)):
		ubicacion = sorted(ubicacion, key=lambda tup: tup[1])
		if all(ubicacion[i][1]==ubicacion[i+1][1]-1 for i in range(len(ubicacion)-1)):
			incorrecto=False
			sg.popup('la palabra es horizontal')
		else:
			sg.popup('ubicacion incorrecta vuelva a intentarlo')
	elif all(ubicacion[i][1]==ubicacion[i+1][1] for i in range(len(ubicacion)-1)):
		ubicacion = sorted(ubicacion, key=lambda tup: tup[0])
		if all(ubicacion[i][0]==ubicacion[i+1][0]-1 for i in range(len(ubicacion)-1)):	
			incorrecto=False
			sg.popup('la palabra es vertical')
		else:
			sg.popup('ubicacion incorrecta vuelva a intentarlo')
	else:
		sg.popup('ubicacion incorrecta vuelva a intentarlo')
	return incorrecto

def activar(window):
	window[(0,8)].update(disabled = True)
	window[(0,11)].update(disabled = True)
			
	window[(0,1)].update(disabled = True)
	window[(0,2)].update(disabled = True)
	window[(0,3)].update(disabled = True)
	window[(0,4)].update(disabled = True)
	window[(0,5)].update(disabled = True)
	window[(0,6)].update(disabled = True)
	window[(0,7)].update(disabled = True)

def desactivar(window):
	window[(0,8)].update(disabled = False)
	window[(0,11)].update(disabled = False)	
			
	window[(0,1)].update(disabled = False)
	window[(0,2)].update(disabled = False)
	window[(0,3)].update(disabled = False)
	window[(0,4)].update(disabled = False)
	window[(0,5)].update(disabled = False)
	window[(0,6)].update(disabled = False)
	window[(0,7)].update(disabled = False)
	

def devolver(window,botones,ScrDic,guardadoAtril,guardado,ubicacion):
	for i in range(len(ubicacion)):
		window[ubicacion[i]].update(ScrDic[ubicacion[i]]['puntImp'], button_color = ScrDic[ubicacion[i]]['color'])				
	for i in guardadoAtril:
		window[i].update(text= botones[i])
	guardado={}
	guardadoAtril=[]
	ubicacion=[]
	return guardadoAtril,guardado,ubicacion
	
def guardarP(window,totalJug,totalComp,letras_total,nivel,current_time,tiempo,clasificacionAleatoria,ScrDic,cantCambFichas,puntJueg):
	dictGuardar = {}
	dictGuardar['PuntajeJug']= totalJug #guardo el puntaje del jugador
	dictGuardar['PuntajeComp']= totalComp #guardo el puntaje de la computadora
	dictGuardar['TotalFichas']= letras_total #guardo el total de fichas que queda
	dictGuardar['Nivel']= nivel #guardo el nivel del juego 
	dictGuardar['Tiempo']= current_time #guardo el tiempo en el momento que se guardo
	dictGuardar['TiempoTotal']= tiempo #guardo el tiempo max que puede durar la partida
	dictGuardar['cantCambFichas']= cantCambFichas
	dictGuardar['puntJueg']= puntJueg
	dictGuardar['clasificacionAleatoria'] = clasificacionAleatoria#guardo el valor aleatorio,me sirve solo si el nivel que se guarda es dificil
	dictGuardar['FichasAtrilComp']=[]
	dictGuardar['FichasAtrilJug']=[]
	for i in range(7):#<---guardo las fichas del atril de la computadora y del jugador
		dictGuardar['FichasAtrilJug'].append(window[(0,i+1)].GetText())
		dictGuardar['FichasAtrilComp'].append(fichasComp[(100,i+1)])
			
	dictGuardar['ClavesCasillero']=[]
			
	for i in range(1,16):	#guardo todos los casilleros del tablero
		for j in range(1,16):
			if ScrDic[(i,j)]['letra'] != '':
				a =	ScrDic[(i,j)]
				b =[str(i),str(j)] #tuve que pasar a string la tupla con las coordenadas pq me tiraba error para guardar en json
				c = ','.join(b) 
				dictGuardar[c] = a# guardo los datos de la coordenada en un diccionario
				dictGuardar['ClavesCasillero'].append(c)# guardo en una lista de las coordenadas
	escribirPartidasGuardadas(dictGuardar)			
def crearDicTablero(window,ScrDic):
	for i in range(1,16):
		for j in range(1,16):		
			if(i,j) in naranja:
				x = window[(i,j)].GetText()
				if x == 'Px3':
					puntajeCa = 3#<-- suma puntaje al casillero	
					letraOpalabra= 'palabra'#<--- multiplica palabra
				else:
					puntajeCa = 3	
					letraOpalabra= 'descuenta'#<---resta puntos						
				ScrDic[(i,j)]={'color':("white", "orange"),'colorLetraUbi':("white", "orange"),'letra':'','puntImp':x,'puntajeC':puntajeCa,'letOpal':letraOpalabra}        
			elif (i,j) in verde:
				x = window[(i,j)].GetText()
				if x == 'Lx2':
					puntajeCa = 2	
					letraOpalabra= 'letra'#<--- multiplica letra
				else:
					puntajeCa = 2	
					letraOpalabra= 'descuenta'        
				ScrDic[(i,j)]={'color':("white", "green"),'colorLetraUbi':("white", "green"),'letra':'','puntImp':x,'puntajeC':puntajeCa,'letOpal':letraOpalabra}       
			elif (i,j) in azul:
				x = window[(i,j)].GetText()
				ScrDic[(i,j)]={'color':("white", "blue"),'colorLetraUbi':("white", "blue"),'letra':'','puntImp':x,'puntajeC':3,'letOpal':'letra'}       
			elif (i,j) in rojo:
				x = window[(i,j)].GetText()
				if x == 'Px2':
					puntajeCa = 2	
					letraOpalabra= 'letra'
				else:
					puntajeCa = 1	
					letraOpalabra= 'descuenta'        
				ScrDic[(i,j)]={'color':("white", "red"),'colorLetraUbi':("white", "red"),'letra':'','puntImp':x,'puntajeC':puntajeCa,'letOpal':letraOpalabra}        
			else:        
				ScrDic[(i,j)]={'color':("white", "lightblue"),'colorLetraUbi':("white", "lightblue"),'letra':'','puntImp':'','puntajeC':0,'letOpal':''}           
	for i in range(1,8):
		ScrDic[(0,i)]=('white','blue')

def puntajeBase():
	puntJueg = {'A':1,'B':3,'C':2,'D':2,'E':1,'F':4,'G':2,'H':4,'I':1,'J':6,'K':6,'L':1,'LL':8,'M':3,'N':1,'Ñ':8,'O':1,'P':3,'Q':8,'R':1,'RR':8,'S':1,'T':1,'U':1,'V':4,'W':8,'X':8,'Y':4,'Z':10}
	return puntJueg
def cantidadBase():
	letras_total = {'A': 11,'B':3,'C':4,'D':4,'E':11,'F':2,'G':2,'H':2,
		'I':6,'J':2,'K':1,'L':4,'M':3,'N':5,'Ñ':1,'O':8,'P':2,'Q':1,'R':4,
		'S':7,'T':4,'U':6,'V':2,'W':1,'X':1,'Y':1,'Z':1}
	return letras_total
		
def time_as_int():
	return int(round(time.time() * 100))
				
naranja = [(1,1),(15,15),(1,15),(15,1),(1,8),(15,8),(8,1),(8,8),(8,15)]
verde = [(1,4),(1,12),(15,4),(15,12),(3,7),(3,9),(13,7),(13,9),(4,1),(4,8),(4,15),(12,1),(12,8),(12,15),(7,3),(7,13),(9,3),(9,13),(8,4),(8,12)]
azul = [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(2,6),(2,10),(14,6),(14,10),(6,2),(6,14),(10,2),(10,14),(7,7),(7,9),(9,7),(9,9)]
rojo = [(2,2),(3,3),(4,4),(5,5),(6,6),(10,10),(11,11),(12,12),(13,13),(14,14),(2,14),(3,13),(4,12),(5,11),(6,10),(10,6),(11,5),(12,4),(13,3),(14,2)]

def main(nivel='',tiempo= 0,carga='',diccionarioC ={},diccionarioV ={}):


	colIzq =  [[sg.Button(puntaje_casillero(i,j,nivel,naranja,verde,azul,rojo),button_color=calcular(i,j,naranja,verde,azul,rojo),size=(5, 2), key=(i,j), pad=(0,0)) for j in range(1,16)] for i in range(1,16)]
	colDer =[
			[sg.Text('Computadora:',size =(100,None),justification='left',text_color='yellow')],
			[sg.Button('?',button_color=color_button,size=tam_button, key=(100,i+1))for i in range(7)],
			[sg.Text('______________________________________________________',text_color='red')],
			[sg.Text('puntaje Computadora:'),sg.In(0, key=(40,40),size=tam_button)],
			[sg.Text('')],
			[sg.Text('')],
			[sg.Text('nivel:                    '),sg.In('', key=(50,50),size=(24,2))],
			[sg.Text('palabras a buscar:'),sg.In('', key=(60,60),size= (24,2))],
			[sg.Text("Fichas restantes: "),sg.In(0, key=(20,20),size=(24,2))],
			[sg.Text('')],
			[sg.Text('Tiempo:'),sg.Text('', size=(8, 1), font=('Helvetica', 20),justification='center', key='text')],
			[sg.Text('')],
			[sg.Text('')],
			[sg.Text('')],
			[sg.Text('puntaje Jugador:'),sg.In(0, key=(30,30),size=tam_button)],
			[sg.Text('______________________________________________________',text_color='red')],
			[sg.Text('Jugador:',size =(100,None),justification='left',text_color='yellow')],
			[sg.Button('',button_color=color_button,size=tam_button, key=(0,i+1))for i in range(7)]]
	colDer.append([sg.Button('Evaluar', key=(0,8),button_color=('black','gray'),size=tam_button),sg.Button('Cambiar Fichas', key=(0,11),button_color=('black','gray'),size=(6,2)),sg.Button('Devolver Fichas', key=(0,9),button_color=('black','gray'),size=(6,2)),sg.Button('Pasar', key=(0,10),button_color=('black','gray'),size=tam_button),sg.Button('Guardar partida', key=(0,12),button_color=('black','gray'),size=(7,2)),sg.Button('Terminar Partida', key=(0,13),button_color=('black','gray'),size=(7,2))])

	layout = [[sg.Column(colIzq,size=(750,750)),sg.Column(colDer,size=(700,700))]]
	window = sg.Window('Scrabble',layout).Finalize()
	window.Maximize()
		
	ScrDic = {}
	crearDicTablero(window,ScrDic)
	
	valor_A = ''
	valor_B = '' 
	fichasComp={} 	                 
#------------------------------------------------------------------------------------------------------
#idea para retornar datos:		 
	if carga != 'nuevo':#<--- si no es distinto de '', significa que se cargo la partida
		actual = leerPartidasGuardadas()
		tiempo= actual['TiempoTotal']
		resta= actual['Tiempo']
		clasificacionAleatoria = actual['clasificacionAleatoria']
		cantCambFichas = actual['cantCambFichas']
		puntJueg = actual['puntJueg'] 
		totalJug= actual['PuntajeJug']
		window[(30,30)].update(totalJug)
		totalComp= actual['PuntajeComp']
		window[(40,40)].update(totalComp)
		letras_total=actual['TotalFichas']
		window[(60,60)].update(clasificacionAleatoria)
		window[(20,20)].update(sum(actual['TotalFichas'].values()))
		botones = {}
		for i in range(7):
			window[0,i+1].update(actual['FichasAtrilJug'][i])
			fichasComp[100,i+1]=actual['FichasAtrilComp'][i]
			botones[0,i+1] = actual['FichasAtrilJug'][i]
		
		for i in range(len(actual['ClavesCasillero'])):
			clave= actual['ClavesCasillero'][i]#<--obtengo la clave del casillero
			coordenada=tuple((map(int,clave.split(','))))#<--convierto la clave que estaba en string a tupla 
			ScrDic[coordenada]=actual[actual['ClavesCasillero'][i]]#<--guardo en el diccionario los datos de ese casillero
			window[coordenada].update(ScrDic[coordenada]['letra'], button_color=ScrDic[coordenada]['colorLetraUbi'])#<--coloco la letra en la interfaz
	
	else:#<--- sino, inicia una nueva
		cantCambFichas = 3
		resta= 0
		tiempo=tiempo * 6000
		# total de fichas:
		#hago el diccionario
		if len(diccionarioC)== 0 :
			letras_total = cantidadBase()
		else:
			letras_total = diccionarioC
		if len(diccionarioV)== 0 :
			puntJueg = puntajeBase()
		else:
			puntJueg = diccionarioV
		#con esto puedo sumar para ver si el diccionario no tiene fichas
		botones = {(0,1):fichas(letras_total),(0,2):fichas(letras_total),(0,3):fichas(letras_total),(0,4):fichas(letras_total),(0,5):fichas(letras_total),(0,6):fichas(letras_total),(0,7):fichas(letras_total)} 
		
		if nivel == 'Dificil':#<--- si el nivel es dificil toma aleatoriamente un valor(verbo,sustantivo, adjetivo)
			listaClasif = ['VB','NN','JJ']
			clasificacionAleatoria = random.choice(listaClasif)
			if(clasificacionAleatoria == 'VB'):
				opcion ='verbos'
			elif(clasificacionAleatoria == 'NN'):
				opcion ='sustantivos'
			else:
				opcion ='adjetivos'
			window[(60,60)].update(opcion)			
		else:# si no, deja la variable vacia
			if nivel == 'Facil':	
				clasificacionAleatoria = 'verbos,sustantivos,adjetivos'
			else:
				clasificacionAleatoria = 'verbos,sustantivos'	
			window[(60,60)].update(clasificacionAleatoria)
		for i in range(7):
			window[0,i+1].update(botones[0,i+1])
			fichasComp[100,i+1]=fichas(letras_total)
		window[(20,20)].update(sum(letras_total.values()))
		totalJug=0#<--- puntaje total del jugador
		totalComp =0#<------- puntaje total de la computadora
	window[(50,50)].update(nivel)	
	print(sum(letras_total.values()))	
#-----------------------------------------------------------------------------------------------------		
	guardado ={}#<--- guarda la ubicacion y la letra en donde se ubico la ficha en el tablero
	guardadoAtril = []#<---- guarda las coordenadas del atril del jugador: de las fichas que uso
	palabra = []#<----guarda las letras de la palabra
	ubicacion = []#<---guarda las coordenadas de donde se ubicaron las letras en el tablero
	listaCoorLetrasUbicadas = []#<---- es la lista de las coordenadas donde la computadora ubico la palabra en el tablero
	#fichasComp={}#<---guarda la ubicacion y la letra de las fichas del atril de la computadora
	seguirJ = True#<-- si da false es que el jugador no puede jugar mas y no hay mas fichas
	TerminoJ = False#<--- si da true es porque seguirJ es igual a false, lo evalua cuando de apreta pasar
	seguirC= True#<-- si da false es que la computadora no puede jugar mas y no hay mas fichas
	
	current_time = 0
	start_time =  time_as_int() - resta#<--- con esto empiezo desde el tiempo en que me quede
	while True:
		event, values = window.read(timeout=10)
		current_time = time_as_int() - start_time
		if current_time >= tiempo:#<-- esto corta el programa a los 60 segundos
			evaluarGanador(totalJug,totalComp,nivel)
			break
			
		#-----------------------------------------------------------------
		
		if TerminoJ  and not seguirC:#<---- si estos dos son false, ya no se puede seguir jugando
			evaluarGanador(totalJug,totalComp,nivel)
			break
		#-----------------------------------------------------------------	
		
		if event in (None, 'Exit'):
			break
					
		elif event != (0,8) and event != (0,9) and event != (0,10) and event != (0,11) and event != (0,12) and event != (0,13):#<--------si no es evaluar,modificar,pasar 
		
			if event in botones.keys():#<------entra si se apreto los botones del atril	
				valor_A = window[event].GetText()#<----toma la letra del boton del atril 
				
				if window[(8,8)].GetText() == 'Px3':#<------si no hay ficha en el casillero del medio
					window[(8,8)].update(valor_A, button_color=('white','black'))#<---
					window[event].update(text='')
					ubicacion.append((8,8))
					guardadoAtril.append(event)
					guardado[(8,8)] = valor_A
				else:	
					keys_entered = event#<--- guarda el event 	
					event, values = window.read()
					
					if event in (None, 'Exit'):#<--------en caso de se haya apretado un boton del atril y se cierre
						break
					
					elif event not in botones.keys():#<-------si no es un boton del atril 
						valor_B = window[event].GetText()#<----toma la letra del segundo event
						if valor_B == '' or valor_B == 'Px2' or valor_B == 'Px3' or valor_B == 'Lx2' or valor_B == 'Lx3' or valor_B == 'Des1' or valor_B == 'Des2' or valor_B == 'Des3':#<---probando px2
							window[event].update(valor_A, button_color=('white','black'))#<---
							window[keys_entered].update(text='')
							ubicacion.append(event)
							guardadoAtril.append(keys_entered)
							guardado[event] = valor_A	
					else:#<------si es un boton del atril
						valor_B = window[event].GetText()
						window[keys_entered].update(valor_B)
						window[event].update(valor_A)
			
		elif event == (0,8):#<----apreto evaluar
			if len(ubicacion) == 0:
				sg.popup('no coloco ninguna ficha en el tablero, no se puede evaluar')
			else:			
				incorrecto= evaluarUbi(ubicacion)
				if incorrecto:#<---- si es incorrecto por ubicacion, vuelve las fichas al lugar
					seguirJ = turnoJugador.devolverAtril(ubicacion,window,ScrDic,guardadoAtril,letras_total,seguirJ,botones)
				else:
					for i in ubicacion:#<---- utilizo las ubicaciones ordenadas, para sacar la palabra 
						palabra.append(guardado[i])
			
					strPal=''.join(palabra).lower()#<-----transformo la lista en string
					if clasificar(strPal,nivel,clasificacionAleatoria):
						sg.popup('se ubico la palabra')	
						totalJug = turnoJugador.sumoPalabra(ubicacion,ScrDic,palabra,puntJueg,totalJug,window)
						if sum(letras_total.values()) == 0:#<---- si no hay mas fichas en la bolsa
							seguirJ=True
						else: #<---- si  hay mas fichas en la bolsa, pide nuevas fichas
							turnoJugador.pidoFichasNuevas(guardadoAtril,botones,letras_total,window)
						#---desactiva evaluar y cambiar fichas
						activar(window)
					else:
						sg.popup('la palabra no es correcta,vuelva a intentarlo')
						seguirJ = turnoJugador.devolverAtril(ubicacion,window,ScrDic,guardadoAtril,letras_total,seguirJ,botones)
				palabra=[]
				guardado={}
				guardadoAtril=[]
				ubicacion=[]			

		elif event == (0,9):#modificar
			#devolver la fichas al atril,en caso de que te hayas equivocado antes de evaluar la palabra
			guardadoAtril,guardado,ubicacion = devolver(window,botones,ScrDic,guardadoAtril,guardado,ubicacion)
			
		elif event == (0,11):#<----cambio las fichas
			print('cambiar')
			if len(ubicacion) != 0:
				guardadoAtril,guardado,ubicacion = devolver(window,botones,ScrDic,guardadoAtril,guardado,ubicacion)
			#----------------------------------------
			if cantCambFichas != 0:
				sg.popup('haga click en las fichas que quiera cambiar y luego haga click en cambiar fichas')
				event, values = window.read()
				listaFcambiar= []
				while event !=(0,11):#se guarda en una lista las coordenadas de las fichas que quiere cambiar el jugador
					listaFcambiar.append(event)
					event, values = window.read()
				for i in listaFcambiar:
					if botones[i] in letras_total:
						letras_total[botones[i]] = letras_total[botones[i]] + 1
					else:
						letras_total[botones[i]] = 1
					botones[i]=fichas(letras_total)
					window[i].update(text= botones[i])
				cantCambFichas = cantCambFichas - 1
				activar(window)
			else:
				sg.popup('ya utilizo los 3 cambios de fichas')
			#---desactiva evaluar y cambiar fichas y las fichas del jugador
			
			
		
		elif event == (0,12):#guardar partida
			guardarP(window,totalJug,totalComp,letras_total,nivel,current_time,tiempo,clasificacionAleatoria,ScrDic,cantCambFichas,puntJueg)	
			break
		elif event == (0,13):#terminar partida
			evaluarGanador(totalJug,totalComp,nivel)
			break		
		else:
			if seguirJ == False:
				TerminoJ = True	
			print(fichasComp.values())		
			palabras_existentes= turnoComputadora.turno(clasificacionAleatoria,fichasComp,nivel)
			print(palabras_existentes)
			#-----------------------------------------------------------------------			
			if len(palabras_existentes) == 0 and sum(letras_total.values()) == 0:#<--- si la computadora no tiene palabras y no hay mas fichas,no puede seguir
				seguirC= False
			elif len(palabras_existentes) == 0:#<--- si la computadorano no tiene palabras y hay mas fichas,las cambia
				#turnoComputadora.cambiarFichas(fichasComp,letras_total,window)
				sg.popup('la computadora no encontro palabra')
			else:#<---sino, busca la ubicacion en el tablero	
				palabraUbi,encontro,listaCoorLetrasUbicadas = turnoComputadora.buscarTablero(palabras_existentes,ScrDic)
				#--------------------------------------------------------------------------------------------------		
				if not encontro and sum(letras_total.values()) == 0:#<--- si la computadora no encontro lugar y no hay mas fichas,no puede seguir
					seguirC= False
				elif not encontro: #<---- si la computadora no encontro lugar y  hay mas fichas,cambia las fichas
					turnoComputadora.cambiarFichas(fichasComp,letras_total,window)
				
				else:#<------ sino, encontro lugar y la ubica en la interfaz
					sumaComp= turnoComputadora.sumarPuntaje(window,listaCoorLetrasUbicadas,ScrDic,puntJueg)
					#-----------------------------------------------------------------------------------------------
					turnoComputadora.nuevasFichas(palabraUbi,fichasComp,window,letras_total)
					#--------------------------------------------------------------
					window[(20,20)].update(sum(letras_total.values()))#con esto puedo sumar para ver si el diccionario no tiene fichas
					totalComp = totalComp + sumaComp
					window[(40,40)].update(totalComp)
					listaCoorLetrasUbicadas = []
					#----activa evaluar y cambiar fichas	
			desactivar(window)
		window['text'].update('{:02d}:{:02d}'.format((current_time // 100) // 60,(current_time // 100) % 60))
	window.close()	
if __name__ == '__main__':
	nivel='Facil'
	nombre='jorge'
	main(nivel,20,'nuevo')
