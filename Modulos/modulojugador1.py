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

import configuracionScrabble

sg.theme('DarkBlue10')
color_button = ('white','orange')
tam_button = 5,2

def buscarFich(DictEleg):
	'''tomo la letra segun lo que pide en el modulo fichas'''
	if DictEleg:
		letra=random.choice(list(DictEleg.keys()))
		DictEleg[letra]= DictEleg[letra] - 1
		if DictEleg[letra] == 0:
			del DictEleg[letra]
	else:
		letra=''
	return letra			

#-----------------------------------------------------------------
def fichas(consonantes,vocales,ubi): 
	'''Busco segun la ubicacion en el atril: vocales, consonantes o random'''
	if ubi== 2 or ubi== 4:
		if(len(vocales)== 0):
			if (len(consonantes)== 0):
				letra=''
			else:	
				letra = buscarFich(consonantes)
		else:
			letra = buscarFich(vocales)						
	elif ubi== 7:
		listaR=[vocales,consonantes]
		random.shuffle(listaR)

		if(len(listaR[0])!= 0):
			letra = buscarFich(listaR[0])				
		else:						
			if(len(listaR[1])!= 0):
				letra = buscarFich(listaR[1])		
			else:			
				letra =''			
	else:
		letra = buscarFich(consonantes)			
	
	return letra

def calcular(i,j,naranja,verde,azul,rojo,nivel):
	'''Calcula el color del casillero segun el nivel en el que este'''
	if(i,j) in naranja:
		color=("white", "orange")
		if (nivel =='Dificil') and ((i,j) == (1,1) or (i,j) == (1,15) or (i,j) == (15,1) or (i,j) == (15,15)):
			color = ("white", "darkred")			
		return color        
	elif(i,j) in verde: 
		color=("white", "green")
		if (nivel =='Dificil' or nivel == 'Medio') and ((i,j) == (4,8) or (i,j) == (12,8) or (i,j) == (8,4) or (i,j) == (8,12)):
			color = ("white", "darkblue")			
		return color               
	elif (i,j) in azul:        
		return("white", "blue")        
	elif (i,j) in rojo:                   
		color=("white", "red")
		if (nivel =='Dificil' or nivel == 'Medio' or nivel == 'Facil') and ((i,j) == (6,6) or (i,j) == (6,10) or (i,j) == (10,10) or (i,j) == (10,6)):
			color = ("white", "purple")			
		return color         
	else:
		color = ("white", "lightblue")
		if nivel == 'Medio':
			color= ("white", "lightgreen")
		elif nivel =='Dificil':
			color= ("white", "pink")      
		return color

def puntaje_casillero(i,j,nivel,naranja,verde,azul,rojo):#<---- devuelve el valor del casillero	
	'''Imprime o no (segun el casillero y el nivel) el valor del casillero '''	
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
		
def leerTopTen(archiv):
	'''Lee el archivo del top ten que se pasa por parametro'''
	with open(archiv, 'r') as archivo:
		datos = json.load(archivo)
	return datos

def escribirTopTen(jugadores,archiv):
	'''Crea el archivo del top ten que se pasa por parametro(en caso de que exista, lo sobreescribe)'''
	with open(archiv, 'w') as archivo:
		json.dump(jugadores, archivo,indent=4)	
				
def leerPartidasGuardadas():
	'''Lee el archivo que tiene la partida guardada'''
	with open('Archivos/partidasGuardadas.json', 'r') as archivo:
		datos = json.load(archivo)
	return datos

def escribirPartidasGuardadas(jugadores):
	'''Crea el archivo  para guardar partida, que se pasa por parametro(en caso de que exista, lo sobreescribe)'''
	with open('Archivos/partidasGuardadas.json', 'w') as archivo:
		json.dump(jugadores, archivo,indent=4)
def definirArchTopTen(nivel):
	if nivel == 'Facil':
		archivo ='Archivos/archivoTopTen.json'
	elif nivel == 'Medio': 
		archivo ='Archivos/archivoTopTenMedio.json'
	else:
		archivo ='Archivos/archivoTopTenDificil.json'
	return archivo
		
