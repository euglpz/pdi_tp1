TUIA - Procesamiento de Imágenes I - TP1

En este proyecto se realizaron dos ejercicios:

1) Ecualización local de histograma

Se desarrolló una función para implementar la ecualización local del histograma,
que reciba como parámetros de entrada la imagen a procesar, y el tamaño de la
ventana de procesamiento (M x N).

Con esta función se analizó una imagen que conteniía detalles escondidos y de esta manera
se determina cuales son estos detalles escondidos en las diferentes zonas de la imagen.

---

2) Validación de formulario

Se tiene una serie de formularios completos, en formato de imagen, y se
pretende validar cada uno de ellos, corroborando que cada uno de sus campos cumpla
con las siguientes restricciones:
1. Nombre y apellido: Debe contener al menos 2 palabras y no más de 25
caracteres en total.
2. Edad: Debe contener 2 o 3 caracteres.
3. Mail: Debe contener 1 palabra y no más de 25 caracteres.
4. Legajo: 8 caracteres formando 1 sola palabra.
5. Preguntas: se debe marcar con 1 caracter una de las dos celdas SI y NO.
No pueden estar ambas vacías ni ambas completas.
6. Comentarios: No debe contener más de 25 caracteres.

Se desarrolló un algoritmo para validar los campos del formulario, tomando como entrada la imagen 
del mismo y se muestra por pantalla el estado de cada uno de sus campos. 
Por ejemplo:

Nombre y apellido: OK
Edad: OK
Mail: MAL
Legajo: MAL
Pregunta 1: OK
Pregunta 2: MAL
Pregunta 3: OK
Comentarios: OK

## Instrucciones para correr el proyecto:
1) Descargar el proyecto desde <> Code -> Download ZIP
2) Extraerlo en su PC (la carpeta se llamará *pdi_tp1-main*)
3) Abrir VS Code -> File -> Open Folder... (pdi_tp1-main)
4) Abrimos una nueva terminal
5) Creamos un venv: python -m venv venv
6) Lo activamos: .\venv\Scripts\activate
8) Y dentro de él instalamos los requerimientos: pip install -r .\requirements.txt
9) Nos movemos a la carpeta src: cd src
10) Corremos python: python
11) Y por último abrimos el ejercicio 1 (tp1_1.py) o el 2 (tp1_2.py)
