import requests
import json
from Departamento import Departamento
from Museo import Museo
from Obra import Autor, Obra

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
        print("")
        print("---------------------| DEPARTAMENTOS |---------------------")
        print("")
        for departamento in self.departamentos:
            departamento.show()
            print("")  
        
        opcion_dep = input("""Ingrese el ID del Departamento que desea ver o ingrese [x] para salir:
-------> """)
        opcion_dep_limpia = opcion_dep.strip()
        
        if opcion_dep_limpia == "x":
            return
        
        try:
            self.buscar_obras_dep(int(opcion_dep_limpia))
            
        except ValueError:
            print("ID ingresado invalido")
        
    def buscar_obras_dep(self, departmentId, query = "" ):
        url_busqueda_dep_obras = f"https://collectionapi.metmuseum.org/public/collection/v1/search?departmentId={departmentId}&q=cat"
        obras_dep_busqueda = requests.get(url_busqueda_dep_obras)
        obras_dep_info = obras_dep_busqueda.json()
        
        total_obras = obras_dep_info.get("total", 0)
        print(f"El Departamento tiene un total de {total_obras} obras")
        
        obras_dep_lista = obras_dep_info.get("objectIDs", [])[:20]
        
        if not obras_dep_lista:
            print("Este Departamento no posee obras asociadas")
            return
        
        print("\n---------------------| OBRAS |---------------------\n")
        
        self.obra_encontrada = []
        
        
        for obra_id in obras_dep_lista:
            url_obra_objeto = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{obra_id}"
            obra_busqueda = requests.get(url_obra_objeto)
            obra_formato = obra_busqueda.json()
            
            nueva_obra = Obra(obra_formato.get("objectID"), obra_formato.get("title", "Desconocido"), obra_formato.get("artistDisplayName", "Desconocido"), obra_formato.get("artistNationality", "Desconocido"), obra_formato.get("artistBeginDate", None), obra_formato.get("artistEndDate", None), obra_formato.get("classification"), obra_formato.get("objectDate"), obra_formato.get("primaryImageSmall"))
            self.obra_encontrada.append(nueva_obra)
            
        for obra in self.obra_encontrada:
            print("")
            obra.show()
            print("")
            
    def cargar_datos(self):
        url_departamentos = "https://collectionapi.metmuseum.org/public/collection/v1/departments"
        dep_busqueda = requests.get(url_departamentos)
        dep_info = dep_busqueda.json()
        
        departamentos_dic = dep_info["departments"]
        
        self.departamentos = []
        for dep in departamentos_dic:
            self.departamentos.append(Departamento(dep["departmentId"], dep["displayName"]))
            
            
        