def guardarTopTen(nivel,totalJug):
	'''Evalua segun el nivel, si  el puntaje del jugador ingresa en el top ten de ese nivel,
		si existe el archivo lo lee y sino lo crea. En caso de que el archivo exista y
		el top ten este lleno, realiza un sorted y evalua el puntaje actual con el minimo del
		top ten, si el valor actual es mayor al minimo elimina el minimo del top ten e ingresa
		el puntaje actual.Luego en el modulo puntajesTP  ordena y  muestra el top ten  '''
	archivo = definirArchTopTen(nivel)		
	try:
		jugTopTen = leerTopTen(archivo)
		jugad = sorted(jugTopTen.items(), key = lambda jug: jug[1]['puntaje'])
		if len(jugad) == 10:
			if jugad[0][1]['puntaje'] < totalJug :
				dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
				nombTopTen = sg.popup_get_text('ingrese nombre ', '')
				while nombTopTen == None or nombTopTen == '':
					sg.popup('no ingreso ningun nombre')
					nombTopTen = sg.popup_get_text('ingrese nombre ', '')
				jugTopTen[dt_string]= {'nombre': nombTopTen, 'puntaje': totalJug}
				del jugTopTen[jugad[0][0]]
				sg.popup('ingreso al top ten')
			else:
				sg.popup('no ingreso al top ten')	
		else:
			dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
			nombTopTen = sg.popup_get_text('ingrese nombre ', '')
			while nombTopTen == None or nombTopTen == '':
				sg.popup('no ingreso ningun nombre')
				nombTopTen = sg.popup_get_text('ingrese nombre ', '')
			jugTopTen[dt_string]= {'nombre': nombTopTen, 'puntaje': totalJug}
			sg.popup('ingreso al top ten')					
	except:
		jugTopTen={}
		dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
		nombTopTen = sg.popup_get_text('ingrese nombre ', '')
		while nombTopTen == None or nombTopTen == '':
			sg.popup('no ingreso ningun nombre')
			nombTopTen = sg.popup_get_text('ingrese nombre ', '')
		jugTopTen[dt_string]= {'nombre': nombTopTen, 'puntaje': totalJug}
		sg.popup('ingreso al top ten')			
	escribirTopTen(jugTopTen,archivo)
	return jugTopTen
def evaluarGanador(totalJug,totalComp,nivel):
	'''Evalua si el jugador gano,empato o perdio el juego y va al modulo guardadTopTen para
	evaluar si ingresa o no al top ten.y por ultimo voy al modulo puntajesTP para mostrar el
	 top ten'''
	if totalJug > totalComp:
		sg.popup('Felicitaciones!!gano el juego')
	elif totalJug < totalComp:
		sg.popup('Perdio el juego')	
	else:
		sg.popup('Empato el juego')			
	archivo = guardarTopTen(nivel,totalJug)		
	puntajesTP.main(nivel,archivo)
	
def clasificar(palabra,nivel,clasificacionAleatoria):
	'''Evalua si la palabra es correcta, segun el nivel''' 
	esValida = False
	correcto=False
	if 'ñ' in palabra:
		if palabra in lexicon.keys():
			correcto=True
	if (palabra in spelling.keys() and palabra in lexicon.keys()) or correcto:
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

def activar(window,*args):
	'''Activa el disabled de las coordenadas que se pasen por parametro'''
	for i in args:
		window[i].update(disabled = True)
def desactivar(window,*args):
	'''Desactiva el disabled de las coordenadas que se pasen por parametro'''
	for i in args:
		window[i].update(disabled = False)		

