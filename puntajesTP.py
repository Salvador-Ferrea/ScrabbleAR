import PySimpleGUI as sg
import json
def leerPartidasGuardadas(nivel):#<---leo el archivo de las partidas guardadas
	if nivel == 'Facil':
		with open('archivoTopTen.json', 'r') as archivo:
			datos = json.load(archivo)
		return datos
	elif nivel == 'Medio':
		with open('archivoTopTenMedio.json', 'r') as archivo:
			datos = json.load(archivo)
		return datos
	else:
		with open('archivoTopTenDificil.json', 'r') as archivo:
			datos = json.load(archivo)
		return datos
		
def main(nivel):
	layout = [
            [sg.Text('Pos       '), sg.Text('nombre'),sg.Text('          '), sg.Text('puntaje')],
            [sg.Listbox(values=[], size= (5,10),key='posicion'),sg.Listbox(values=[], size= (10,10),key='colores'),sg.Listbox(values=[], size= (10,10),key='valor')],
                 
         ]

	window = sg.Window(nivel, layout).Finalize()
	def mostrar_listado(listbox, lista):
		listbox.Update(map(lambda x: "{}".format(x), lista))
	
	pos=[1,2,3,4,5,6,7,8,9,10]
	jugTopTen= leerPartidasGuardadas(nivel)
	jugad = sorted(jugTopTen.items(), key = lambda jug: jug[1]['puntaje'],reverse = True)
	listaNom=[]
	puntaje=[]
	for i in jugad:
		listaNom.append(i[1]['nombre'])
		puntaje.append(i[1]['puntaje'])
	mostrar_listado( window.FindElement('colores'), listaNom)
	mostrar_listado( window.FindElement('posicion'), pos)
	mostrar_listado( window.FindElement('valor'),puntaje)
	while True:
		event, values = window.Read()
		if event in (None, 'Exit'):
			break
	
		
if __name__ == '__main__':
	main('Facil')

