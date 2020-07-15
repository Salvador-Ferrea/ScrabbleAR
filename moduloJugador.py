import PySimpleGUI as sg
from pattern.es import spelling,lexicon,parse

import moduloIA

import itertools as it

import random

import os.path as path

import json

import time



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
				
def leerPartidasGuardadas():#<---leo el archivo de las partidas guardadas
	with open('partidasGuardadas.json', 'r') as archivo:
		datos = json.load(archivo)
	return datos

def escribirPartidasGuardadas(jugadores):#<---escribo en el archivo  las partidas guardadas
	with open('partidasGuardadas.json', 'w') as archivo:
		json.dump(jugadores, archivo,indent=4)				
	
		

def main(nivel='',tiempo= 0,nombre=''):
	
	naranja = [(1,1),(15,15),(1,15),(15,1),(1,8),(15,8),(8,1),(8,8),(8,15)]
	verde = [(1,4),(1,12),(15,4),(15,12),(3,7),(3,9),(13,7),(13,9),(4,1),(4,8),(4,15),(12,1),(12,8),(12,15),(7,3),(7,13),(9,3),(9,13),(8,4),(8,12)]
	azul = [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(2,6),(2,10),(14,6),(14,10),(6,2),(6,14),(10,2),(10,14),(7,7),(7,9),(9,7),(9,9)]
	rojo = [(2,2),(3,3),(4,4),(5,5),(6,6),(10,10),(11,11),(12,12),(13,13),(14,14),(2,14),(3,13),(4,12),(5,11),(6,10),(10,6),(11,5),(12,4),(13,3),(14,2)]
	
	if nombre!= '':#<--- si el nombre es distinto a '' significa que esta cargado
		cargarA = leerPartidasGuardadas()
		actual = cargarA[nombre]
		nivel = actual['Nivel']
		tiempo= actual['TiempoTotal']
		resta= actual['Tiempo']
	else:
		resta= 0
		tiempo=tiempo * 6000 

	puntJueg = {'A':1,'B':3,'C':2,'D':2,'E':1,'F':4,'G':2,'H':4,'I':1,'J':6,'K':6,'L':1,'LL':8,'M':3,'N':1,'Ñ':8,'O':1,'P':3,'Q':8,'R':1,'RR':8,'S':1,'T':1,'U':1,'V':4,'W':8,'X':8,'Y':4,'Z':10}

	colIzq =  [[sg.Button(puntaje_casillero(i,j,nivel,naranja,verde,azul,rojo),button_color=calcular(i,j,naranja,verde,azul,rojo),size=(5, 2), key=(i,j), pad=(0,0)) for j in range(1,16)] for i in range(1,16)]
	colDer =[
			[sg.Text('Computadora:',size =(100,None),justification='left',text_color='yellow')],
			[sg.Button('',button_color=color_button,size=tam_button, key=(100,i+1))for i in range(7)],
			[sg.Text('______________________________________________________',text_color='red')],
			[sg.Text('puntaje Computadora:'),sg.Button(0, key=(40,40),button_color=('black','gray'),size=tam_button)],
			[sg.Text('')],
			[sg.Text('')],
			[sg.Text('')],
			[sg.Text('')],
			[sg.Text("Fichas restantes: "),sg.Button(0, key=(20,20),button_color=('black','gray'),size=tam_button)],
			[sg.Text('')],
			[sg.Text('Tiempo:'),sg.Text('', size=(8, 1), font=('Helvetica', 20),justification='center', key='text')],
			[sg.Text('')],
			[sg.Text('')],
			[sg.Text('')],
			[sg.Text('puntaje Jugador:'),sg.Button(0, key=(30,30),button_color=('black','gray'),size=tam_button)],
			[sg.Text('______________________________________________________',text_color='red')],
			[sg.Text('Jugador:',size =(100,None),justification='left',text_color='yellow')],
			[sg.Button('',button_color=color_button,size=tam_button, key=(0,i+1))for i in range(7)]]
	colDer.append([sg.Button('Evaluar', key=(0,8),button_color=('black','gray'),size=tam_button),sg.Button('Cambiar Fichas', key=(0,11),button_color=('black','gray'),size=(6,2)),sg.Button('Devolver Fichas', key=(0,9),button_color=('black','gray'),size=(6,2)),sg.Button('Pasar', key=(0,10),button_color=('black','gray'),size=tam_button),sg.Button('Guardar partida', key=(0,12),button_color=('black','gray'),size=(7,2))])

	layout = [[sg.Column(colIzq,size=(750,750)),sg.Column(colDer,size=(700,700))]]
	window = sg.Window('Scrabble',layout).Finalize()
	window.Maximize()

		
	ScrDic = {}

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

	valor_A = ''

	valor_B = ''                   
