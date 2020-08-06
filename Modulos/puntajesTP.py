import PySimpleGUI as sg
import json

def temaNivel(nivel):
	if nivel =='Facil':
		sg.theme('DarkBlue10')
	elif nivel =='Medio':
		sg.theme('DarkGreen1')	
	else:
		sg.theme('DarkRed2')

					
def main(nivel, archivo):
	temaNivel(nivel)
	layout = [
            [sg.Text('Pos       ',font=('Helvetica', 30)), sg.Text('nombre',font=('Helvetica', 30)),sg.Text('          '), sg.Text('puntaje',font=('Helvetica', 30))],
            [sg.Listbox(values=[], size= (5,10),key='posicion',font=('Helvetica', 30)),sg.Listbox(values=[], size= (10,10),key='colores',font=('Helvetica', 30)),sg.Listbox(values=[], size= (10,10),key='valor',font=('Helvetica', 30))],
                 
         ]

	window = sg.Window(nivel, layout).Finalize()
	def mostrar_listado(listbox, lista):
		listbox.Update(map(lambda x: "{}".format(x), lista))
	
	pos=[1,2,3,4,5,6,7,8,9,10]
	
	jugad = sorted(archivo.items(), key = lambda jug: jug[1]['puntaje'],reverse = True)
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

