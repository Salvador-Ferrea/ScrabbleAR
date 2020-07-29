import PySimpleGUI as sg

def main(configuracion):
	lista=[]
	for i in range(1000):
		lista.append(i)
	letras=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	col1 =  [[sg.Text(letras[i]+':' ) for j in range(1)] for i in range(0,9)]
	col2 = [[sg.Combo(values=lista, key=letras[i])for j in range(1)] for i in range(0,9)]
	col3 =  [[sg.Text(letras[i]+':' ) for j in range(1)] for i in range(9,18)]
	col4 = [[sg.Combo(values=lista, key=letras[i])for j in range(1)] for i in range(9,18)]
	col5 =  [[sg.Text(letras[i]+':' ) for j in range(1)] for i in range(18,27)]
	col6 = [[sg.Combo(values=lista, key=letras[i])for j in range(1)] for i in range(18,27)]
	
	layout =[ 
			[sg.Text(configuracion)],
			[sg.Column(col1,size=(50,250)),sg.Column(col2,size=(50,250)),sg.Column(col3,size=(50,250)),sg.Column(col4,size=(50,250)),sg.Column(col5,size=(50,250)),sg.Column(col6,size=(50,250))],
			[sg.Button('Ejecutar')]
			]
	window = sg.Window('MenuScrabble').Layout(layout).Finalize()

	while True:
		event, values = window.Read()
		if event in (None, 'Exit'):
			break
		if event == 'Ejecutar':
			diccionario={}
			if configuracion == 'cantidad de fichas':
				suma=0
				
				for i in letras:
					cantidad = window[i].Get()
					if cantidad != '' and cantidad != 0:
						suma= suma + cantidad
						diccionario[i] = cantidad
				if suma	> 225:	
					sg.popup('se paso del limite')
					diccionario={}	
			elif configuracion == 'valor de fichas':
				for i in letras:
					valor = window[i].Get()
					if valor != '':
						diccionario[i] = valor			
					else:	
						diccionario[i] = 1
			return diccionario
			break
	window.close()		
						
if __name__ == '__main__':
	main('configuracion de cantidad de letras:')