#------------------------------------------------------------------------------------------------------
#idea para retornar datos:

	if nombre != '':#<--- si no es distinto de '', significa que se cargo la partida
		letras_total={}
		totalJug= actual['PuntajeJug']
		window[(30,30)].update(totalJug)
		totalComp= actual['PuntajeComp']
		window[(40,40)].update(totalComp)
		letras_total=actual['TotalFichas']
		window[(20,20)].update(sum(actual['TotalFichas'].values()))
		botones = {}
		for i in range(7):
			window[0,i+1].update(actual['FichasAtrilJug'][i])
			window[100,i+1].update(actual['FichasAtrilComp'][i])
			botones[0,i+1] = actual['FichasAtrilJug'][i]
		
		for i in range(len(actual['ClavesCasillero'])):
			clave= actual['ClavesCasillero'][i]#<--obtengo la clave del casillero
			coordenada=tuple((map(int,clave.split(','))))#<--convierto la clave que estaba en string a tupla 
			ScrDic[coordenada]=actual[actual['ClavesCasillero'][i]]#<--guardo en el diccionario los datos de ese casillero
			window[coordenada].update(ScrDic[coordenada]['letra'], button_color=ScrDic[coordenada]['colorLetraUbi'])#<--coloco la letra en la interfaz
	
	else:#<--- sino, inicia una nueva
		# total de fichas:

		#hago el diccionario
		letras_total = {'A': 11,'B':3,'C':4,'D':4,'E':11,'F':2,'G':2,'H':2,
		'I':6,'J':2,'K':1,'L':4,'M':3,'N':5,'Ñ':1,'O':8,'P':2,'Q':1,'R':4,
		'S':7,'T':4,'U':6,'V':2,'W':1,'X':1,'Y':1,'Z':1}
		#con esto puedo sumar para ver si el diccionario no tiene fichas
		botones = {(0,1):fichas(letras_total),(0,2):fichas(letras_total),(0,3):fichas(letras_total),(0,4):fichas(letras_total),(0,5):fichas(letras_total),(0,6):fichas(letras_total),(0,7):fichas(letras_total)} 

		for i in range(7):
			window[0,i+1].update(botones[0,i+1])
			window[100,i+1].update(fichas(letras_total))
		window[(20,20)].update(sum(letras_total.values()))
		totalJug=0#<--- puntaje total del jugador
		totalComp =0#<------- puntaje total de la computadora
		
	print(sum(letras_total.values()))
	
	#print(dictGuardar['ClavesCasillero'][0].keys())<----es para acceder a la clave(coordenadas)
