class Departamento:
    def __init__(self, id, nombre, obras):
        self.id = id
        self.nombre = nombre
        self.obras = obras
        
    def show(self):
        print(f"Departamento: {self.nombre}  --  ID: {self.id}") 
          
       
