import cv2
import numpy as np
import matplotlib.pyplot as plt

# Función para implementar la ecualización local del histograma
def local_heq(img, window_size):
    # Obtenemos dimensiones de la imágen
    height, width = img.shape
    
    # Calculamos la mitad del tamaño de la ventana en ambas dimensiones
    half_height = window_size[0] // 2
    half_width = window_size[1] // 2
    
    # Creamos una copia de la imágen original para almacenar el resultado
    result_img = img.copy()
    
    # Agregamos un borde a la imágen para manejar los píxeles en el borde de manera adecuada
    border_type = cv2.BORDER_REPLICATE  # BORDER_REFLECT_101
    image_with_border = cv2.copyMakeBorder(img, half_height, half_height, half_width, half_width, border_type)
    
    # Recorremos la imágen pixel a pixel
    for y in range(half_height, height + half_height): # cols
        for x in range(half_width, width + half_width): # rows

            # Obtenemos la región de la ventana
            window = image_with_border[y - half_height:y + half_height + 1, x - half_width:x + half_width + 1]
            
            # Calculamos histograma de la ventana
            hist = cv2.calcHist([window], [0], None, [256], [0, 256])
            
            # Calculamos la función de distribución acumulativa del histograma
            cdf = hist.cumsum()

            # La normalizamos (cdf[-1] es el recuento total de px de la img)
            cdfn = cdf / cdf[-1]
            
            # Realizamos la ecualización del histograma local
            result_pixel_value = int(cdfn[window[window_size[0] // 2, window_size[1] // 2]] * 255)

            # Asignamos el valor resultante al píxel correspondiente en la imagen de resultado
            result_img[y - half_height, x - half_width] = result_pixel_value
    
    return result_img

img = cv2.imread('Imagen_con_detalles_escondidos.tif', cv2.IMREAD_GRAYSCALE)


ventana_tamano3x3 = (3, 3)  
img_ecualizada3x3 = local_heq(img, ventana_tamano3x3)

ventana_tamano5x5 = (5, 5)
img_ecualizada5x5 = local_heq(img, ventana_tamano5x5)

ventana_tamano11x11 = (11, 11)  
img_ecualizada11x11 = local_heq(img, ventana_tamano11x11)

# Gráfico imágen original con su histograma
plt.subplot(121)
plt.imshow(img,cmap='gray')
plt.title('Imagen Original')
plt.subplot(122)
plt.hist(img.flatten(), 256, [0, 256])
plt.title('Histograma')
plt.show(block=False)

# Gráficos imágenes ecualizadas
plt.figure()
ax = plt.subplot(221)
plt.imshow(img_ecualizada3x3,cmap='gray',vmin=0,vmax=255), plt.title('Imagen Ecualizada Ventana 3x3')
plt.subplot(223,sharex=ax,sharey=ax), plt.imshow(img_ecualizada5x5,cmap='gray',vmin=0,vmax=255), plt.title('Imagen Ecualizada Ventana 5x5')
plt.subplot(224,sharex=ax,sharey=ax), plt.imshow(img_ecualizada11x11,cmap='gray',vmin=0,vmax=255), plt.title('Imagen Ecualizada Ventana 11x11')
plt.show(block=False)

# Gráficos imágenes ecualizadas con sus histogramas
plt.figure()
ax1 = plt.subplot(321)
plt.imshow(img_ecualizada3x3,cmap='gray',vmin=0,vmax=255), plt.title('Imagen Ecualizada Ventana 3x3')
plt.subplot(322), plt.hist(img_ecualizada3x3.flatten(), 256, [0, 256]), plt.title('Histograma')

plt.subplot(323,sharex=ax1,sharey=ax1), plt.imshow(img_ecualizada5x5,cmap='gray',vmin=0,vmax=255), plt.title('Imagen Ecualizada Ventana 5x5')
plt.subplot(324), plt.hist(img_ecualizada5x5.flatten(), 256, [0, 256]), plt.title('Histograma Imagen Ecualizada Ventana 5x5')

plt.subplot(325,sharex=ax1,sharey=ax1), plt.imshow(img_ecualizada11x11,cmap='gray',vmin=0,vmax=255), plt.title('Imagen Ecualizada Ventana 11x11')
plt.subplot(326), plt.hist(img_ecualizada11x11.flatten(), 256, [0, 256]), plt.title('Histograma Imagen Ecualizada Ventana 11x11')

plt.show(block=False)
