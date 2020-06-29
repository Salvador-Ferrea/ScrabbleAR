import PySimpleGUI as sg
import moduloJugador


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
			if window["niveles"].Get()!= '':
				moduloJugador.main(window["niveles"].Get())
			else:
				sg.popup('no cargo nivel')	
		elif event =='configuracion':
			print(window["niveles"].Get())
		elif event == 'cargar partida':
			print('o')	
		elif event == '10 mejores puntajes':
			print('a')	
if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))


