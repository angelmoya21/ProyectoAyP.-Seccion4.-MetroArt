import requests

# Funcion Auxiliar que descarga una imagen desde un URL y la muestra.

def guardar_imagen(url, nombre_archivo):
    try: 
        response = requests.get(url, stream=True )
        response.raise_for_status    #Lanza una excepcion para codigos de estado de error (4xx o 5xx)
        
        content_type = response.headers.get("Content-Type")
        extension = ".png"
        
        if content_type:
            if "image/png" in content_type:
                extension = ".png"
            elif "image/jpeg" in content_type:
                extension = ".jpg"
            elif "image/svg+xml" in content_type:
                extension = ".svg"
                
        nombre_archivo_final = f"{nombre_archivo}{extension}"
        
        with open(nombre_archivo_final, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
               file.write(chunk)
               
        print(f"Imagen guardada exitosamente como '{nombre_archivo_final}'")
        
        
    except requests.exceptions.RequestException as e:
       print(f"Error al hacer el request: {e}")
    except IOError as e:
       print(f"Error al escribir el archivo: {e}")
    return nombre_archivo_final
