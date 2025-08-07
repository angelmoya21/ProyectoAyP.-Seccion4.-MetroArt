import requests
import json
from Departamento import Departamento
from Museo import Museo
from Autor import Autor, Obra

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
2- Ver Nacionalidades
3- Ver Autores
4- Ver Obra
5- Salir
-------> """) 
            if menu == "1":
                self.mostrar_departamento() 
                
            elif menu == "5":
                print("Gracias por tu visitarnos, esperamos haya sido de tu agrado")
                break
        
            else:
                print("Opcion Invalida")  
        
        
        
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
                    obra_formato = obra_busqueda.json()
            
                    nueva_obra = Obra(obra_formato.get("objectID"), obra_formato.get("title", "Desconocido"), obra_formato.get("artistDisplayName", "Desconocido"), obra_formato.get("artistNationality", "Desconocido"), obra_formato.get("artistBeginDate", None), obra_formato.get("artistEndDate", None), obra_formato.get("classification"), obra_formato.get("objectDate"), obra_formato.get("primaryImageSmall"))
                    self.obra_encontrada.append(nueva_obra)
                
                except requests.exceptions.RequestException as error:
                    print(f"Error en la conexion a la API: {error}")
            
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
            
        