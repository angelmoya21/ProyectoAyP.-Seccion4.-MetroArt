#Clase departamento con sus atributos y metodos.

class Departamento:
    def __init__(self, id, nombre):
        self.id = id
        self.nombre = nombre
        
#Metodo que muestra nombre del departamento y su ID asociado.   
    def show(self):
        print(f"Departamento: {self.nombre}  --  ID:({self.id})") 
          
       
