import numpy as np
import cv2
from PIL import Image

def porcentaje_color(img, lower, upper):
    """Calcula el porcentaje de píxeles dentro de un rango HSV dado."""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    porcentaje = (np.sum(mask > 0) / mask.size) * 100
    return porcentaje

async def clasificar_etiqueta(img: Image.Image, name:str):
    """Clasifica la etiqueta ambiental según los colores detectados."""
    # Convertir PIL.Image a array OpenCV (BGR)
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # Rango de colores HSV (ajustables según tus imágenes)
    rangos = {
        "azul": ([90, 50, 50], [130, 255, 255]),
        "verde": ([35, 40, 40], [85, 255, 255]),
        "amarillo": ([20, 100, 100], [35, 255, 255]),
    }

    resultados = {}
    for color, (low, high) in rangos.items():
        low_np, high_np = np.array(low), np.array(high)
        resultados[color] = porcentaje_color(img_cv, low_np, high_np)

    azul = resultados["azul"]
    verde = resultados["verde"]
    amarillo = resultados["amarillo"]

    if azul > 20 and verde > 20:
        etiqueta = "ECO"
    elif azul > max(verde, amarillo):
        etiqueta = "Cero emisiones"
    elif verde > max(azul, amarillo):
        etiqueta = "C"
    elif amarillo > max(azul, verde):
        etiqueta = "B"
    else:
        etiqueta = "No identificada"

    return {
        "etiqueta_detectada": etiqueta,
        "porcentajes": resultados,
        "name": name
    }