#-----------------------------------------------------------------------------------------------------	
	#botones = {(0,1):fichas(letras_total),(0,2):fichas(letras_total),(0,3):fichas(letras_total),(0,4):fichas(letras_total),(0,5):fichas(letras_total),(0,6):fichas(letras_total),(0,7):fichas(letras_total)} 
	#for i in range(7):
	#	window[0,i+1].update(botones[0,i+1])
	#	window[100,i+1].update(fichas(letras_total))
	guardado ={}#<--- guarda la ubicacion y la letra en donde se ubico la ficha en el tablero
	guardadoAtril = []#<---- guarda las coordenadas del atril del jugador: de las fichas que uso
	palabra = []#<----guarda las letras de la palabra
	ubicacion = []#<---guarda las coordenadas de donde se ubicaron las letras en el tablero
	#totalJug=0#<--- puntaje total del jugador
	listaCoorLetrasUbicadas = []#<---- es la lista de las coordenadas donde la computadora ubico la palabra en el tablero
	fichasComp={}#<---guarda la ubicacion y la letra de las fichas del atril de la computadora
	#totalComp =0#<------- puntaje total de la computadora
	seguirJ = True#<-- si da false es que el jugador no puede jugar mas y no hay mas fichas
	seguirC= True#<-- si da false es que la computadora no puede jugar mas y no hay mas fichas
	def time_as_int():
		return int(round(time.time() * 100))
	current_time = 0
	start_time =  time_as_int() - resta#<--- con esto empiezo desde el tiempo en que me quede
	while True:
		event, values = window.read(timeout=10)
		current_time = time_as_int() - start_time
		if current_time == tiempo:#<-- esto corta el programa a los 60 segundos
			break
		'''	
		#-----------------------------------------------------------------
		
		if not seguirJ  and not seguirC:#<---- si estos dos son false, ya no se puede seguir jugando
			
			-termina el juego y hay un ganador
			-aca tiene que anotar en el top 10 en el caso de que el puntaje sea muy bueno
			
			break
		
		#-----------------------------------------------------------------	
		'''
		if event in (None, 'Exit'):
			break
					
		elif event != (0,8) and event != (0,9) and event != (0,10) and event != (0,11) and event != (0,12):#<--------si no es evaluar,modificar,pasar 
		
			if event in botones.keys():#<------entra si se apreto los botones del atril	
				valor_A = window[event].GetText()#<----toma la letra del boton del atril 
				
				if window[(8,8)].GetText() == 'Px3':#<------si no hay ficha en el casillero del medio
					window[(8,8)].update(valor_A, button_color=('white','black'))#<---
					window[event].update(text='')
					#palabra.append(valor_A)
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
							#palabra.append(valor_A)
							ubicacion.append(event)
							guardadoAtril.append(keys_entered)
							guardado[event] = valor_A	
					else:#<------si es un boton del atril
						valor_B = window[event].GetText()
						window[keys_entered].update(valor_B)
						window[event].update(valor_A)
			
				
			#else:#<------si se toca en el tablero, no hace nada
				
		elif event == (0,8):#<----apreto evaluar
		
		
			encontroX= True#
			encontroY= True#
			antX=ubicacion[0][0]#
			antY=ubicacion[0][1]#
			print(antX)
			print(antY)
			for i in range(len(ubicacion)):#
				if i != 0:
					if(antX != ubicacion[i][0]):#<-----verifico si la ubicacion es vertical,horizontal, o esta mal ubicada 
						encontroX=False#
								
					if(antY != ubicacion[i][1] ):#<-----verifico si la ubicacion es vertical,horizontal, o esta mal ubicada
						encontroY=False#
				
#------------------------------------------------------------------	
			if encontroX == False and	encontroY == True:#<---- si es vertical/horizontal, verifico si son consecutivas 
				ubicacion = sorted(ubicacion, key=lambda tup: tup[0])
			
				x= ubicacion[0][0]
		
				incorrecto= False
				for i in range(len(ubicacion)):
					if i != 0:
					
						if ubicacion[i][0] == x+1:
							x=x+1
						else:
							incorrecto = True
							break
					
