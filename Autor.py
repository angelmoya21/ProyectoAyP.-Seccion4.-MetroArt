class autor:
    def __init__(self,nombre,nacionalidad,fecha_de_nacimiento,fecha_de_muerte,obras):
        self.nombre=nombre
        self.nacionalidad=nacionalidad
        self.fecha_de_nacimiento=fecha_de_nacimiento
        self.fecha_de_muerte=fecha_de_muerte
        self.obras=obras
    
    def show(self):
        print('nombre del autor:',self.nombre)
        
class obra(autor):
    def __init__(self,id,titulo,nombre, nacionalidad, fecha_de_nacimiento, fecha_de_muerte, tipo,ano_de_creacion,imagen):
        super().__init__(nombre, nacionalidad, fecha_de_nacimiento, fecha_de_muerte)
        self.id=id
        self.tipo=tipo
        self.ano_de_creacion=ano_de_creacion
        self.imagen=imagen
        self.titulo=titulo
    def show(self):
        super().show()
        print('id:',self.id)
        print('titulo:',self.titulo)
        print('nombre del autor:',self.nombre)