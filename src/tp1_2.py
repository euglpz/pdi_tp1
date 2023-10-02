import cv2
import numpy as np
import matplotlib.pyplot as plt

# Función para mostrar imágenes
def imshow(img, new_fig=True, title=None, color_img=False, blocking=False, colorbar=True, ticks=False):
    if new_fig:
        plt.figure()
    if color_img:
        plt.imshow(img)
    else:
        plt.imshow(img, cmap='gray')
    plt.title(title)
    if not ticks:
        plt.xticks([]), plt.yticks([])
    if colorbar:
        plt.colorbar()
    if new_fig:
        plt.show()

# Función para identificar las ROI del formulario:
def ident_rois(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Pasamos a escala de grises
    umbral, thresh_img = cv2.threshold(gray, thresh=124, maxval=255, type=cv2.THRESH_BINARY_INV)  # Umbralamos
    contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) # Identificamos los contornos

    rectangulos=[]

    for contorno in contours:
        perimetro = cv2.arcLength(contorno, True) # El perímetro se utiliza para definir parámetros de la aproximación del contorno
        aproximacion = cv2.approxPolyDP(contorno, 0.01 * perimetro, True) # Esta funcion devuelve los vertices de la aproximación
    
        # Si la aproximación tiene cuatro vértices, es un rectángulo
        if len(aproximacion) == 4:
            area = cv2.contourArea(aproximacion)
        
            # Algunas letras se reconocen como rectangulos. Usamos un umbral de área para no incluirlas en la lista de rectangulos.
            if (area > 50) & (area < 400000):
                rectangulos.append(aproximacion)


    indices_campos = [0,2,3,5,6,8,9,14,16,18,20]
    campos=[]

    for c in indices_campos:
        cv2.drawContours(thresh_img, rectangulos, c, (0, 255, 0), 2)
        campos.append(rectangulos[c])
    return campos

# Funcion para extraer una lista de las ROI:
def crop_rois(img,campos):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Pasamos a escala de grises
    umbral, thresh_img = cv2.threshold(gray, thresh=124, maxval=255, type=cv2.THRESH_BINARY_INV)  # Umbralamos
    rois=[]
    for i in campos:
        x1 = i[0][0][0]
        y1 = i[0][0][1]
        x2 = i[2][0][0]
        y2 = i[2][0][1]
        ancho = x2-x1
        alto = y2-y1    
        rois.append(thresh_img[y1+2:y1+alto-2, x1+2:x1+ancho-2])        
    return rois

# Funcion para mapear las ROI en un diccionario:
def map_rois(rois):
    dict_rois = {}
    dict_rois['Nombre'] = rois[10]
    dict_rois['Edad'] = rois[9]
    dict_rois['Mail'] = rois[8]
    dict_rois['Legajo'] = rois[7]
    dict_rois['P1_Si'] = rois[6]
    dict_rois['P1_No'] = rois[5]
    dict_rois['P2_Si'] = rois[4]
    dict_rois['P2_No'] = rois[3]
    dict_rois['P3_Si'] = rois[2]
    dict_rois['P3_No'] = rois[1]
    dict_rois['Coment'] = rois[0]
    return dict_rois

# Función para obtener un diccionario con las ROI del formulario:
def get_rois(img):
    '''
    Función para obtener un diccionario con las ROI del formulario:
    Claves: Nombre, Edad, Mail, Legajo, P1_Si, P1_No, P2_Si, P2_No, P3_Si, P3_No, Coment
    '''
    rois = crop_rois(img,ident_rois(img))
    dict_rois = map_rois(rois)
    return dict_rois

# Función para contar caracteres y palabras:
def cont_car_pal(roi):
    connectivity = 8
    tam_espacio = 8 # Tamaño de los espacios

    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(roi, connectivity, cv2.CV_32S)
    cant_caract = num_labels -1
    cant_palabras = 0
    espacios = []

    # Se ordenan elementos segun la posición sobre el eje x
    # El primer elemento es el campo del formulario. Los caracteres son los elementos del índice 1 en adelante.
    sort_index = np.argsort(stats[:, 0])
    stats = stats[sort_index]

    # Cálculo de espacios
    for i in range(len(stats)):
        if i > 1:
            espacios.append(stats[i][0]-(stats[i-1][0]+stats[i-1][2]))
    
    # Cantidad de palabras según umbral de espacio
    if espacios != []:
        cant_palabras = 1

    for i in espacios:
        if i > tam_espacio:
            cant_palabras+=1

    return cant_caract, cant_palabras, espacios

