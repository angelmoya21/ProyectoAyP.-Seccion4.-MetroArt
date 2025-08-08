#Clase autor con sus atributos y metodos

class Autor:
    def __init__(self, nombre_autor, nacionalidad, fecha_nacimiento, fecha_fallecimiento):
        self.nombre = nombre_autor
        self.nacionalidad = nacionalidad
        self.fecha_nacimiento = fecha_nacimiento
        self.fecha_fallecimiento = fecha_fallecimiento
        
    def show(self):
        pass

#Clase obra que hereda atributos y metodo de clase autor 

class Obra(Autor):
    def __init__(self, id_obra, titulo, nombre_autor, nacionalidad,  fecha_nacimiento, fecha_fallecimiento, tipo, ano_creacion, imagen):
        super().__init__(nombre_autor, nacionalidad, fecha_nacimiento, fecha_fallecimiento)
        self.id_obra = id_obra
        self.titulo = titulo
        self.tipo = tipo
        self.ano_creacion = ano_creacion
        self.imagen = imagen  
        
    def show(self):
        print(f"ID: {self.id_obra}")
        print(f"Titulo: {self.titulo}")
        print(f"Autor: {self.nombre}")

#Metodo que permite mostrar las obras y su autor de forma detallada al usuario cuando sea requerido
        
    def show_detalles(self):
        print(f"Titulo: {self.titulo}")
        print(f"Nombre del Artista: {self.nombre}")
        print(f"Nacionalidad del Artista:{self.nacionalidad}")
        print(f"Fecha de nacimiento: {self.fecha_nacimiento}")
        print(f"Fecha de muerte: {self.fecha_fallecimiento}")
        print(f"Tipo:{self.tipo}")
        print(f"Año de creacion: {self.ano_creacion}")
        
        