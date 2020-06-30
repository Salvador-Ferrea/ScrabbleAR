


#turno del robot:
import random

#uso clases para cada ubicacion del tablero,asi no es necesario dos tableros(horizontal/vertical)

def funcVert(palabra,tablero,listaVacia):
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
				y = y + 1 
			print(len(listaVacia))#2	
			encontro = True
		else:#si no, elimino la fila i de la lista filas
			filas.remove(i)#elimino la posicion de la fila i de la lista filas
	return encontro	#retorno el boolean
					
def funcHor(palabra,tablero,listaVacia):
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
			print(listPal)#3
			for k in range(len(listPal)):#lista con la palabra
				listaVacia.append((x,y))
				tablero[(x,y)]['letra']=listPal[k]
				x = x + 1 
			print(len(listaVacia))#4	
			encontro = True
		else:#si no, elimino la fila i de la lista filas
			filas.remove(j)#elimino la posicion de la fila i de la lista filas
	return encontro	#retorno el boolean	
			
def buscarUbicacion(palabra,tablero,listaVacia):
	
	opciones=['vertical','horizontal']
	random.shuffle(opciones)
	
	encontro= False

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
#---------------------------------------------------------------------	