# Función para obtener las cantidades de cada ROI:
def get_cant(rois):
    # Salida: Diccionario: Clave = Campo; Valores = [0:cant. caracteres; 1:cant. palabras; 2:[espacios]]
    cant_dict = {}
    for k in rois.keys():
        cant_dict[k] = cont_car_pal(rois[k])
    return cant_dict

# Función de validación de campos de formularios: 
def valid_form(datos):
    '''
    Nombre y apellido: Debe contener al menos 2 palabras y no más de 25 caracteres en total.
    Edad: Debe contener 2 o 3 caracteres.
    Mail: Debe contener 1 palabra y no más de 25 caracteres.
    Legajo: 8 caracteres formando 1 sola palabra.
    Preguntas: se debe marcar con 1 caracter una de las dos celdas SI y NO. No pueden estar ambas vacías ni ambas completas.
    Comentarois: No debe contener más de 25 caracteres.

    datos[0]: caracteres
    datos[1]: palabras
    '''
    valid_dict = {}
    
    #Validar NOMBRE
    if (datos['Nombre'][0] <= 25) & (datos['Nombre'][1] >= 2):
        valid_dict['Nombre']='OK'
    else:
        valid_dict['Nombre']='MAL'

    #Validar EDAD
    if (datos['Edad'][0] >= 2) & (datos['Edad'][0] <= 3):
        valid_dict['Edad']='OK'
    else:
        valid_dict['Edad']='MAL'

    #Validar Mail
    if (datos['Mail'][0] <= 25) & (datos['Mail'][1] == 1):
        valid_dict['Mail']='OK'
    else:
        valid_dict['Mail']='MAL'

    #Validar Legajo
    if (datos['Legajo'][0] == 8) & (datos['Legajo'][1] == 1):
        valid_dict['Legajo']='OK'
    else:
        valid_dict['Legajo']='MAL'

    #Validar Pregunta 1
    if (datos['P1_Si'][0] + datos['P1_No'][0]) == 1:
        valid_dict['P1']='OK'
    else:
        valid_dict['P1']='MAL'

    #Validar Pregunta 2
    if (datos['P2_Si'][0] + datos['P2_No'][0]) == 1:
        valid_dict['P2']='OK'
    else:
        valid_dict['P2']='MAL'

    #Validar Pregunta 3
    if (datos['P3_Si'][0] + datos['P3_No'][0]) == 1:
        valid_dict['P3']='OK'
    else:
        valid_dict['P3']='MAL'

    #Validar Comentario
    if (datos['Coment'][0] <= 25):
        valid_dict['Coment']='OK'
    else:
        valid_dict['Coment']='MAL'

    return valid_dict

# Lectura de formularios
form0 = cv2.imread('formulario_vacio.png')
form1 = cv2.imread('formulario_01.png')
form2 = cv2.imread('formulario_02.png')
form3 = cv2.imread('formulario_03.png')
form4 = cv2.imread('formulario_04.png')
form5 = cv2.imread('formulario_05.png')

# Extracción de Regiones de Interés (ROI)
rois0 = get_rois(form0)
rois1 = get_rois(form1)
rois2 = get_rois(form2)
rois3 = get_rois(form3)
rois4 = get_rois(form4)
rois5 = get_rois(form5)

# Análisis de cantidades
datos0 = get_cant(rois0)
datos1 = get_cant(rois1)
datos2 = get_cant(rois2)
datos3 = get_cant(rois3)
datos4 = get_cant(rois4)
datos5 = get_cant(rois5)

# Validación de formularios
form0_status = valid_form(datos0)
form1_status = valid_form(datos1)
form2_status = valid_form(datos2)
form3_status = valid_form(datos3)
form4_status = valid_form(datos4)
form5_status = valid_form(datos5)

# Resultados
form0_status
form1_status
form2_status
form3_status
form4_status
form5_status