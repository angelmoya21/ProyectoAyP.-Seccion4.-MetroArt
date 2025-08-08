import requests
import json
from Departamento import Departamento
from Autor import Autor, Obra
from Nacionalidades import nacionalidades
from Imagen import guardar_imagen
from PIL import Image


class MetroArt:
    def __init__(self):
        self.departamentos = []
        self.obras = []
        
    def start(self):
        self.cargar_datos()
        
        
        while True:
            print("")
            menu = input("""--------------------------   Bienvenido a MetroArt   --------------------------
Este es el catalogo de nuestro Museo, por favor elija la opcion que desea consultar:

1- Ver Deartamentos
2- Ver Obras por Nacion
3- Ver Obras de Autor
4- Ver Detalles de la Obra
5- Salir
-------> """) 
            if menu == "1":
                self.mostrar_departamento() 

            elif menu=='2':
                self.mostrar_por_nacionalidad()
           
            elif menu == "3":
                self.mostrar_obras_autor()
                
            elif menu == "4":
                self.mostrar_detalles_obra()
                
            elif menu == "5":
                print("Gracias por tu visitarnos, esperamos haya sido de tu agrado")
                break
        
            else:
                print("Opcion Invalida")  
     
     
     
     
    def mostrar_detalles_obra(self):
         url_obras_total = "https://collectionapi.metmuseum.org/public/collection/v1/objects"
         obras_respuesta = requests.get(url_obras_total)
         obras_respuesta.raise_for_status()
         obras_formato = obras_respuesta.json()
         
         lista_obras_ids = obras_formato["objectIDs"]
         
         print(f"El numero total de IDs es de : {len(lista_obras_ids)}")
         print(f"Como ejemplo la lista de los primeros 30 IDs es la siguiente: \n {lista_obras_ids[:30]}")
         
         
         
         while True:
            obra_buscada = input("""Ingrese el ID de la Obra que desea visualizar o (x) para salir: 
------>ID: """).strip()
            
            if obra_buscada.lower() == "x":
                return
            elif not obra_buscada:
                print("Por favor debe ingresar un Id valido")
                continue
            
            elif obra_buscada.isnumeric:
                for id in lista_obras_ids:
                    if id == int(obra_buscada):
                        try:
                            url_busqueda_obra = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obra_buscada}" 
                 
                        
                            obra_busqueda_respuesta = requests.get(url_busqueda_obra)
                            obra_busqueda_respuesta.raise_for_status()
                            obra_formato = obra_busqueda_respuesta.json()
            
                            obra_objeto = Obra(obra_formato.get("objectID"), obra_formato.get("title", "Desconocido"), obra_formato.get("artistDisplayName", "Desconocido"), obra_formato.get("artistNationality", "Desconocido"), obra_formato.get("artistBeginDate", None), obra_formato.get("artistEndDate", None), obra_formato.get("classification"), obra_formato.get("objectDate"), obra_formato.get("primaryImageSmall"))  
                            print("-------------------------------------------")
                            print("")
                            obra_objeto.show_detalles()
                            print("")
                            print("-------------------------------------------")
                            
                            imagen_url = obra_formato.get("primaryImageSmall")
                            if imagen_url:
                                opcion_ver_imagen = input("Si desea ver la imagen de la obra (s) si desea salir (x): ").strip().lower()
                                if opcion_ver_imagen == "s":
                                    api_url = imagen_url
                                    nombre_archivo_destino = "logo_aleatorio"
                                    nombre_archivo_destino=guardar_imagen(api_url, nombre_archivo_destino)
                                    img = Image.open(nombre_archivo_destino)
                                    img.show()



                                    
                                    guardar_imagen(imagen_url, f"obra_{obra_buscada}")
                                    
                                elif opcion_ver_imagen == "x":
                                    return
                                
                                else:
                                    print("Obra sin imagen asociada")
                                    
                        except (requests.exceptions.RequestException, json.decoder.JSONDecodeError) as error:
                            print(f"Error en la conexion a la API, OBRA:{obra_buscada} : {error}")
                            continue
            
    def mostrar_obras_autor(self):
        while True:
            autor_buscado = input("""Ingrese el nombre del Autor del que desee ver sus obras o (x) para salir: 
------>""").strip()
            if autor_buscado.lower() == "x":
                return
            if not autor_buscado:
                print("Por favor debe ingresar un nombre valido")
                continue
            
            url_busqueda_autor = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={autor_buscado}"
            
            try:
                obras_autor_busqueda = requests.get(url_busqueda_autor)
                obras_autor_busqueda.raise_for_status()
                obras_autor_info = obras_autor_busqueda.json()
        
            except requests.exceptions.RequestException as error:
                print(f"Error en la conexion a la API: {error}")
                continue
        
            total_obras = obras_autor_info.get("total", 0)
            if total_obras == 0:
                print(f"No se encontraron obras de este Autor : {autor_buscado}. Intente con otro por favor.")
                continue
            
            print(f"El Autor : {autor_buscado} --- tiene un total de {total_obras} obras")
        
            obras_id_lista_completa = obras_autor_info.get("objectIDs", [])
            
            pagina_actual = 0
            obras_por_pagina = 20
            total_paginas = (total_obras // obras_por_pagina) + (1 if total_obras % obras_por_pagina != 0 else 0)

            while True:
                inicio = pagina_actual * obras_por_pagina
                fin = inicio + obras_por_pagina
                obras_autor_lista = obras_id_lista_completa [inicio:fin]
        
                print(f"\nMostrando la pagina {pagina_actual + 1} de {total_paginas}. \n")
                print("")
            
                print("\n---------------------| OBRAS AUTOR |---------------------\n")
        
        
                for obra_id in obras_autor_lista:
                    try:
                        url_obra_objeto = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obra_id}"
                        obra_busqueda = requests.get(url_obra_objeto)
                        obra_busqueda.raise_for_status()
                        obra_formato = obra_busqueda.json()
            
                        nueva_obra = Obra(obra_formato.get("objectID"), obra_formato.get("title", "Desconocido"), obra_formato.get("artistDisplayName", "Desconocido"), obra_formato.get("artistNationality", "Desconocido"), obra_formato.get("artistBeginDate", None), obra_formato.get("artistEndDate", None), obra_formato.get("classification"), obra_formato.get("objectDate"), obra_formato.get("primaryImageSmall"))
                        
                        if nueva_obra.nombre.lower() == autor_buscado.lower():
                            print("")
                            nueva_obra.show()
                            print("")
                
                    except (requests.exceptions.RequestException, json.decoder.JSONDecodeError) as error:
                        print(f"Error en la conexion a la API. Obra: {obra_id} : {error}")
                        continue
                opcion_pagina = input(f""" ---- Pagina {pagina_actual + 1} de {total_paginas}. 
Ingrese (s) para acceder a la siguiente pagina. 
Ingrese (a) para retroceder a la anterior.
Ingrese (x) para salir.
----->> """).strip()
            
                if opcion_pagina.lower() == "s":
                    if pagina_actual < (total_paginas - 1):
                        pagina_actual += 1
                    
                    else:
                        print("Ya te encuentras en la ultima pagina")
            
                elif opcion_pagina.lower() == "a":
                    if pagina_actual > 0:
                        pagina_actual -=1
                    else:
                        print("Ya te encuentras en la primera pagina")
            
                elif opcion_pagina.lower() == "x":
                    return
            
                else:
                    print("Esa opcion no es valida")  
        
        
    def mostrar_departamento(self):
        while True:
            print("")
            print("---------------------| DEPARTAMENTOS |---------------------")
            print("")
            for departamento in self.departamentos:
                departamento.show()
                print("")  
        
            opcion_dep = input("""Ingrese el ID del Departamento que desea ver o ingrese [x] para salir:
-------> """)
            opcion_dep_limpia = opcion_dep.strip()
        
            if opcion_dep_limpia.lower() == "x":
                return
        
            try:
                self.buscar_obras_dep(int(opcion_dep_limpia))
            
            except ValueError:
                print("ID ingresado invalido")
            except requests.exceptions.RequestException as error:
                print(f"Error en la conexion a la API: {error}")
        
    def buscar_obras_dep(self, departmentId):
        url_busqueda_dep_obras = f"https://collectionapi.metmuseum.org/public/collection/v1/search?departmentId={departmentId}&q=cat"
        
        try:
            obras_dep_busqueda = requests.get(url_busqueda_dep_obras)
            obras_dep_busqueda.raise_for_status()
            obras_dep_info = obras_dep_busqueda.json()
        
        except requests.exceptions.RequestException as error:
            print(f"Error en la conexion a la API: {error}")
            return
        
        total_obras = obras_dep_info.get("total", 0)
        print(f"El Departamento tiene un total de {total_obras} obras")
        
        obras_id_completas = obras_dep_info.get("objectIDs", [])
        
        if not obras_id_completas:
            print("Este Departamento no posee obras asociadas")
            return
        
        pagina_actual = 0
        obras_por_pagina = 20
        total_paginas = (total_obras // obras_por_pagina) + (1 if total_obras % obras_por_pagina != 0 else 0)
        
        while True:
            inicio = pagina_actual * obras_por_pagina
            fin = inicio + obras_por_pagina
            obras_dep_lista = obras_id_completas [inicio:fin]
            
            print(f"\nMostrando la pagina {pagina_actual + 1} de {total_paginas}. \n")
            print("")
            
            print("\n---------------------| OBRAS |---------------------\n")
        
            self.obra_encontrada = []
        
        
            for obra_id in obras_dep_lista:
                try:
                    url_obra_objeto = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obra_id}"
                    obra_busqueda = requests.get(url_obra_objeto)
                    obra_busqueda.raise_for_status()
                    obra_formato = obra_busqueda.json()
            
                    nueva_obra = Obra(obra_formato.get("objectID"), obra_formato.get("title", "Desconocido"), obra_formato.get("artistDisplayName", "Desconocido"), obra_formato.get("artistNationality", "Desconocido"), obra_formato.get("artistBeginDate", None), obra_formato.get("artistEndDate", None), obra_formato.get("classification"), obra_formato.get("objectDate"), obra_formato.get("primaryImageSmall"))
                    self.obra_encontrada.append(nueva_obra)
                
                except (requests.exceptions.RequestException, json.decoder.JSONDecodeError) as error:
                    print(f"Error en la conexion a la API, OBRA:{obra_id} : {error}")
                    continue
                            
            for obra in self.obra_encontrada:
                print("")
                obra.show()
                print("")
            
            opcion_pagina = input(f""" ---- Pagina {pagina_actual + 1} de {total_paginas}. 
Ingrese (s) para acceder a la siguiente pagina. 
Ingrese (a) para retroceder a la anterior.
Ingrese (x) para salir.
----->> """).strip()
            
            if opcion_pagina.lower() == "s":
                if pagina_actual < (total_paginas - 1):
                    pagina_actual += 1
                else:
                    print("Ya te encuentras en la ultima pagina")
            
            elif opcion_pagina.lower() == "a":
                if pagina_actual > 0:
                    pagina_actual -=1
                else:
                    print("Ya te encuentras en la primera pagina")
            
            elif opcion_pagina.lower() == "x":
                return
            
            else:
                print("Esa opcion no es valida")
            
    def cargar_datos(self):
        try:
            url_departamentos = "https://collectionapi.metmuseum.org/public/collection/v1/departments"
            dep_busqueda = requests.get(url_departamentos)
            dep_info = dep_busqueda.json()
        
            departamentos_dic = dep_info["departments"]
        
            self.departamentos = []
            for dep in departamentos_dic:
                self.departamentos.append(Departamento(dep["departmentId"], dep["displayName"]))
        
        except requests.exceptions.RequestException as error:
            print(f"Error en la conexion a la API: {error}")   

    def mostrar_por_nacionalidad(self):
        print("")
        print("---------------------| NACIONALIDADES |---------------------")
        print("")
        for nacion in nacionalidades:
                print(nacion)
        print("")  
        
        opcion_nacionalidad = input("""Ingrese la nacionalidad del artista que desea ver o ingrese [x] para salir:
-------> """)
        opcion_nacionalidad_limpia = opcion_nacionalidad.strip()
        
        if opcion_nacionalidad_limpia not in nacionalidades:
            print('nacionalidad invalida')
            return
    
        elif opcion_nacionalidad_limpia == "x":
            return
        
        try:
            self.buscar_obras_nacionalidad(opcion_nacionalidad_limpia)
            
        except ValueError:
            print("Nacionalidad ingresada invalida")

        
        
    def buscar_obras_nacionalidad(self, nacionalidad, query = "" ):
        url_busqueda_nacionalidad_obras = f"https://collectionapi.metmuseum.org/public/collection/v1/search?q={nacionalidad}"
        obras_nacionalidad_busqueda = requests.get(url_busqueda_nacionalidad_obras)
        obras_nacionalidad_info = obras_nacionalidad_busqueda.json()
        
        total_obras = obras_nacionalidad_info.get("total", 0)
        print(f"Existen un total de {total_obras} obras")
        
        obras_nacionalidad_lista = obras_nacionalidad_info.get("objectIDs", [])[:20]
        
        if not obras_nacionalidad_lista:
            print("Este Nacionalidad no posee obras asociadas")
            return
        
        print("\n---------------------| OBRAS |---------------------\n")
        
        self.obra_encontrada = []
        
        
        for obra_id in obras_nacionalidad_lista:
            url_obra_objeto = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obra_id}"
            obra_busqueda = requests.get(url_obra_objeto)
            obra_formato = obra_busqueda.json()
            
            nueva_obra = Obra(obra_formato.get("objectID"), obra_formato.get("title", "Desconocido"), obra_formato.get("artistDisplayName", "Desconocido"), obra_formato.get("artistNationality", "Desconocido"), obra_formato.get("artistBeginDate", None), obra_formato.get("artistEndDate", None), obra_formato.get("classification"), obra_formato.get("objectDate"), obra_formato.get("primaryImageSmall"))
            self.obra_encontrada.append(nueva_obra)
            
        for obra in self.obra_encontrada:
            print("")
            obra.show()
            print("")