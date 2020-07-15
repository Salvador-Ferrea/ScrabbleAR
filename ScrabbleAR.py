import PySimpleGUI as sg
import moduloJugador
import os.path as path
import json
def leerPartidasGuardadas():#<---leo el archivo de las partidas guardadas
	with open('partidasGuardadas.json', 'r') as archivo:
		datos = json.load(archivo)
	return datos

def main(args):
	layout = [
		[sg.Text('Scrabble')],
		[sg.Text("Tiempo de juego:   "), sg.Combo(values=(20,40,60), key="tiempo")],
		[sg.Text("Nivel de juego:   "), sg.Combo(values=("Facil", "Medio", "Dificil"), key="niveles")],
		[sg.Button('juego nuevo')],
		[sg.Button('configuracion')],
		[sg.Button('cargar partida')],
		[sg.Button('10 mejores puntajes')],
		[ sg.Exit()]
	]

	window = sg.Window('MenuScrabble').Layout(layout).Finalize()

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
				moduloJugador.main(nivel,tiempo)
			else:
				sg.popup('no cargo nivel o tiempo')	
		elif event =='configuracion':
			print(window["niveles"].Get())
		elif event == 'cargar partida':
			nombre = sg.popup_get_text('ingrese nombre guardado', '')
			if path.exists('partidasGuardadas.json'):
				archGuardado=leerPartidasGuardadas()
				try:
					if archGuardado[nombre]:
						sg.popup('Resultado:  existe partida con el nombre', nombre)
						moduloJugador.main('',0,nombre)
				except:
					sg.popup('Resultado: no existe partida con el nombre', nombre)
			else:
				sg.popup('Resultado: el archivo de partidas esta vacio')		 		
		elif event == '10 mejores puntajes':
			print('a')	
if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))


