import PySimpleGUI as sg
from pattern.es import spelling,lexicon,parse

import moduloIA

import itertools as it

import random

sg.theme('DarkAmber')
color_button = ('white','blue')
tam_button = 5,2

#-----------------------------------------------------------------
# total de fichas:

#hago el diccionario
letras_total = {'A': 11,'B':3,'C':4,'D':4,'E':11,'F':2,'G':2,'H':2,
'I':6,'J':2,'K':1,'L':4,'LL':1,'M':3,'N':5,'Ñ':1,'O':8,'P':2,'Q':1,'R':4,
'RR':1,'S':7,'T':4,'U':6,'V':2,'W':1,'X':1,'Y':1,'Z':1}
#con esto puedo sumar para ver si el diccionario no tiene fichas

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
				
	
		

def main(nivel):
	print(nivel)
	naranja = [(1,1),(15,15),(1,15),(15,1),(1,8),(15,8),(8,1),(8,8),(8,15)]
	verde = [(1,4),(1,12),(15,4),(15,12),(3,7),(3,9),(13,7),(13,9),(4,1),(4,8),(4,15),(12,1),(12,8),(12,15),(7,3),(7,13),(9,3),(9,13),(8,4),(8,12)]
	azul = [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),(2,6),(2,10),(14,6),(14,10),(6,2),(6,14),(10,2),(10,14),(7,7),(7,9),(9,7),(9,9)]
	rojo = [(2,2),(3,3),(4,4),(5,5),(6,6),(10,10),(11,11),(12,12),(13,13),(14,14),(2,14),(3,13),(4,12),(5,11),(6,10),(10,6),(11,5),(12,4),(13,3),(14,2)]
	
	
	
	botones = {(0,1):fichas(letras_total),(0,2):fichas(letras_total),(0,3):fichas(letras_total),(0,4):fichas(letras_total),(0,5):fichas(letras_total),(0,6):fichas(letras_total),(0,7):fichas(letras_total)} 

	
	puntJueg = {'A':1,'B':3,'C':2,'D':2,'E':1,'F':4,'G':2,'H':4,'I':1,'J':6,'K':6,'L':1,'LL':8,'M':3,'N':1,'Ñ':8,'O':1,'P':3,'Q':8,'R':1,'RR':8,'S':1,'T':1,'U':1,'V':4,'W':8,'X':8,'Y':4,'Z':10}

	colIzq =  [[sg.Button(puntaje_casillero(i,j,nivel,naranja,verde,azul,rojo),button_color=calcular(i,j,naranja,verde,azul,rojo),size=(5, 2), key=(i,j), pad=(0,0)) for j in range(1,16)] for i in range(1,16)]
	colDer =[
			[sg.Text('Computadora:',size =(100,None),justification='left',text_color='yellow')],
			[sg.Button(fichas(letras_total),button_color=color_button,size=tam_button, key=(100,i+1))for i in range(7)],
			[sg.Text('______________________________________________________',text_color='red')],
			[sg.Text('puntaje Computadora:'),sg.Button(0, key=(40,40),button_color=('black','gray'),size=tam_button)],
			[sg.Text('')],
			[sg.Text('')],
			[sg.Text('')],
			[sg.Text('')],
			[sg.Text("Fichas restantes: "),sg.Button(sum(letras_total.values()), key=(20,20),button_color=('black','gray'),size=tam_button)],
			[sg.Text('Tiempo:')],
			[sg.Text('')],
			[sg.Text('')],
			[sg.Text(''),sg.Button('guardar partida', key=(50,50),button_color=('black','gray'),size=tam_button)],
			[sg.Text('')],
			[sg.Text('puntaje Jugador:'),sg.Button(0, key=(30,30),button_color=('black','gray'),size=tam_button)],
			[sg.Text('______________________________________________________',text_color='red')],
			[sg.Text('Jugador:',size =(100,None),justification='left',text_color='yellow')],
			[sg.Button(botones[(0,i+1)],button_color=color_button,size=tam_button, key=(0,i+1))for i in range(7)]]
	colDer.append([sg.Button('Evaluar', key=(0,8),button_color=('black','gray'),size=tam_button),sg.Button('Cambiar Fichas', key=(0,11),button_color=('black','gray'),size=(6,2)),sg.Button('Modificar', key=(0,9),button_color=('black','gray'),size=(6,2)),sg.Button('Pasar', key=(0,10),button_color=('black','gray'),size=tam_button)])

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
						
				ScrDic[(i,j)]={'color':("white", "orange"),'letra':'','puntajeC':puntajeCa,'letOpal':letraOpalabra}
        
			elif (i,j) in verde:
				x = window[(i,j)].GetText()
				if x == 'Lx2':
					puntajeCa = 2	
					letraOpalabra= 'letra'#<--- multiplica letra
				else:
					puntajeCa = 2	
					letraOpalabra= 'descuenta'
        
				ScrDic[(i,j)]={'color':("white", "green"),'letra':'','puntajeC':puntajeCa,'letOpal':letraOpalabra}
        
			elif (i,j) in azul:
				
				ScrDic[(i,j)]={'color':("white", "blue"),'letra':'','puntajeC':3,'letOpal':'letra'}
        
			elif (i,j) in rojo:
				x = window[(i,j)].GetText()
				if x == 'Px2':
					puntajeCa = 2	
					letraOpalabra= 'letra'
				else:
					puntajeCa = 1	
					letraOpalabra= 'descuenta'
        
				ScrDic[(i,j)]={'color':("white", "red"),'letra':'','puntajeC':puntajeCa,'letOpal':letraOpalabra}
        
			else:
        
				ScrDic[(i,j)]={'color':("white", "lightblue"),'letra':'','puntajeC':0,'letOpal':''}
            
	for i in range(1,8):

		ScrDic[(0,i)]=('white','blue')

	valor_A = ''

	valor_B = ''                   

	     
	
	guardado ={}#<--- guarda la ubicacion y la letra en donde se ubico la ficha en el tablero
	guardadoAtril = []#<---- guarda las coordenadas del atril del jugador: de las fichas que uso
	palabra = []#<----guarda las letras de la palabra
	ubicacion = []#<---guarda las coordenadas de donde se ubicaron las letras en el tablero
	totalJug=0#<--- puntaje total del jugador
	listaCoorLetrasUbicadas = []#<---- es la lista de las coordenadas donde la computadora ubico la palabra en el tablero
	fichasComp={}#<---guarda la ubicacion y la letra de las fichas del atril de la computadora
	totalComp =0#<------- puntaje total de la computadora
	
	while True:
		event, values = window.read()
		if event in (None, 'Exit'):
			break
		elif event != (0,8) and event != (0,9) and event != (0,10) and event != (0,11):#<--------si no es evaluar,modificar,pasar 
		
			if event in botones.keys():#<------entra si se apreto los botones del atril
			
				valor_A = window[event].GetText()#<----toma la letra del boton del atril 
				print(event)
				keys_entered = event#<--- guarda el event 
			
				event, values = window.read()
			
				if event in (None, 'Exit'):#<--------en caso de se haya apretado un boton del atril y se cierre
					break
			
				elif event not in botones.keys():#<-------si no es un boton del atril 
					valor_B = window[event].GetText()#<----toma la letra del segundo event
					if valor_B == '':
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
			
				
			else:#<------si se toca en el tablero, no hace nada
				print (event)
		elif event == (0,8):#<----apreto evaluar
		
		
			encontroX= False#
			encontroY= False#
			antX=ubicacion[0][0]#
			antY=ubicacion[0][1]#
			print(antX)
			print(antY)
			for i in range(len(ubicacion)):#
				
				if(antX == ubicacion[i][0]):#<-----verifico si la ubicacion es vertical,horizontal, o esta mal ubicada 
					encontroX=True#
				else:#
					encontroX=False#			
				if(antY == ubicacion[i][1]):#
					encontroY=True#
				else:#
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
					window[ubicacion[i]].update('', button_color = ScrDic[ubicacion[i]]['color'])	
				
				
				guardado={}
				guardadoAtril=[]
				ubicacion=[]
			
			else:
			
				for i in ubicacion:#<---- utilizo las ubicaciones ordenadas, para sacar la palabra 
					palabra.append(guardado[i])
			
				strPal=''.join(palabra).lower()#<-----transformo la lista en string
				if strPal in spelling.keys() or strPal in lexicon.keys():#<-----evaluo la palabra, si es correcta ubica la palabra
					sg.popup('se ubico la palabra')
					suma=0
					for i in range(len(ubicacion)):
						ScrDic[ubicacion[i]]['letra']=palabra[i]#<----guardo la letra en el diccionario del tablero(para el turno de la computadora) 
						suma = suma + puntJueg[palabra[i]]#<-----sumo el puntaje de la palabra
					for i in guardadoAtril:#<----pido nuevas fichas, y las pongo en el atril y en el diccionario botones
						botones[i]=fichas(letras_total)
						window[i].update(text= botones[i])
					window[(20,20)].update(sum(letras_total.values()))#con esto puedo sumar para ver si el diccionario no tiene fichas
					totalJug = totalJug + suma
					window[(30,30)].update(totalJug)
					ubicacion = []
					palabra = []
					guardadoAtril=[]
					guardado={}
				else:#<--- si es incorrecta la palabra,vuelve las fichas al lugar
					sg.popup('la palabra no es correcta,vuelva a intentarlo')
					for i in range(len(ubicacion)):
						window[ubicacion[i]].update('', button_color = ScrDic[ubicacion[i]]['color'])	
					#ubicacion = []
					for i in guardadoAtril:
						window[i].update(text= botones[i])
					guardado={}
					guardadoAtril=[]
					ubicacion=[]
					palabra=[]
					
		elif event == (0,9):
			#devolver la fichas al atril,en caso de que te hayas equivocado antes de evaluar la palabra
			for i in range(len(ubicacion)):
				window[ubicacion[i]].update('', button_color = ScrDic[ubicacion[i]]['color'])	
				
			for i in guardadoAtril:
				window[i].update(text= botones[i])
			guardado={}
			guardadoAtril=[]
			ubicacion=[]
		elif event == (0,11):#<----cambio las fichas
			for i in botones.keys():
				if botones[i] in letras_total:
					letras_total[botones[i]] = letras_total[botones[i]] + 1
				else:
					letras_total[botones[i]] = 1
			for i in botones.keys():#<----pido nuevas fichas, y las pongo en el atril y en el diccionario botones
				botones[i]=fichas(letras_total)
				window[i].update(text= botones[i])	
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

			#-----------------------------------------------------------
			#Con la lista de palabras existentes(las ordeno de mayor a menor) busco la ubicacion en el tablero
			palabras_existentes.sort(key=len,reverse=True)
			x = ''# lo uso como guia, en caso de que la palabra que envie no se pueda ubicar,si el largo de la palabra anterior es igual
				# al largo de la palabra actual, no busca ubicacion
			palabraUbi = ''	
			for i in palabras_existentes:
				if len(x) != len(i):
					x = i
					if moduloIA.buscarUbicacion(i,ScrDic,listaCoorLetrasUbicadas):
						sg.popup('encontro lugar')
						palabraUbi= i
						print(palabraUbi)
						break
					
						
			for j in range(len(listaCoorLetrasUbicadas)):
				window[listaCoorLetrasUbicadas[j]].update(ScrDic[listaCoorLetrasUbicadas[j]]['letra'],button_color=('black','white'))
			#------------------------------------------------------------	
			sumaComp=0
			for i in range(len(palabraUbi)):#<----pido nuevas fichas para el atril de la computadora, y las pongo en el atril y en el diccionario botones
				sumaComp = sumaComp + puntJueg[palabraUbi[i]]
				for j in range(7):
				
					if fichasComp[(100,j+1)] == palabraUbi[i]:
						fichasComp[(100,j+1)] = fichas(letras_total)
						window[(100,j+1)].update(text= fichasComp[(100,j+1)])
			#--------------------------------------------------------------
			window[(20,20)].update(sum(letras_total.values()))#con esto puedo sumar para ver si el diccionario no tiene fichas
			totalComp = totalComp + sumaComp
			window[(40,40)].update(totalComp)
						
			listaCoorLetrasUbicadas = []							
			#------------------------------------------------------------	
		
	
if __name__ == '__main__':
	nivel='Facil'
	main(nivel)
