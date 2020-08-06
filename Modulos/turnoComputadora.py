import PySimpleGUI as sg
import itertools as it
import modulojugador1
import moduloIA


def buscarTablero(palabras_existentes,ScrDic):
	'''Con la lista de palabras existentes(las ordeno de mayor a menor) busco la ubicacion en el tablero,
		si no encuentro lugar busca  ubicar una palabra de menos letras '''
	palabras_existentes.sort(key=len,reverse=True)
	x = ''# lo uso como guia, en caso de que la palabra que envie no se pueda ubicar,si el largo de la palabra anterior es igual
		# al largo de la palabra actual, no busca ubicacion
	palabraUbi = ''	
	encontro= False
	listaCoorLetrasUbicadas = []
	for i in palabras_existentes:
		if len(x) != len(i):
			x = i
			if moduloIA.buscarUbicacion(i,ScrDic,listaCoorLetrasUbicadas):
				encontro=True
				sg.popup('encontro lugar')
				palabraUbi= i
				break
	return palabraUbi,encontro,listaCoorLetrasUbicadas
	
					
def cambiarFichas(fichasComp,consonantes,vocales,window):
	'''Cambia las fichas del atril de la computadora, si bien el Tp decia que la computadora no tiene que cambiar fichas 
		si no encuentra palabra, pusimos esta funcion porque si no en algunos niveles no se podia jugar'''	
	for i in fichasComp.keys():
		if i[1]== 2 or i[1]== 4:
			if fichasComp[i] in vocales:
				vocales[fichasComp[i]] = vocales[fichasComp[i]] + 1
			else:
				vocales[fichasComp[i]] = 1
		elif i[1] == 7:
			if fichasComp[i] == 'A' or fichasComp[i] == 'E' or fichasComp[i] == 'I' or fichasComp[i] == 'O' or fichasComp[i] == 'U': 
				if fichasComp[i] in vocales:
					vocales[fichasComp[i]] = vocales[fichasComp[i]] + 1
				else:
					vocales[fichasComp[i]] = 1
			else:
				if fichasComp[i] in consonantes:
					consonantes[fichasComp[i]] = consonantes[fichasComp[i]] + 1
				else:
					consonantes[fichasComp[i]] = 1	
		else:
			if fichasComp[i] in consonantes:
				consonantes[fichasComp[i]] = consonantes[fichasComp[i]] + 1
			else:
				consonantes[fichasComp[i]] = 1
				
	for i in fichasComp.keys():#<----pido nuevas fichas, y las pongo en el atril y en el diccionario fichasComp
		fichasComp[i]=modulojugador1.fichas(consonantes,vocales,i[1])
		
def sumarPuntaje(window,listaCoorLetrasUbicadas,ScrDic,puntJueg):		
		'''Coloca las fichas de la palabra de la computadora(que ya fueron puestas en el diccionario del tablero)en la interfaz y 
			suma el puntaje en el total de la computadora'''	 			
		multPal=0
		descuento=0
		puntPalabra=0			
		for j in range(len(listaCoorLetrasUbicadas)):
			window[listaCoorLetrasUbicadas[j]].update(ScrDic[listaCoorLetrasUbicadas[j]]['letra'],button_color=('black','white'),disabled_button_color=('black','white'),disabled=True)
			actual = ScrDic[listaCoorLetrasUbicadas[j]]
			if actual['letOpal'] == 'palabra':
				multPal= multPal + actual['puntajeC']
				puntPalabra = puntPalabra + puntJueg[actual['letra']]
			elif actual['letOpal'] == 'letra':
				puntPalabra = puntPalabra + (puntJueg[actual['letra']] * actual['puntajeC'] )
			elif actual['letOpal'] == 'descuenta':	
				descuento = descuento + actual['puntajeC']
				puntPalabra = puntPalabra + puntJueg[actual['letra']]
			else:
				puntPalabra = puntPalabra + puntJueg[actual['letra']]		
	
		sumaComp= puntPalabra - descuento
		
		if multPal != 0:
			sumaComp = sumaComp * multPal
		return sumaComp
		
def nuevasFichas(palabraUbi,fichasComp,window,consonantes,vocales):
	'''Pido nuevas fichas para el atril de la computadora(para las fichas que uso en la palabra que ubico),
		y las pongo en el atril y en el diccionario botones'''
	for i in range(len(palabraUbi)):
		for j in range(7):							
			if fichasComp[(100,j+1)] == palabraUbi[i]:
				fichasComp[(100,j+1)] = modulojugador1.fichas(consonantes,vocales,j+1)
				break

			
def turno(clasificacionAleatoria,fichasComp,nivel):
	'''Realiza las permutaciones con las letras del atril de la computadora
		y las coloca en palabras(set),luego recorre las permutaciones y 
		las evalua para ver cuales son correctas. Las correctas ingresan a 
		una lista llamada palabras_existentes'''
				
	letras=''.join(fichasComp.values())#<-- el string de la palabra
			
			
	palabras = set()#<---tiene las permutaciones
	for i in range(2,len(letras)+1):
		palabras.update((map("".join, it.permutations(letras,i))))
			
	palabras_existentes=[]#<--- guarda las palabras que armo y que existen
	for i in palabras:
				
		if modulojugador1.clasificar(''.join(i).lower(),nivel,clasificacionAleatoria):
			palabras_existentes.append(i)
			
	return palabras_existentes
			

