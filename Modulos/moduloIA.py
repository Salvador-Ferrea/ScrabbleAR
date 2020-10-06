import random

def funcVert(palabra,tablero,listaVacia):
	'''
		Aca busca la ubicacion en vertical, tiene una lista con el numero de filas, elije una fila random
		y empieza a buscar desde el inicio de esa fila la cantidad de lugares donde ubicar su palabra, cuenta
		la cantidad de lugares vacios y si llega a la cantidad correcta guarda la coordenada inicial en una lista
		y sigue buscando en esa fila si hay mas lugares. Al terminar esa fila si encontro lugares elije uno de esos
		lugares con random y coloca la palabra y retorna true. Si al terminar la fila no encontro lugar, elimina 
		de la lista que tiene el numero de filas, ese numero de fila y busca otra random y hace el mismo procedimiento.
		Si pasa por todas las filas y no encontro lugar retorna false. 
	'''
	filas=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
	encontro=False
	listPal=list(palabra)
	while ((not encontro) and (len(filas) != 0)):
		i=random.choice(filas)#elijo la fila para buscar
		suma=0#sumo las ubicaciones seguidas
		lugares=[]#guardo las coordenadas iniciales en donde puedo ubicar la palabra
		lugar= -1#guardo la posicion inicial actual, que todavia no se si sirve
		for j in range(1,16):
			if(tablero[(i,j)]['letra'] == '' and suma < len(listPal)):# <---lista con la palabra que hay que ubicar: si la posicion esta vacia y la suma es menor que el largo de la palabra,entro
				if(suma == 0):#si esta vacia, guardo la ubicacion en la variable lugar
					lugar= j
				suma= suma + 1
			elif(tablero[(i,j)]['letra'] != '' and suma < len(listPal)):# si la ubicacion no es vacia, borra la variable lugar y vuelvo suma a cero
				suma = 0
				lugar= -1 #borro la coordenada que puse en lugar
			else:#si no, encontro lugar y guarda la ubicacion en la lista lugares
				lugares.append(lugar)
				if tablero[(i,j)]['letra']== '':
					lugar = j
					suma= 1
				else:	
					suma = 0
		if len(lugares) != 0:# si la lista no esta vacia, ubico la palabra, cambio el boolean encontro a true
			x=i
			y= random.choice(lugares)
			print(listPal)#1
			for k in range(len(listPal)):#lista con la palabra
				listaVacia.append((x,y))
				tablero[(x,y)]['letra']=listPal[k]
				tablero[(x,y)]['colorLetraUbi']=('black','white')#<--- guardo el color de la letra ubicada para poder reestablecerla en la interfaz despues(en caso de querer guardar la partida)
				y = y + 1 	
			encontro = True
		else:#si no, elimino la fila i de la lista filas
			filas.remove(i)#elimino la posicion de la fila i de la lista filas
	return encontro	#retorno el boolean
					
