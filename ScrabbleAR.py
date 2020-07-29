import PySimpleGUI as sg
import modulojugador1
import os.path as path
import json
import puntajesTP
import configuracionScrabble

lista=[]
for i in range(1000):
	lista.append(i)
letras=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z']

def leerPartidasGuardadas():#<---leo el archivo de las partidas guardadas
	with open('partidasGuardadas.json', 'r') as archivo:
		datos = json.load(archivo)
	return datos

def main(args):
	layout = [[sg.Text('Scrabble:')],
		[sg.Text("Tiempo de juego:   "), sg.Combo(values=(20,40,60), key="tiempo")],
		[sg.Text("Nivel de juego:   "), sg.Combo(values=("Facil", "Medio", "Dificil"), key="niveles")],
		[sg.Text("Elegir nivel de Top Ten:   "), sg.Combo(values=("Facil", "Medio", "Dificil"), key="TopTen")],
		[sg.Button('juego nuevo')],
		[sg.Button('configuracion de valor de fichas')],
		[sg.Button('configuracion de cantidad de fichas')],
		[sg.Button('cargar partida')],
		[sg.Button('10 mejores puntajes')],
		[sg.Button('Exit')]]

	window = sg.Window('MenuScrabble').Layout(layout).Finalize()
	diccionarioV ={}
	diccionarioC ={}
	while True:
		event, values = window.Read()

		# sg.Print(event)
		# sg.Print(values)

		#window.FindElement()

		if event is None or event == 'Exit':      
			break
		elif event == 'juego nuevo':
			if window["niveles"].Get()!= '' and window["tiempo"].Get()!='':
				nivel= window["niveles"].Get()
				tiempo= window["tiempo"].Get()
				modulojugador1.main(nivel,tiempo,'nuevo',diccionarioC ,diccionarioV )
			else:
				sg.popup('no cargo nivel o tiempo')	
		elif event =='configuracion de valor de fichas':
			diccionarioV = configuracionScrabble.main('valor de fichas')
			print(diccionarioV)
		elif event =='configuracion de cantidad de fichas':
			diccionarioC = configuracionScrabble.main('cantidad de fichas')
			print(diccionarioC)	
		elif event == 'cargar partida':
			if path.exists('partidasGuardadas.json'):
				archGuardado = leerPartidasGuardadas()
				sg.popup('Resultado:  existe partida')
				modulojugador1.main(archGuardado['Nivel'],0,'viejo')
				
			else:
				sg.popup('Resultado: no hay partida guardada')		 		
		elif event == '10 mejores puntajes':
			nivelTopTen= window["TopTen"].Get()
			if nivelTopTen == '':
				sg.popup('no ingreso nivel del Top Ten')
			else:
				if nivelTopTen == 'Facil':
					if path.exists('archivoTopTen.json'):
						puntajesTP.main(nivelTopTen)
					else:
						sg.popup('no existe el top ten nivel facil')
				elif nivelTopTen == 'Medio':
					if path.exists('archivoTopTenMedio.json'):
						puntajesTP.main(nivelTopTen)
					else:
						sg.popup('no existe el top ten nivel medio')
				else:
					if path.exists('archivoTopTenDificil.json'):
						puntajesTP.main(nivelTopTen)
					else:
						sg.popup('no existe el top ten nivel dificil')			
					
if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))


