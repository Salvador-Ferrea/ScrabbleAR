import sys
sys.path.insert(0, 'Modulos')
import PySimpleGUI as sg
import modulojugador1
import os.path as path
import json
import puntajesTP
import configuracionScrabble

sg.theme('DarkAmber')

def calcular(i,j,naranja,verde,azul,rojo):
	''' Toma los colores de los casilleros del minitablero'''
	if(i,j) in naranja:			
		return ("white", "orange")        
	elif(i,j) in verde: 			
		return ("white", "green")               
	elif (i,j) in azul:        
		return("white", "blue")        
	elif (i,j) in rojo:                   			
		return ("white", "red") 
	elif i==0 or j==0 or i==16 or j==16:
		return("white", "brown") 	        
	else:
		return ("white", "lightblue")

def puntaje_casillero(i,j,naranja,verde,azul,rojo):
	''' Toma los valores de los casilleros para el minitablero'''	
	if(i,j) in naranja:				       
		return 'Px3'		 			
	elif(i,j) in verde:	       
		return 'Lx2'			        
	elif (i,j) in azul:        
		return 'Lx3'        
	elif (i,j) in rojo:          
		return 'Px2'			
	else:
		return''	
def leerPartidasTopTen(nivel):#<---leo el archivo de las partidas guardadas
	'''Lee el archivo del top ten segun el nivel'''
	if nivel == 'Facil':
		with open('Archivos/archivoTopTen.json', 'r') as archivo:
			datos = json.load(archivo)
		return datos
	elif nivel == 'Medio':
		with open('Archivos/archivoTopTenMedio.json', 'r') as archivo:
			datos = json.load(archivo)
		return datos
	else:
		with open('Archivos/archivoTopTenDificil.json', 'r') as archivo:
			datos = json.load(archivo)
		return datos

def leerPartidasGuardadas():#<---leo el archivo de las partidas guardadas
	'''Lee el archivo partidasGuardadas.json'''
	with open('Archivos/partidasGuardadas.json', 'r') as archivo:
		datos = json.load(archivo)
	return datos
naranja = [(1,1),(15,15),(1,15),(15,1),(1,8),(15,8),(8,1),(8,8),(8,15)]
verde = [(1,4),(1,12),(15,4),(15,12),(3,7),(3,9),(13,7),(13,9),(4,1),(4,8),(4,15),(12,1),(12,8),(12,15),(7,3),(7,13),(9,3),(9,13),(8,4),(8,12)]
azul = [(2,6),(2,10),(14,6),(14,10),(6,2),(6,14),(10,2),(10,14),(7,7),(7,9),(9,7),(9,9)]
rojo = [(2,2),(3,3),(4,4),(5,5),(6,6),(10,10),(11,11),(12,12),(13,13),(14,14),(2,14),(3,13),(4,12),(5,11),(6,10),(10,6),(11,5),(12,4),(13,3),(14,2)]

def main(args):
	lista=[]
	for i in range(1,61):
		lista.append(i)
	colIzq1=[[sg.Text('')]]
	colIzq =[[sg.Button(puntaje_casillero(i,j,naranja,verde,azul,rojo),button_color=calcular(i,j,naranja,verde,azul,rojo),disabled_button_color=calcular(i,j,naranja,verde,azul,rojo),size=(3, 1), key=(i,j),disabled=True, pad=(0,0)) for j in range(0,17)] for i in range(0,17)]
	
	colIzq.append([sg.Text('',size=(20,1),justification="left",font=('Arial', 40))])
	colIzq.append([sg.Text('ScrabbleAr',size=(20,1),justification="left",font=('Arial', 70))])

	colDer = [
		[sg.Text('Menu:',font=('Helvetica', 40))],
		[sg.Text('',font=('Helvetica', 40))],
		[sg.Text("Tiempo de juego:   ",font=('Helvetica', 15)), sg.Combo(values=lista,size=(3,2), key="tiempo",font=('Helvetica', 15))],
		[sg.Text("Nivel de juego:   ",font=('Helvetica', 15)), sg.Combo(values=("Facil", "Medio", "Dificil"), key="niveles",font=('Helvetica', 15))],
		[sg.Text("Elegir nivel de Top Ten:   ",font=('Helvetica', 15)), sg.Combo(values=("Facil", "Medio", "Dificil"), key="TopTen",font=('Helvetica', 15))],
		[sg.Text('',font=('Helvetica', 40))],
		[sg.Button('juego nuevo',font=('Helvetica', 15))],
		[sg.Button('configuracion de valor de fichas',font=('Helvetica', 15))],
		[sg.Button('configuracion de cantidad de fichas',font=('Helvetica',15))],
		[sg.Button('cargar partida',font=('Helvetica', 15))],
		[sg.Button('10 mejores puntajes',font=('Helvetica', 15))],
		[sg.Button('Exit',font=('Helvetica', 15))]]
	layout = [[sg.Column(colIzq1,size=(100,10)),sg.Column(colIzq,size=(650,650)),sg.Column(colDer,size=(700,700))]]
	window = sg.Window('MenuScrabble').Layout(layout).Finalize()
	window.Maximize()
	diccionarioVguardado ={}
	diccionarioCguardado ={}
	diccionarioV ={}
	diccionarioC ={}
	while True:
		event, values = window.Read()
		if event is None or event == 'Exit':      
			break
		elif event == 'juego nuevo':
			if window["niveles"].Get()!= '' and window["tiempo"].Get()!='':
				nivel= window["niveles"].Get()
				tiempo= window["tiempo"].Get()
				
				if len(diccionarioV)== 0:
					diccionarioV = configuracionScrabble.valorPred()
				if len(diccionarioC) == 0:
					diccionarioC = configuracionScrabble.cantidadPred()	
				
				diccionarioVguardado = diccionarioV.copy()
				diccionarioCguardado=diccionarioC.copy()
				modulojugador1.main(nivel,tiempo,'nuevo',diccionarioC ,diccionarioV )
				diccionarioC= diccionarioCguardado
				diccionarioV= diccionarioVguardado
			else:
				sg.popup('no cargo nivel o tiempo')	
		elif event =='configuracion de valor de fichas':
			sg.theme('DarkAmber')
			diccionarioV=configuracionScrabble.main('valor de fichas')					
		elif event =='configuracion de cantidad de fichas':
			sg.theme('DarkAmber')
			diccionarioC=configuracionScrabble.main('cantidad de fichas')
		elif event == 'cargar partida':
			try:
				archGuardado = leerPartidasGuardadas()
				sg.popup('Resultado:  existe partida')			
				modulojugador1.main(archGuardado['Nivel'],0,'viejo',diccionarioC,diccionarioV,archGuardado)				
			except:
				sg.popup('Resultado: no hay partida guardada')		 		
		elif event == '10 mejores puntajes':
			nivelTopTen= window["TopTen"].Get()
			if nivelTopTen == '':
				sg.popup('no ingreso nivel del Top Ten')		
			else:				
				try:							
					archTopTen = leerPartidasTopTen(nivelTopTen)
					puntajesTP.main(nivelTopTen,archTopTen)
					
				except:
					sg.popup('no existe el top ten ')		
					
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))