def funcHor(palabra,tablero,listaVacia):
	'''
		Aca busca la ubicacion en horizontal, tiene una lista con el numero de columnas, elije una columna random
		y empieza a buscar desde el inicio de esa columna la cantidad de lugares donde ubicar su palabra, cuenta
		la cantidad de lugares vacios y si llega a la cantidad correcta guarda la coordenada inicial en una lista
		y sigue buscando en esa columna si hay mas lugares. Al terminar esa columna si encontro lugares elije uno de esos
		lugares con random y coloca la palabra y retorna true. Si al terminar la columna no encontro lugar, elimina 
		de la lista que tiene el numero de columnas, ese numero de columna y busca otra random y hace el mismo procedimiento.
		Si pasa por todas las columnas y no encontro lugar retorna false. 
	'''
	columnas=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
	encontro=False
	listPal=list(palabra)
	
	while ((not encontro) and (len(columnas) != 0)):
		j=random.choice(columnas)#elijo la fila para buscar
		suma=0#sumo las ubicaciones seguidas
		lugares=[]#guardo las coordenadas iniciales en donde puedo ubicar la palabra
		lugar= -1#guardo la posicion inicial actual, que todavia no se si sirve
		for i in range(1,16):
			if(tablero[(i,j)]['letra']== '' and suma < len(listPal)):# <---lista con la palabra que hay que ubicar: si la posicion esta vacia y la suma es menor que el largo de la palabra,entro
				if(suma == 0):#si esta vacia, guardo la ubicacion en la variable lugar
					lugar= i
				suma= suma + 1
			
			elif(tablero[(i,j)]['letra']!= '' and suma < len(listPal)):# si la ubicacion no es vacia, borra la variable lugar y vuelvo suma a cero
				suma = 0
				lugar= -1 #borro la coordenada que puse en lugar
			else:#si no, encontro lugar y guarda la ubicacion en la lista lugares
				lugares.append(lugar)
				if tablero[(i,j)]['letra']== '':
					lugar = i
					suma= 1
				else:	
					suma = 0
					
		if len(lugares) != 0:# si la lista no esta vacia, ubico la palabra, cambio el boolean encontro a true
			x= random.choice(lugares)
			y= j
			for k in range(len(listPal)):#lista con la palabra
				listaVacia.append((x,y))
				tablero[(x,y)]['letra']=listPal[k]
				tablero[(x,y)]['colorLetraUbi']=('black','white')#<--- guardo el color de la letra ubicada para poder reestablecerla en la interfaz despues(en caso de querer guardar la partida)
				x = x + 1 	
			encontro = True
		else:#si no, elimino la columna j de la lista columnas
			columnas.remove(j)#elimino la posicion de la columna j de la lista columnas
	return encontro	#retorno el boolean	
			
def buscarUbicacion(palabra,tablero,listaVacia):
	''' La computadora busca ubicacion en el tablero, si no esta ocupada el casillero del medio
		ubica ahi la primera letra y luego con random.shuffle selecciona si va vertical u horizontal.
		Si esta ocupado el casillero del medio,selecciona con random.shuffle si va vertical u horizontal 
		y llama a la funcion funcVert o funcHor segun lo que haya seleccionado.Si no encuentra ubicacion 
		en una de las dos, va a la otra a buscar ubicacion. Retorna un boolean para saber si encontro no lugar.
		utiliza una lista vacia para guardar las coordenadas donde ubico la palabra en el diccionario del tablero,
		ya que, a diferencia del turno del jugador , en el turno de la computadora primero ubica la palabra en el 
		diccionario y luego la ubica en la interfaz'''
		
	opciones=['vertical','horizontal']
	random.shuffle(opciones)
	encontro= False
	
	if tablero[(8,8)]['letra'] == '':
		encontro=True
		opcion1= opciones[0]
		if opcion1 == 'vertical':
			print(opcion1)
			listPal=list(palabra)	
			x = 8
			y = 8
			for k in range(len(listPal)):#lista con la palabra
				listaVacia.append((x,y))
				tablero[(x,y)]['letra']=listPal[k]
				tablero[(x,y)]['colorLetraUbi']=('black','white')#<--- guardo el color de la letra ubicada para poder reestablecerla en la interfaz despues(en caso de querer guardar la partida)
				x = x + 1 
		else:
			print(opcion1)
			listPal=list(palabra)	
			x = 8
			y = 8
			for k in range(len(listPal)):#lista con la palabra
				listaVacia.append((x,y))
				tablero[(x,y)]['letra']=listPal[k]
				tablero[(x,y)]['colorLetraUbi']=('black','white')#<--- guardo el color de la letra ubicada para poder reestablecerla en la interfaz despues(en caso de querer guardar la partida)
				y = y + 1
				 		
	else:
		
		opcion1= opciones[0]
		opcion2= opciones[1]

		if(opcion1 == 'vertical'):
			if funcVert(palabra,tablero,listaVacia)==False :# la lista guarda la ubicacion de las fichas a colocar en la interfaz
				if funcHor(palabra,tablero,listaVacia) == False:
					encontro=False
				else:
					encontro=True
			else:
				encontro = True			
	
		else:
			if funcHor(palabra,tablero,listaVacia) == False:	
				if funcVert(palabra,tablero,listaVacia)==False :
					encontro=False
				else:
					encontro=True
			else:
				encontro=True			
	return encontro
	
