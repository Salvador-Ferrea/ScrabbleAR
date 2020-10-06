import PySimpleGUI as sg

def cantidadPred():
	''' Es la cantidad Predeterminada de fichas.En caso de no configurar toma estos valores'''
	x = {'A': 11,'B':3,'C':4,'D':4,'E':11,'F':2,'G':2,'H':2,
			'I':6,'J':2,'K':1,'L':4,'M':3,'N':5,'Ñ':1,'O':8,'P':2,'Q':1,'R':4,
			'S':7,'T':4,'U':6,'V':2,'W':1,'X':1,'Y':1,'Z':1}
	return x
	
def valorPred():
	''' Son los valores Predeterminados de fichas.En caso de no configurar toma estos valores'''	
	x = {'A':1,'B':3,'C':2,'D':2,'E':1,'F':4,'G':2,'H':4,'I':1,'J':6,'K':6,
			'L':1,'M':3,'N':1,'Ñ':8,'O':1,'P':3,'Q':8,'R':1,'S':1,
			'T':1,'U':1,'V':4,'W':8,'X':8,'Y':4,'Z':10}
	return x
	
def activar(window,*args):
	'''Activa el disabled de todas las coordenadas que se pasan por parametro'''
	for i in args:
		window[i].update(disabled = True)
		
def desactivar(window,*args):
	'''Desactiva el disabled de todas las coordenadas que se pasan por parametro'''
	for i in args:
		window[i].update(disabled = False)
	
def main(configuracion,dicFichas):
	lista=[]
	for i in range(1,200):
		lista.append(i)
	letras=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','Ñ','O','P','Q','R','S','T','U','V','W','X','Y','Z']
	col1 =  [[sg.Text(letras[i]+':',font=('Helvetica', 20) ) for j in range(1)] for i in range(0,9)]
	col2 = [[sg.In(0, key=letras[i],size=(4,2),font=('Helvetica', 20),disabled = True)for j in range(1)] for i in range(0,9)]
	col3 =  [[sg.Text(letras[i]+':',font=('Helvetica', 20) ) for j in range(1)] for i in range(9,18)]
	col4 = [[sg.In(0, key=letras[i],size=(4,2),font=('Helvetica', 20),disabled = True)for j in range(1)] for i in range(9,18)]
	col5 =  [[sg.Text(letras[i]+':',font=('Helvetica', 20) ) for j in range(1)] for i in range(18,27)]
	col6 = [[sg.In(0, key=letras[i],size=(4,2),font=('Helvetica', 20),disabled = True)for j in range(1)] for i in range(18,27)]
	
	layout =[ 
			[sg.Text(configuracion,font=('Helvetica', 15))],
			[sg.Column(col1,size=(100,450)),sg.Column(col2,size=(100,450)),sg.Column(col3,size=(100,450)),sg.Column(col4,size=(100,450)),sg.Column(col5,size=(100,450)),sg.Column(col6,size=(100,450))],
			[sg.Text('Total:',font=('Helvetica', 15)),sg.In(0, key='total',size=(4,2),font=('Helvetica', 15),disabled = True)],
			[sg.Button('Modificar Letra',font=('Helvetica', 15)),sg.Text('Letra:',font=('Helvetica', 15)), sg.Combo(values=letras, key='letra',font=('Helvetica', 15),size=(3,2),readonly=True),sg.Text('Valor:',font=('Helvetica', 15)), sg.Combo(values=lista, key='Valor',font=('Helvetica', 15),readonly=True)],
			[sg.Button('Ejecutar',font=('Helvetica', 15)),sg.Button('Devolver Valores Predeterminados',font=('Helvetica', 15))]
			]
	window = sg.Window('MenuScrabble').Layout(layout).Finalize()
	
	if configuracion == 'cantidad de fichas':
		
		x = dicFichas['cantidad']
		for i in x.keys():
			window[i].update(x[i])
		window['total'].update(sum(x.values()))
	else:
		x = dicFichas['valor']
		for i in x.keys():
			window[i].update(x[i])
		window['total'].update(sum(x.values()))	
	while True:
		event, values = window.Read()		
		if event in (None, 'Exit'):
			break
		if event == 'Modificar Letra':
			let=window['letra'].Get()
			val=window['Valor'].Get()
			if let == '' or val == '':
				sg.popup('no ingreso letra o palabra')
			else:
				window[let].update(val)
				x[let]=val
				window['total'].update(sum(x.values()))
				
				if configuracion == 'cantidad de fichas':
					suma = int(window['total'].Get())	
					if suma > 225:	
						sg.popup('se paso del limite')
						window['Ejecutar'].update(disabled = True)
					else:
						window['Ejecutar'].update(disabled = False)
					
			
		elif event == 'Devolver Valores Predeterminados':
			if configuracion == 'cantidad de fichas':
				x=cantidadPred()

			else:
				x= valorPred()
			for i in x.keys():
				window[i].update(x[i])
			window['total'].update(sum(x.values()))		
		
			break
			
		elif event ==  'Ejecutar':
	
			break
		
		
	window.close()		
	return x					
if __name__ == '__main__':
	dicFichas={}
	dicFichas['cantidad']=cantidadPred()
	dicFichas['valor']= valorPred()
	main('cantidad de fichas',dicFichas)
