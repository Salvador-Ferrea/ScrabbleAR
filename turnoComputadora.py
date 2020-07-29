import PySimpleGUI as sg
import itertools as it
import modulojugador1
import moduloIA
#turno computadora

def buscarTablero(palabras_existentes,ScrDic):
	#Con la lista de palabras existentes(las ordeno de mayor a menor) busco la ubicacion en el tablero
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
				print(palabraUbi)
				break
	return palabraUbi,encontro,listaCoorLetrasUbicadas
	#--------------------------------------------------------------------------------------------------	
					
def cambiarFichas(fichasComp,letras_total,window):	
	for i in fichasComp.keys():
		if fichasComp[i] in letras_total:
			letras_total[fichasComp[i]] = letras_total[fichasComp[i]] + 1
		else:
			letras_total[fichasComp[i]] = 1
	for i in fichasComp.keys():#<----pido nuevas fichas, y las pongo en el atril y en el diccionario fichasComp
		fichasComp[i]=modulojugador1.fichas(letras_total)
		
def sumarPuntaje(window,listaCoorLetrasUbicadas,ScrDic,puntJueg):		
		#-----------------------------------------------------------------------------------------------	 			
		multPal=0
		descuento=0
		puntPalabra=0			
		for j in range(len(listaCoorLetrasUbicadas)):
			window[listaCoorLetrasUbicadas[j]].update(ScrDic[listaCoorLetrasUbicadas[j]]['letra'],button_color=('black','white'))
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
		#------------------------------------------------------------	
		sumaComp= puntPalabra - descuento
		
		if multPal != 0:
			sumaComp = sumaComp * multPal
		return sumaComp
		
def nuevasFichas(palabraUbi,fichasComp,window,letras_total):
	for i in range(len(palabraUbi)):#<----pido nuevas fichas para el atril de la computadora, y las pongo en el atril y en el diccionario botones
		for j in range(7):							
			if fichasComp[(100,j+1)] == palabraUbi[i]:
				fichasComp[(100,j+1)] = modulojugador1.fichas(letras_total)
				break
	#--------------------------------------------------------------
			
def turno(clasificacionAleatoria,fichasComp,nivel):
				
	letras=''.join(fichasComp.values())#<-- el string de la palabra
			
			
	palabras = set()#<---tiene las permutaciones
	for i in range(2,len(letras)+1):
		palabras.update((map("".join, it.permutations(letras,i))))
			
	palabras_existentes=[]#<--- guarda las palabras que armo y que existen
	for i in palabras:
				
		if modulojugador1.clasificar(''.join(i).lower(),nivel,clasificacionAleatoria):
			palabras_existentes.append(i)
			
	return palabras_existentes
			
	#-----------------------------------------------------------------------
