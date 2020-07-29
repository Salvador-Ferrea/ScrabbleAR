import PySimpleGUI as sg
import modulojugador1

def evaluarUbi(ubicacion):
	incorrecto=True
	if all(ubicacion[i][0]==ubicacion[i+1][0] for i in range(len(ubicacion)-1)):
		ubicacion = sorted(ubicacion, key=lambda tup: tup[1])
		if all(ubicacion[i][1]==ubicacion[i+1][1]-1 for i in range(len(ubicacion)-1)):
			incorrecto=False
			sg.popup('la palabra es horizontal')
		else:
			sg.popup('ubicacion incorrecta vuelva a intentarlo')
	elif all(ubicacion[i][1]==ubicacion[i+1][1] for i in range(len(ubicacion)-1)):
		ubicacion = sorted(ubicacion, key=lambda tup: tup[0])
		if all(ubicacion[i][0]==ubicacion[i+1][0]-1 for i in range(len(ubicacion)-1)):	
			incorrecto=False
			sg.popup('la palabra es vertical')
		else:
			sg.popup('ubicacion incorrecta vuelva a intentarlo')
	else:
		sg.popup('ubicacion incorrecta vuelva a intentarlo')
	return incorrecto

def devolverAtril(ubicacion,window,ScrDic,guardadoAtril,letras_total,seguirJ,botones):	
	for i in range(len(ubicacion)):
		window[ubicacion[i]].update(ScrDic[ubicacion[i]]['puntImp'], button_color = ScrDic[ubicacion[i]]['color'])	
	for i in guardadoAtril:
		window[i].update(text= botones[i])
	if sum(letras_total.values()) == 0:#<---- si no hay mas fichas en la bolsa
		seguirJ=False
	return seguirJ

def sumoPalabra(ubicacion,ScrDic,palabra,puntJueg,totalJug,window):									
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
	totalJug = totalJug + suma
	window[(30,30)].update(totalJug)
	return totalJug

def pidoFichasNuevas(guardadoAtril,botones,letras_total,window):				
	for i in guardadoAtril:#<----pido nuevas fichas, y las pongo en el atril y en el diccionario botones
		botones[i]=modulojugador1.fichas(letras_total)
		window[i].update(text= botones[i])
	window[(20,20)].update(sum(letras_total.values()))#con esto puedo sumar para ver si el diccionario no tiene fichas
			