#-----------------------------------------------------------------
			elif encontroX == True and encontroY == False:#<---- si es vertical/horizontal, verifico si son consecutivas 
				ubicacion = sorted(ubicacion, key=lambda tup: tup[1])
			
				y= ubicacion[0][1]
		
				incorrecto= False
				for i in range(len(ubicacion)):
					if i != 0:
					
						if ubicacion[i][1] == y+1:
							y=y+1
						else:
							incorrecto = True
							break
					
			elif encontroX == False and encontroY == False:#<---- si no es vertical/horizontal, es incorrecto=false 
				incorrecto = True
			else:
				incorrecto=False				
			if incorrecto:#<---- si es incorrecto por ubicacion, vuelve las fichas al lugar
				sg.popup('ubicacion incorrecta vuelva a intentarlo')
				for i in range(len(ubicacion)):
					window[ubicacion[i]].update(ScrDic[ubicacion[i]]['puntImp'], button_color = ScrDic[ubicacion[i]]['color'])	
				for i in guardadoAtril:
						window[i].update(text= botones[i])
				
				guardado={}
				guardadoAtril=[]
				ubicacion=[]
			
			else:
			
				for i in ubicacion:#<---- utilizo las ubicaciones ordenadas, para sacar la palabra 
					palabra.append(guardado[i])
			
				strPal=''.join(palabra).lower()#<-----transformo la lista en string
				if strPal in spelling.keys() or strPal in lexicon.keys():#<-----evaluo la palabra, si es correcta ubica la palabra
					sg.popup('se ubico la palabra')
					multPalab=0
					descuent=0
					puntPalab=0
					suma=0
					for i in range(len(ubicacion)):
						ScrDic[ubicacion[i]]['letra'] = palabra[i]#<----guardo la letra en el diccionario del tablero(para el turno de la computadora)
						ScrDic[ubicacion[i]]['colorLetraUbi'] = ('white','black') #<--- guardo el color de la letra ubicada para poder reestablecerla en la interfaz despues(en caso de querer guardar la partida)
						if ScrDic[ubicacion[i]]['letOpal'] == 'palabra':
							multPalab=multPalab + ScrDic[ubicacion[i]]['puntajeC']
							puntPalab= puntPalab + puntJueg[palabra[i]]
						elif ScrDic[ubicacion[i]]['letOpal'] == 'letra':
							puntPalab= puntPalab + (puntJueg[palabra[i]] * ScrDic[ubicacion[i]]['puntajeC'])
						elif ScrDic[ubicacion[i]]['letOpal'] == 'descuenta':
							descuent = descuent + ScrDic[ubicacion[i]]['puntajeC']
							puntPalab= puntPalab + puntJueg[palabra[i]]
						else:		
							puntPalab= puntPalab + puntJueg[palabra[i]]
					suma= puntPalab - descuent
					if multPalab != 0:
						suma = suma * multPalab	
					#----------------------------------------------------------------------------------------
					
					if sum(letras_total.values()) == 0:#<---- si no hay mas fichas en la bolsa
						seguirJ=False
					else: #<---- si  hay mas fichas en la bolsa, pide nuevas fichas
							
						#----------------------------------------------------------------------------------------	
						for i in guardadoAtril:#<----pido nuevas fichas, y las pongo en el atril y en el diccionario botones
							botones[i]=fichas(letras_total)
							window[i].update(text= botones[i])
						window[(20,20)].update(sum(letras_total.values()))#con esto puedo sumar para ver si el diccionario no tiene fichas
						totalJug = totalJug + suma
						window[(30,30)].update(totalJug)
						#---desactiva evaluar y cambiar fichas
						window[(0,8)].update(disabled = True)
						window[(0,11)].update(disabled = True)
					
						ubicacion = []
						palabra = []
						guardadoAtril=[]
						guardado={}
				else:#<--- si es incorrecta la palabra,vuelve las fichas al lugar
					sg.popup('la palabra no es correcta,vuelva a intentarlo')
					for i in range(len(ubicacion)):
						window[ubicacion[i]].update(ScrDic[ubicacion[i]]['puntImp'], button_color = ScrDic[ubicacion[i]]['color'])	
					#ubicacion = []
					for i in guardadoAtril:
						window[i].update(text= botones[i])
					guardado={}
					guardadoAtril=[]
					ubicacion=[]
					palabra=[]
					if sum(letras_total.values()) == 0:#<---- si no hay mas fichas en la bolsa
						seguirJ=False
					
		elif event == (0,9):#modificar
			#devolver la fichas al atril,en caso de que te hayas equivocado antes de evaluar la palabra
			for i in range(len(ubicacion)):
				window[ubicacion[i]].update(ScrDic[ubicacion[i]]['puntImp'], button_color = ScrDic[ubicacion[i]]['color'])	
				
			for i in guardadoAtril:
				window[i].update(text= botones[i])
			guardado={}
			guardadoAtril=[]
			ubicacion=[]
		elif event == (0,11):#<----cambio las fichas
			print('cambiar')
			if len(ubicacion) != 0:
				for i in range(len(ubicacion)):
					window[ubicacion[i]].update(ScrDic[ubicacion[i]]['puntImp'], button_color = ScrDic[ubicacion[i]]['color'])				
				for i in guardadoAtril:
					window[i].update(text= botones[i])
				guardado={}
				guardadoAtril=[]
				ubicacion=[]
				
				
			for i in botones.keys():
				if botones[i] in letras_total:
					letras_total[botones[i]] = letras_total[botones[i]] + 1
				else:
					letras_total[botones[i]] = 1
			for i in botones.keys():#<----pido nuevas fichas, y las pongo en el atril y en el diccionario botones
				botones[i]=fichas(letras_total)
				window[i].update(text= botones[i])
			#---desactiva evaluar y cambiar fichas
			window[(0,8)].update(disabled = True)
			window[(0,11)].update(disabled = True)
		
		elif event == (0,12):#guardar partida
			if nombre=='':
				nombre = sg.popup_get_text('ingrese nombre para guardar partida', '')
			dictGuardar = {}
			dictGuardar['PuntajeJug']= totalJug #guardo el puntaje del jugador
			dictGuardar['PuntajeComp']= totalComp #guardo el puntaje de la computadora
			dictGuardar['TotalFichas']= letras_total #guardo el total de fichas que queda
			dictGuardar['Nivel']= nivel #guardo el nivel del juego 
			dictGuardar['Tiempo']= current_time #guardo el tiempo en el momento que se guardo
			dictGuardar['TiempoTotal']= tiempo #guardo el tiempo max que puede durar la partida
			dictGuardar['FichasAtrilComp']=[]
			dictGuardar['FichasAtrilJug']=[]
			for i in range(7):#<---guardo las fichas del atril de la computadora y del jugador
				dictGuardar['FichasAtrilJug'].append(window[(0,i+1)].GetText())
				dictGuardar['FichasAtrilComp'].append(window[(100,i+1)].GetText())
			
			dictGuardar['ClavesCasillero']=[]
			
			for i in range(1,16):	#guardo todos los casilleros del tablero
				for j in range(1,16):
					if ScrDic[(i,j)]['letra'] != '':
						a =	ScrDic[(i,j)]
						b =[str(i),str(j)] #tuve que pasar a string la tupla con las coordenadas pq me tiraba error para guardar en json
						c = ','.join(b) 
						dictGuardar[c] = a# guardo los datos de la coordenada en un diccionario
						dictGuardar['ClavesCasillero'].append(c)# guardo en una lista de las coordenadas
						
						
			if path.exists('partidasGuardadas.json'): # si el archivo existe
				print('existe archivo')
				archivoGuardados = leerPartidasGuardadas() 
				archivoGuardados[nombre] = dictGuardar
				escribirPartidasGuardadas(archivoGuardados)
			
			else:# si el archivo no existe
				print('no existe archivo')
				archGuardar = {}
				archGuardar[nombre] = dictGuardar
				escribirPartidasGuardadas(archGuardar)
			break	
		else:
			
			
			#turno computadora
			
			
			
			
			for i in range(7):#<---toma las fichas de la computadora
				
				fichasComp[(100,i+1)] = window[(100,i+1)].GetText()
				
			letras=''.join(fichasComp.values())#<-- el string de la palabra
			
			
			palabras = set()#<---tiene las permutaciones
			for i in range(2,len(letras)+1):
				palabras.update((map("".join, it.permutations(letras,i))))
			
			palabras_existentes=[]#<--- guarda las palabras que armo y que existen
			for i in palabras:
				
				if i in spelling.keys() or i in lexicon.keys():#dificultad=facil
					#verificar si la palabra es verbo o adjetivo parse()-> VB --JJ |--> dificultad medio dificil
					palabras_existentes.append(i)
					
			'''
			with open("palabras.json","w") as fil:
				#json.dump(res,fil,indent=4)
				json.dump(palabras_existentes,fil,indent=4)
			'''	
			#-----------------------------------------------------------------------
			
			if len(palabras_existentes) == 0 and sum(letras_total.values()) == 0:#<--- si la computadora no tiene palabras y no hay mas fichas,no puede seguir
				seguirC= False
			elif len(palabras_existentes) == 0:#<--- si la computadorano no tiene palabras y hay mas fichas,las cambia
				for i in fichasComp.keys():
					if fichasComp[i] in letras_total:
						letras_total[fichasComp[i]] = letras_total[fichasComp[i]] + 1
					else:
						letras_total[fichasComp[i]] = 1
				for i in fichasComp.keys():#<----pido nuevas fichas, y las pongo en el atril y en el diccionario fichasComp
					fichasComp[i]=fichas(letras_total)
					window[i].update(text= fichasComp[i])
			else:#<---sino, busca la ubicacion en el tablero	
				
				#-----------------------------------------------------------
				#Con la lista de palabras existentes(las ordeno de mayor a menor) busco la ubicacion en el tablero
				palabras_existentes.sort(key=len,reverse=True)
				x = ''# lo uso como guia, en caso de que la palabra que envie no se pueda ubicar,si el largo de la palabra anterior es igual
					# al largo de la palabra actual, no busca ubicacion
				palabraUbi = ''	
				encontro= False
				for i in palabras_existentes:
					if len(x) != len(i):
						x = i
						if moduloIA.buscarUbicacion(i,ScrDic,listaCoorLetrasUbicadas):
							encontro=True
							sg.popup('encontro lugar')
							palabraUbi= i
							print(palabraUbi)
							break
				#--------------------------------------------------------------------------------------------------	
					
				if not encontro and sum(letras_total.values()) == 0:#<--- si la computadora no encontro lugar y no hay mas fichas,no puede seguir
					seguirC= False
				elif not encontro: #<---- si la computadora no encontro lugar y  hay mas fichas,cambia las fichas
					for i in fichasComp.keys():
						if fichasComp[i] in letras_total:
							letras_total[fichasComp[i]] = letras_total[fichasComp[i]] + 1
						else:
							letras_total[fichasComp[i]] = 1
					for i in fichasComp.keys():#<----pido nuevas fichas, y las pongo en el atril y en el diccionario fichasComp
						fichasComp[i]=fichas(letras_total)
						window[i].update(text= fichasComp[i])
				else:#<------ sino, encontro lugar y la ubica en la interfaz
				
					#-----------------------------------------------------------------------------------------------	 			
					multPal=0
					descuento=0
					puntPalabra=0			
					for j in range(len(listaCoorLetrasUbicadas)):
						window[listaCoorLetrasUbicadas[j]].update(ScrDic[listaCoorLetrasUbicadas[j]]['letra'],button_color=('black','white'))
						actual = ScrDic[listaCoorLetrasUbicadas[j]]
						if actual['letOpal'] == 'palabra':
							multPal= multPal + actual['puntajeC']
							puntPalabra = puntPalabra + puntJueg[actual['letra']]
						elif actual['letOpal'] == 'letra':
							puntPalabra = puntPalabra + (puntJueg[actual['letra']] * actual['puntajeC'] )
						elif actual['letOpal'] == 'descuenta':	
							descuento = descuento + actual['puntajeC']
							puntPalabra = puntPalabra + puntJueg[actual['letra']]
						else:
							puntPalabra = puntPalabra + puntJueg[actual['letra']]		
					#------------------------------------------------------------	
					sumaComp= puntPalabra - descuento
					if multPal != 0:
						sumaComp = sumaComp * multPal
					for i in range(len(palabraUbi)):#<----pido nuevas fichas para el atril de la computadora, y las pongo en el atril y en el diccionario botones
						#sumaComp = sumaComp + puntJueg[palabraUbi[i]]
						for j in range(7):
							
							if fichasComp[(100,j+1)] == palabraUbi[i]:
								fichasComp[(100,j+1)] = fichas(letras_total)
								print(fichasComp[(100,j+1)])#1
								window[(100,j+1)].update(text= fichasComp[(100,j+1)])
								break
					#--------------------------------------------------------------
					window[(20,20)].update(sum(letras_total.values()))#con esto puedo sumar para ver si el diccionario no tiene fichas
					totalComp = totalComp + sumaComp
					window[(40,40)].update(totalComp)
					#----activa evaluar y cambiar fichas
					window[(0,8)].update(disabled = False)
					window[(0,11)].update(disabled = False)	
					
					listaCoorLetrasUbicadas = []							
					#------------------------------------------------------------	
		#window['text'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,(current_time // 100) % 60,current_time % 100))
		window['text'].update('{:02d}:{:02d}'.format((current_time // 100) // 60,(current_time // 100) % 60))
if __name__ == '__main__':
	nivel='Facil'
	nombre='jorge'
	main(nivel)