def guardarP(window,totalJug,totalComp,consonantes,vocales,nivel,current_time,tiempo,clasificacionAleatoria,ScrDic,cantCambFichas,puntJueg,fichasComp):
	'''Guarda los datos de la partida: la cantidad y el valor de las fichas,el tiempo total, el tiempo que iba cuando se guardo,
		el puntaje de la computadora y el del jugador,la cantidad de cambios, las fichas de los dos atriles,el nivel y el/los tipo/s de
		palabra/s que tiene que buscar'''
	dictGuardar = {}
	dictGuardar['PuntajeJug']= totalJug #guardo el puntaje del jugador
	dictGuardar['PuntajeComp']= totalComp #guardo el puntaje de la computadora
	dictGuardar['ConsonantesFichas']= consonantes #guardo el total de fichas que queda
	dictGuardar['VocalesFichas']= vocales #guardo el total de fichas que queda
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
def crearDicTablero(window,ScrDic,nivel):
	''' Creo un diccionario(segun el nivel) con la informacion del tablero: el color del casillero, el valor del casillero,
		el tipo de valor del casillero, el color del casillero cuando se ubica la letra.Esto me sirve para guardar partida, en
		caso de querer guardarla.''' 
	for i in range(1,16):
		for j in range(1,16):		
			if(i,j) in naranja:
				x = window[(i,j)].GetText()								
				if x == 'Px3':
					puntajeCa = 3#<-- suma puntaje al casillero	
					letraOpalabra= 'palabra'#<--- multiplica palabra
					color=("white", "orange")
				else:
					puntajeCa = 3	
					letraOpalabra= 'descuenta'#<---resta puntos
					color = ("white", "darkred")						
				ScrDic[(i,j)]={'color':color,'colorLetraUbi':color,'letra':'','puntImp':x,'puntajeC':puntajeCa,'letOpal':letraOpalabra}        
			elif (i,j) in verde:
				x = window[(i,j)].GetText()
				if x == 'Lx2':
					puntajeCa = 2	
					letraOpalabra= 'letra'#<--- multiplica letra
					color=("white", "green")
				else:
					puntajeCa = 2	
					letraOpalabra= 'descuenta'
					color=("white", "darkblue")        
				ScrDic[(i,j)]={'color':color,'colorLetraUbi':color,'letra':'','puntImp':x,'puntajeC':puntajeCa,'letOpal':letraOpalabra}       
			elif (i,j) in azul:
				x = window[(i,j)].GetText()
				ScrDic[(i,j)]={'color':("white", "blue"),'colorLetraUbi':("white", "blue"),'letra':'','puntImp':x,'puntajeC':3,'letOpal':'letra'}       
			elif (i,j) in rojo:
				x = window[(i,j)].GetText()
				if x == 'Px2':
					puntajeCa = 2	
					letraOpalabra= 'palabra'
					color=("white", "red")
				else:
					puntajeCa = 1	
					letraOpalabra= 'descuenta' 
					color=("white", "purple")       
				ScrDic[(i,j)]={'color':color,'colorLetraUbi':color,'letra':'','puntImp':x,'puntajeC':puntajeCa,'letOpal':letraOpalabra}        
			else:
				if nivel == 'Facil':
					color = ("white", "lightblue")
				elif nivel == 'Medio':
					color = ("white", "lightgreen")
				else:
					color = ("white", "pink")		        
				ScrDic[(i,j)]={'color':color,'colorLetraUbi':color,'letra':'','puntImp':'','puntajeC':0,'letOpal':''} 

def temaNivel(nivel):
	''' Segun el nivel que eligieron, toma distinto color la pantalla'''	
	if nivel == 'Facil':
		sg.theme('DarkBlue10')
	elif nivel == 'Medio':
		sg.theme('DarkGreen1')
	else:
		sg.theme('DarkRed2')		
def time_as_int():
	'''Devuelve el tiempo'''
	return int(round(time.time() * 100))
				
naranja = [(1,1),(15,15),(1,15),(15,1),(1,8),(15,8),(8,1),(8,8),(8,15)]
verde = [(1,4),(1,12),(15,4),(15,12),(3,7),(3,9),(13,7),(13,9),(4,1),(4,8),(4,15),(12,1),(12,8),(12,15),(7,3),(7,13),(9,3),(9,13),(8,4),(8,12)]
azul = [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(2,6),(2,10),(14,6),(14,10),(6,2),(6,14),(10,2),(10,14),(7,7),(7,9),(9,7),(9,9)]
rojo = [(2,2),(3,3),(4,4),(5,5),(6,6),(10,10),(11,11),(12,12),(13,13),(14,14),(2,14),(3,13),(4,12),(5,11),(6,10),(10,6),(11,5),(12,4),(13,3),(14,2)]

