ScrabbleAR - Trabajo Final

 Integrantes:
   
    Alacid, Francisco Javier (Legajo: 15151/6)
   
    Ferrea, Salvador (Legajo: 14986/0)
   
    Papurello, Diego (Legajo: 15302/2)

Requisitos:

- Sistema operativo Windows (7 o superior)
- Python 3.6.0 (Esta versión era la recomendada inicialmente por la cátedra)
- PySimpleGUI 4.20.0 (última versión a la fecha)
- Pattern 3.6 (última versión a la fecha)

Como instalar:

1.Descargar e instalar Python (https://www.python.org/downloads/release/python-360/), Bajar a la sección “Files” y descargar el instalador para la versión correspondiente de Windows.

2.Abrir el programa “Símbolo del sistema” o “Windows PowerShell” e ingresar “pip3 install PySimpleGUI” y esperar a que se instale la librería.

3.Después de que se haya instalado PySimpleGUI, ingresar “pip3 install pattern” y esperar a que se instale la librería.

Luego de completar los pasos anteriores, ya está listo para poder jugar ScrabbleAR.

Para comenzar, ejecute el archivo “ScrabbleAR.py” y se abrirá un menú. Para poder jugar, se debe ingresar un tiempo (en minutos) de juego y un nivel de juego.
El nivel de juego determina qué tipo de palabras (sustantivos, adjetivos y/o verbos) pueden ser jugadas y la cantidad de casilleros con descuento en el tablero.
Opcionalmente, se puede cambiar tanto el valor de las fichas, como la cantidad de estas con los botones “configuración de valor de fichas” y “configuración de cantidad de fichas” respectivamente.
Para poder hacerlo, se debe seleccionar de la lista "Letra" junto al boton "Modificar Letra", la letra que se desea modificar y el valor a asignarle se selecciona de la lista "Valor" junto a la lista "Letra".
Luego de configurar las fichas, para iniciar el juego se debe seleccionar el botón “juego nuevo” y dará inicio a la partida.

Para poder ingresar una palabra, se debe clickear una ficha, y luego seleccionar el espacio en el tablero (en caso de ser el primer turno, la primera ficha seleccionada será colocada automáticamente en el centro del tablero para facilitar el cumplimiento del reglamento).
Al terminar de ingresar la palabra, se debe presionar el botón “Evaluar”, luego, en caso de que la palabra sea incorrecta, se le informará al jugador de esto y se devolverán todas las fichas usadas al atril, y en caso de ser correcta, también se le informa al jugador, se asigna el puntaje correspondiente y se deberá presionar el botón “Pasar” para pasar el turno a la computadora. 
De esta forma, se juega hasta que se terminen las fichas, se acabe el tiempo o el jugador decida terminar la partida. Se dará la partida por acabada, se informa el resultado de la misma (si el jugador perdió o ganó) y se procederá a verificar si el puntaje es elegible para entrar en los diez mejores puntajes.

Para poder ver los “top ten” de cada categoría, en el menú principal se debe seleccionar de la lista “Elegir nivel de Top Ten:” el nivel deseado y luego seleccionar el botón “10 mejores puntajes”.