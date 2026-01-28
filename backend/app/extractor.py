# extractor.py
from collections import defaultdict, OrderedDict
import pytesseract
from PIL import Image
import re

async def procesar_tabla(img: Image.Image, name: str):
    """
    Procesa una imagen PIL y devuelve la tabla detectada como lista de OrderedDicts
    """
    # Escalar imagen 3×
    w, h = img.size
    img_resized = img.resize((w*3, h*3), Image.Resampling.BICUBIC)

    # OCR solo números
    custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.,'
    text_data = pytesseract.image_to_data(
        img_resized, lang='spa', config=custom_config, output_type=pytesseract.Output.DICT
    )

    # Agrupar palabras por línea
    lineas = defaultdict(list)
    tolerancia = 15  # unir líneas partidas
    for i, text in enumerate(text_data['text']):
        if text.strip():
            top = text_data['top'][i]
            found_line = False
            for k in lineas:
                if abs(k - top) <= tolerancia:
                    lineas[k].append((text_data['left'][i], text))
                    found_line = True
                    break
            if not found_line:
                lineas[top].append((text_data['left'][i], text))

    # Función para unir números partidos por OCR
    def unir_numeros_partidos(palabras):
        nuevas = []
        i = 0
        while i < len(palabras):
            palabra = palabras[i]
            if re.match(r'^\d+$', palabra) and i+1 < len(palabras):
                siguiente = palabras[i+1]
                if re.match(r'^\d{2}$', siguiente):  # parte decimal
                    palabra = f"{palabra},{siguiente}"
                    i += 1
            nuevas.append(palabra)
            i += 1
        return nuevas

    # Construir tabla final
    sorted_tops = sorted(lineas.keys())
    if not sorted_tops:
        return []

    cabecera = [palabra for left, palabra in sorted(lineas[sorted_tops[0]], key=lambda x: x[0])]
    tabla_final = []

    for top in sorted_tops[1:]:
      linea_actual = [p for _, p in sorted(lineas[top], key=lambda x: x[0])]
      if not linea_actual:
          continue

      # Unir números partidos
      linea_actual = unir_numeros_partidos(linea_actual)

      # Ahora: solo asigna Kilometraje si parece un valor de kilometraje
      if re.match(r'^\d{1,2}\.\d{3}$', linea_actual[0]):
          fila = OrderedDict()
          fila["Kilometraje"] = linea_actual[0]

          # Asignar resto de palabras a cabecera más cercana
          for idx, palabra in enumerate(linea_actual[1:], start=1):
            if re.match(r'^\d{3,}$', palabra) and ',' not in palabra:
                palabra = palabra[:-2] + ',' + palabra[-2:]
                
            col_name = cabecera[idx-1] if idx-1 < len(cabecera) else f"Columna{idx-1}"
            fila[col_name] = palabra

          # Rellenar columnas vacías
          for col in cabecera:
              if col not in fila:
                  fila[col] = ""

          tabla_final.append(fila)
      else:
          # Si no es Kilometraje, asignar a última fila columna vacía '60'
          if tabla_final:
              tabla_final[-1]['60'] = linea_actual[0]

    return {
    "tabla": tabla_final,
    "name": name
}