def main(nivel='',tiempo= 0,carga='',diccionarioC ={},diccionarioV ={},actual={}):
	temaNivel(nivel)
	colIzq =  [[sg.Button(puntaje_casillero(i,j,nivel,naranja,verde,azul,rojo),button_color=calcular(i,j,naranja,verde,azul,rojo,nivel),size=(5, 2), key=(i,j), pad=(0,0)) for j in range(1,16)] for i in range(1,16)]
	colDer =[
			[sg.Text('Computadora:',size =(100,None),justification='left',text_color='yellow')],
			[sg.Button('?',button_color=color_button,size=tam_button, key=(100,i+1))for i in range(7)],
			[sg.Text('______________________________________________________',text_color='red')],
			[sg.Text('puntaje Computadora:'),sg.In(0, key=(40,40),text_color='black',size=tam_button,disabled = True)],
			[sg.Text('')],
			[sg.Text('')],
			[sg.Text('nivel:                    '),sg.In('', key=(50,50),text_color='black',size=(24,2),disabled = True)],
			[sg.Text('palabras a buscar:'),sg.In('', key=(60,60),text_color='black',size= (24,2),disabled = True)],
			[sg.Text("Fichas restantes: "),sg.In(0, key=(20,20),text_color='black',size=(24,2),disabled = True)],
			[sg.Text('')],
			[sg.Text('Tiempo:'),sg.Text('', size=(8, 1), font=('Helvetica', 20),justification='center', key='text')],
			[sg.Text('')],
			[sg.Text('')],
			[sg.Text('cantidad de cambios:'),sg.In(0, key=(70,70),text_color='black',size=(2,2),disabled = True)],
			[sg.Text('puntaje Jugador:'),sg.In(0, key=(30,30),text_color='black',size=tam_button,disabled = True)],
			[sg.Text('______________________________________________________',text_color='red')],
			[sg.Text('Jugador:',size =(100,None),justification='left',text_color='yellow')],
			[sg.Button('',button_color=color_button,size=tam_button, key=(0,i+1))for i in range(7)]]
	colDer.append([sg.Button('Evaluar', key=(0,8),button_color=('black','gray'),size=tam_button),sg.Button('Cambiar Fichas', key=(0,11),button_color=('black','gray'),size=(6,2)),sg.Button('Devolver Fichas', key=(0,9),button_color=('black','gray'),size=(6,2)),sg.Button('Pasar', key=(0,10),button_color=('black','gray'),size=tam_button),sg.Button('Guardar partida', key=(0,12),button_color=('black','gray'),size=(7,2)),sg.Button('Terminar Partida', key=(0,13),button_color=('black','gray'),size=(7,2))])

	layout = [[sg.Column(colIzq,size=(750,750)),sg.Column(colDer,size=(700,700))]]
	window = sg.Window('Scrabble',layout).Finalize()
	window.Maximize()		
	ScrDic = {}
	crearDicTablero(window,ScrDic,nivel)	
	valor_A = ''
	valor_B = '' 
	fichasComp={} 	                 
