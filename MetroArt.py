import requests
import json
from Departamento import Departamento
from Museo import Museo

class MetroArt:
    
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
                opcion_dep = input("""Ingrese el ID del Departamento que desea ver:
-------> """)
            
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

    def cargar_datos(self):
        url_departamentos = "https://collectionapi.metmuseum.org/public/collection/v1/departments"
        dep_busqueda = requests.get(url_departamentos)
        dep_info = dep_busqueda.json()
        
        departamentos_dic = dep_info["departments"]
        
        self.departamentos = []
        for dep in departamentos_dic:
            self.departamentos.append(Departamento(dep["departmentId"], dep["displayName"]))

 