#------------------------------------------------------------------------------------------------------		 
	if carga != 'nuevo':#<--- si no es distinto de '', significa que se cargo la partida

		tiempo= actual['TiempoTotal']
		resta= actual['Tiempo']
		clasificacionAleatoria = actual['clasificacionAleatoria']
		cantCambFichas = actual['cantCambFichas']
		window[(70,70)].update(cantCambFichas)
		puntJueg = actual['puntJueg'] 
		totalJug= actual['PuntajeJug']
		window[(30,30)].update(totalJug)
		totalComp= actual['PuntajeComp']
		window[(40,40)].update(totalComp)
		consonantes=actual['ConsonantesFichas']
		vocales=actual['VocalesFichas']
		window[(60,60)].update(clasificacionAleatoria)
		window[(20,20)].update(sum(actual['ConsonantesFichas'].values()) + sum(actual['VocalesFichas'].values()))
		botones = {}		
		for i in range(7):
			window[0,i+1].update(actual['FichasAtrilJug'][i])
			fichasComp[100,i+1]=actual['FichasAtrilComp'][i]
			botones[0,i+1] = actual['FichasAtrilJug'][i]
		
		for i in range(len(actual['ClavesCasillero'])):
			clave= actual['ClavesCasillero'][i]#<--obtengo la clave del casillero
			coordenada=tuple((map(int,clave.split(','))))#<--convierto la clave que estaba en string a tupla 
			ScrDic[coordenada]=actual[actual['ClavesCasillero'][i]]#<--guardo en el diccionario los datos de ese casillero
			window[coordenada].update(ScrDic[coordenada]['letra'], button_color=ScrDic[coordenada]['colorLetraUbi'],disabled_button_color=ScrDic[coordenada]['colorLetraUbi'],disabled=True)#<--coloco la letra en la interfaz	
	
	else:#<--- sino, inicia una nueva
		cantCambFichas = 3
		window[(70,70)].update(cantCambFichas)
		resta= 0
		tiempo=tiempo * 6000
		consonantes = diccionarioC
		vocales={'A':0,'E':0,'I':0,'O':0,'U':0}
		for i in vocales.keys():
			vocales[i]=consonantes[i]
			del consonantes[i]
		puntJueg = diccionarioV
		botones = {(0,1):fichas(consonantes,vocales,1),(0,2):fichas(consonantes,vocales,2),(0,3):fichas(consonantes,vocales,3),(0,4):fichas(consonantes,vocales,4),(0,5):fichas(consonantes,vocales,5),(0,6):fichas(consonantes,vocales,6),(0,7):fichas(consonantes,vocales,7)} 		
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
			fichasComp[100,i+1]=fichas(consonantes,vocales,i+1)
		window[(20,20)].update(sum(consonantes.values()) + sum(vocales.values()))
		totalJug=0#<--- puntaje total del jugador
		totalComp =0#<------- puntaje total de la computadora		
		listaTurno=['comp','jug']
		eleccion = random.choice(listaTurno)	
		if eleccion == 'comp':
			activar(window,(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9),(0,10),(0,11),(0,12),(0,13))
			palabras_existentes= turnoComputadora.turno(clasificacionAleatoria,fichasComp,nivel)
			if len(palabras_existentes) == 0:#<--- si la computadora no tiene palabras y hay mas fichas,las cambia	
				sg.popup('la computadora no encontro palabra')
			else:
				palabraUbi,encontro,listaCoorLetrasUbicadas = turnoComputadora.buscarTablero(palabras_existentes,ScrDic)
				if not encontro: #<---- si la computadora no encontro lugar y  hay mas fichas,cambia las fichas
					turnoComputadora.cambiarFichas(fichasComp,consonantes,vocales,window)
					sg.popup('la computadora no encontro ubicacion')
				else:	
					sumaComp= turnoComputadora.sumarPuntaje(window,listaCoorLetrasUbicadas,ScrDic,puntJueg)
					turnoComputadora.nuevasFichas(palabraUbi,fichasComp,window,consonantes,vocales)
					window[(20,20)].update(sum(consonantes.values()) + sum(vocales.values()))#con esto puedo sumar para ver si el diccionario no tiene fichas
					totalComp = totalComp + sumaComp
					window[(40,40)].update(totalComp)
					listaCoorLetrasUbicadas = []
				#----activa evaluar y cambiar fichas	
			desactivar(window,(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9),(0,10),(0,11),(0,12),(0,13))		
	window[(50,50)].update(nivel)			
	guardado ={}#<--- guarda la ubicacion y la letra en donde se ubico la ficha en el tablero
	guardadoAtril = []#<---- guarda las coordenadas del atril del jugador: de las fichas que uso
	palabra = []#<----guarda las letras de la palabra
	ubicacion = []#<---guarda las coordenadas de donde se ubicaron las letras en el tablero
	listaCoorLetrasUbicadas = []#<---- es la lista de las coordenadas donde la computadora ubico la palabra en el tablero
	Termino = False#<--- si da true es porque seguirJ es igual a false, lo evalua cuando de apreta pasar	
	current_time = 0
	start_time =  time_as_int() - resta#<--- con esto empiezo desde el tiempo en que me quede					
	while True:
		event, values = window.read(timeout=10)
		current_time = time_as_int() - start_time
		if current_time >= tiempo:#<-- esto corta el programa a los 60 segundos
			evaluarGanador(totalJug,totalComp,nivel)
			break		
		if Termino:#<---- si estos dos son false, ya no se puede seguir jugando
			evaluarGanador(totalJug,totalComp,nivel)
			break		
		if event in (None, 'Exit'):
			break					
		elif event != (0,8) and event != (0,9) and event != (0,10) and event != (0,11) and event != (0,12) and event != (0,13):#<--------si no es evaluar,modificar,pasar 		
			if event in botones.keys():#<------entra si se apreto los botones del atril	
				valor_A = window[event].GetText()#<----toma la letra del boton del atril 
				window[event].update('', button_color = color_button)
				activar(window,(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9),(0,10),(0,11),(0,12),(0,13))
				if window[(8,8)].GetText() == 'Px3':#<------si no hay ficha en el casillero del medio
					window[(8,8)].update(valor_A, disabled_button_color=('white','black'), button_color=('white','black'),disabled=True)#<---
					window[event].update(text='')
					ubicacion.append((8,8))
					guardadoAtril.append(event)
					guardado[(8,8)] = valor_A
					desactivar(window,(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9),(0,10),(0,11),(0,12),(0,13))
				else:	
					keys_entered = event#<--- guarda el event 	
					event, values = window.read()
					
					if event in (None, 'Exit'):#<--------en caso de se haya apretado un boton del atril y se cierre
						break					
					elif event not in botones.keys():#<-------si no es un boton del atril 
						valor_B = window[event].GetText()#<----toma la letra del segundo event
						if valor_B == '' or valor_B == 'Px2' or valor_B == 'Px3' or valor_B == 'Lx2' or valor_B == 'Lx3' or valor_B == 'Des1' or valor_B == 'Des2' or valor_B == 'Des3':#<---probando px2
							window[event].update(valor_A, disabled_button_color=('white','black'), button_color=('white','black'),disabled=True)#<---
							window[keys_entered].update(text='')
							ubicacion.append(event)
							guardadoAtril.append(keys_entered)
							guardado[event] = valor_A
						desactivar(window,(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9),(0,10),(0,11),(0,12),(0,13))
						
		elif event == (0,8):#<----apreto evaluar
			if len(ubicacion) == 0:
				sg.popup('no coloco ninguna ficha en el tablero, no se puede evaluar')
			elif len(ubicacion) == 1:
				sg.popup('debe colocar 2 fichas minimo, no se puede evaluar')
				turnoJugador.devolverAtril(ubicacion,window,ScrDic,guardadoAtril,botones)					
			else:			
				incorrecto,ubicacion= turnoJugador.evaluarUbi(ubicacion)
				if incorrecto:#<---- si es incorrecto por ubicacion, vuelve las fichas al lugar
					turnoJugador.devolverAtril(ubicacion,window,ScrDic,guardadoAtril,botones)

				else:
					for i in ubicacion:#<---- utilizo las ubicaciones ordenadas, para sacar la palabra 
						palabra.append(guardado[i])			
					strPal=''.join(palabra).lower()#<-----transformo la lista en string
					if clasificar(strPal,nivel,clasificacionAleatoria):
						for i in ubicacion:
							window[i].update(disabled_button_color=('white','black'),disabled=True)
						sg.popup('se ubico la palabra')	
						totalJug = turnoJugador.sumoPalabra(ubicacion,ScrDic,palabra,puntJueg,totalJug,window)

						turnoJugador.pidoFichasNuevas(guardadoAtril,botones,consonantes,vocales,window)
						if any(botones[i] == '' for i in botones.keys()):
							Termino=True	
						#---desactiva evaluar y cambiar fichas						
						activar(window,(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9),(0,11),(0,12),(0,13))
					else:
						sg.popup('la palabra no es correcta,vuelva a intentarlo')
						turnoJugador.devolverAtril(ubicacion,window,ScrDic,guardadoAtril,botones)
						
					palabra=[]			
			guardado,guardadoAtril,ubicacion=turnoJugador.vaciar()	
							
		elif event == (0,9):#modificar
			#devolver la fichas al atril,en caso de que te hayas equivocado antes de evaluar la palabra
			turnoJugador.devolverAtril(ubicacion,window,ScrDic,guardadoAtril,botones)
			guardado,guardadoAtril,ubicacion=turnoJugador.vaciar()			
		elif event == (0,11):#<----cambio las fichas
			if len(ubicacion) != 0:
				turnoJugador.devolverAtril(ubicacion,window,ScrDic,guardadoAtril,botones)
				guardado,guardadoAtril,ubicacion=turnoJugador.vaciar()
			#----------------------------------------
			if cantCambFichas != 0:
				sg.popup('haga click en las fichas que quiera cambiar y luego haga click en cambiar fichas')
				activar(window,(0,8),(0,9),(0,10),(0,12),(0,13))
				event, values = window.read()
				listaFcambiar= []
				while event !=(0,11):#se guarda en una lista las coordenadas de las fichas que quiere cambiar el jugador
					listaFcambiar.append(event)
					window[event].update(disabled = True)
					event, values = window.read()
				activar(window,(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,11))
				desactivar(window,(0,10),(0,12),(0,13))	
				for i in listaFcambiar:
					if i[1] == 2 or i[1] == 4:
						if botones[i] in vocales:
							vocales[botones[i]] = vocales[botones[i]] + 1
						else:
							vocales[botones[i]] = 1
					elif i[1] == 7:
						if botones[i] == 'A' or botones[i] == 'E' or botones[i] == 'I' or botones[i] == 'O' or botones[i] == 'U': 
							if botones[i] in vocales:
								vocales[botones[i]] = vocales[botones[i]] + 1
							else:
								vocales[botones[i]] = 1
						else:
							if botones[i] in consonantes:
								consonantes[botones[i]] = consonantes[botones[i]] + 1
							else:
								consonantes[botones[i]] = 1	
					else:
						if botones[i] in consonantes:
							consonantes[botones[i]] = consonantes[botones[i]] + 1
						else:
							consonantes[botones[i]] = 1
				 		
					botones[i]=fichas(consonantes,vocales,i[1])

					window[i].update(text= botones[i])
				cantCambFichas = cantCambFichas - 1
				window[(70,70)].update(cantCambFichas)
			else:
				sg.popup('ya utilizo los 3 cambios de fichas')		
		elif event == (0,12):#guardar partida
			if len(ubicacion) != 0:
				turnoJugador.devolverAtril(ubicacion,window,ScrDic,guardadoAtril,botones)
				guardado,guardadoAtril,ubicacion=turnoJugador.vaciar()

			guardarP(window,totalJug,totalComp,consonantes,vocales,nivel,current_time,tiempo,clasificacionAleatoria,ScrDic,cantCambFichas,puntJueg,fichasComp)	
			break
		elif event == (0,13):#terminar partida
			evaluarGanador(totalJug,totalComp,nivel)
			break		
		else:			
			if len(ubicacion) != 0:				
				turnoJugador.devolverAtril(ubicacion,window,ScrDic,guardadoAtril,botones)
				guardado,guardadoAtril,ubicacion=turnoJugador.vaciar()								
	
			palabras_existentes= turnoComputadora.turno(clasificacionAleatoria,fichasComp,nivel)
			#-----------------------------------------------------------------------			
			if len(palabras_existentes) == 0 and (sum(consonantes.values()) + sum(vocales.values())) == 0:#<--- si la computadora no tiene palabras y no hay mas fichas,no puede seguir
				Termino=True
			elif len(palabras_existentes) == 0:#<--- si la computadora no tiene palabras y hay mas fichas,las cambia
				turnoComputadora.cambiarFichas(fichasComp,consonantes,vocales,window)
				sg.popup('la computadora no encontro palabra')
			else:#<---sino, busca la ubicacion en el tablero	
				palabraUbi,encontro,listaCoorLetrasUbicadas = turnoComputadora.buscarTablero(palabras_existentes,ScrDic)
				#--------------------------------------------------------------------------------------------------		
				if not encontro and (sum(consonantes.values()) + sum(vocales.values())) == 0:#<--- si la computadora no encontro lugar y no hay mas fichas,no puede seguir
					Termino=True
				elif not encontro: #<---- si la computadora no encontro lugar y  hay mas fichas,cambia las fichas
					turnoComputadora.cambiarFichas(fichasComp,consonantes,vocales,window)

					sg.popup('la computadora no encontro ubicacion')
				else:#<------ sino, encontro lugar y la ubica en la interfaz
					sumaComp= turnoComputadora.sumarPuntaje(window,listaCoorLetrasUbicadas,ScrDic,puntJueg)
					#-----------------------------------------------------------------------------------------------
					turnoComputadora.nuevasFichas(palabraUbi,fichasComp,window,consonantes,vocales)
					if any(fichasComp[i] == '' for i in fichasComp.keys()):
						Termino=True
					#--------------------------------------------------------------
					window[(20,20)].update(sum(consonantes.values()) + sum(vocales.values()))#con esto puedo sumar para ver si el diccionario no tiene fichas
					totalComp = totalComp + sumaComp
					window[(40,40)].update(totalComp)
					listaCoorLetrasUbicadas = []
					#----activa evaluar y cambiar fichas	
			desactivar(window,(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(0,8),(0,9),(0,10),(0,11),(0,12),(0,13))
		window['text'].update('{:02d}:{:02d}'.format((current_time // 100) // 60,(current_time // 100) % 60))
	window.close()	
if __name__ == '__main__':
	nivel='Facil'
	nombre='jorge'
	diccionarioC = configuracionScrabble.cantidadPred()
	diccionarioV = configuracionScrabble.valorPred()	
	main(nivel,20,'nuevo',diccionarioC ,diccionarioV )
