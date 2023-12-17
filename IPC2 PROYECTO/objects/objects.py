import os
from tkinter import Entry
class Nodo:
    def __init__(self, value, id):
        self.value = value
        self.id = id
        self.siguiente = None
        self.anterior = None
    def __str__(self) -> str:
        return str(self.value)
class ListaDoble:
    def __init__(self):
        self.length = 0
        self.cabeza = None
        self.cola = None
    def append(self, value):
        nuevo = Nodo(value, self.length)
        if self.cabeza == None:
            self.cabeza = nuevo
            self.cola = self.cabeza
        else:
            actual = self.cola
            nuevo.anterior = actual
            self.cola = nuevo
            actual.siguiente = self.cola
        self.length += 1
    def getById(self, id):
        if self.cabeza == None:
            return "No hay cabeza"
        else:
            if id < 0 or id >= self.length:
                return "Fuera de rango"
            else:
                actual = self.cabeza
                while actual.id != id:
                    actual = actual.siguiente
                return actual.value
    def contains(self, nombre):
        if self.cabeza == None:
            return None
        else:
            actual = self.cabeza
            while actual != None:
                if actual.value.nombre == nombre:
                    break
                else:
                    actual = actual.siguiente
            if actual != None:
                return actual.id
            else:
                return None
    def __str__(self):
        if self.cabeza == None:
            return "[]"
        else:
            string = "["
            actual = self.cabeza
            while actual != None:
                if actual.siguiente == None:
                    string += "{}]".format(actual)
                else:
                    string += "{},".format(actual)
                actual = actual.siguiente
            return string
class Cancion:
    def __init__(self, nombre, album, artista, ruta, imagen):
        self.nombre = nombre
        self.album = album
        self.artista = artista
        self.ruta = ruta
        self.imagen = imagen
    def __str__(self):
        return "Canción: {}".format(self.nombre)
class Album:
    def __init__(self, nombre, imagen):
        self.nombre = nombre
        self.imagen = imagen
        self.listaCanciones = ListaDoble()
    def getCanciones(self):
        return self.listaCanciones
    def __str__(self):
        string = "\n\t\t\tAlbum: {} - Canciones:\n".format(self.nombre)
        for i in range(self.listaCanciones.length):
                string += "\n\t\t\t\t{}".format(self.listaCanciones.getById(i))       
        return string
class Artista:
    def __init__(self, nombre):
        self.nombre = nombre
        self.listaAlbumes = ListaDoble()
    def getAlbumes(self):
        lista = []
        for i in range(self.listaAlbumes.length):
            album = self.listaAlbumes.getById(i)
            lista.append(album.nombre)
        return lista
    def __str__(self):
        string = "\n\t\tArtista: {} - Albumes:".format(self.nombre)
        for i in range(self.listaAlbumes.length):
            string += "\n{}".format(self.listaAlbumes.getById(i))
        return string
class Library:
    def __init__(self):
        self.listaArtistas = ListaDoble()
    def addSong(self, song):
        new = song
        nombre = new.nombre
        album = new.album
        artista = new.artista
        imagen = new.imagen
        contains = self.listaArtistas.contains(artista)
        if contains != None:
            artist = self.listaArtistas.getById(contains)
            contains = artist.listaAlbumes.contains(album)
            if contains != None:
                album_ = artist.listaAlbumes.getById(contains)
                contains = album_.listaCanciones.contains(nombre)
                if contains != None:
                    print("Cancion en biblioteca.. Posición: {}".format(contains))
                else:
                    album_.listaCanciones.append(new)
            else:
                nuevoAlbum = Album(album, imagen)
                nuevoAlbum.listaCanciones.append(new)
                artist.listaAlbumes.append(nuevoAlbum)
        else:
            nuevoArtista = Artista(artista)
            nuevoAlbum = Album(album, imagen)
            nuevoAlbum.listaCanciones.append(new)
            nuevoArtista.listaAlbumes.append(nuevoAlbum)
            self.listaArtistas.append(nuevoArtista)
    def toList(self):#Este método retorna una lista que es necesaria
        lista = ListaDoble()
        for i in range(self.listaArtistas.length):
            artista = self.listaArtistas.getById(i)
            for j in range(artista.listaAlbumes.length):
                album = artista.listaAlbumes.getById(j)
                for k in range(album.listaCanciones.length):
                    cancion = album.listaCanciones.getById(k)
                    lista.append(cancion)
        return lista
    def report(self):
        string = """digraph G {
layout = dot;
labelloc = "t";
edge [weigth = 1000];
rankdir = LR;\n"""
        string += "\tsubgraph artistas {\n\trankdir = LR;\n"
        for i in range(self.listaArtistas.length):
            artista = self.listaArtistas.getById(i)
            string += '\t\t"{}"[fillcolor = beige style = "filled"];\n'.format(artista.nombre)
            string += '\t\t\tsubgraph "album{}"{}\n\t\t\trankdir = TB;\t\t\trank=same;\n'.format(artista.nombre,"{")
            for j in range(artista.listaAlbumes.length):
                album = artista.listaAlbumes.getById(j)
                if j == 0:
                    string += '\t\t\t\t"{}"->"{}"\n'.format(artista.nombre,album.nombre)
                string += '\t\t\t\t"{}"[fillcolor = aquamarine style = "filled"];\n'.format(album.nombre)
                string += '\t\t\t\t\tsubgraph "album{}"{}\n\t\t\t\t\trankdir = LR;\n'.format(album.nombre,"{")
                for k in range(album.listaCanciones.length):
                    cancion = album.listaCanciones.getById(k)
                    if k == 0:
                        string += '\t\t\t\t\t\t"{}"->"{}"\n'.format(album.nombre, cancion.nombre)
                    string += '\t\t\t\t\t\t\t"{}"[fillcolor = deepskyblue style = "filled"];\n'.format(cancion.nombre)
                string += '\t\t\t\t\t}\n'

            string += '\t\t\t}\n'
        string += "\t}\n"
        #Hacia delante
        for i in range(self.listaArtistas.length):
            artista = self.listaArtistas.getById(i)
            if i+1 == self.listaArtistas.length:
                string += '"{}"->"NoneR{}"[style = dashed];\n'.format(artista.nombre, i+1)
            else:
                siguiente = self.listaArtistas.getById(i+1)
                string += '"{}"->"{}";\n'.format(artista.nombre, siguiente.nombre)
            for j in range(artista.listaAlbumes.length):
                album = artista.listaAlbumes.getById(j)
                if j+1 == artista.listaAlbumes.length:
                    string += '"{}"->"NoneR{}{}"[style = dashed];\n'.format(album.nombre,i,j)
                else:
                    siguiente = artista.listaAlbumes.getById(j+1)
                    string += '"{}"->"{}";\n'.format(album.nombre, siguiente.nombre)
                for k in range(album.listaCanciones.length):
                    cancion = album.listaCanciones.getById(k)
                    if k+1 == album.listaCanciones.length:
                        string += '"{}"->"NoneR{}{}{}"[style = dashed];\n'.format(cancion.nombre,i,j,k)
                    else:
                        siguiente = album.listaCanciones.getById(k+1)
                        string += '"{}"->"{}";\n'.format(cancion.nombre, siguiente.nombre)
        #Hacia atras
        for i in range(self.listaArtistas.length-1,-1,-1):
            artista = self.listaArtistas.getById(i)
            if i-1 == -1:
                string += '"{}"->"NoneL{}"[style = dashed];\n'.format(artista.nombre,i)
            else:
                anterior = self.listaArtistas.getById(i-1)
                string += '"{}"->"{}";\n'.format(artista.nombre, anterior.nombre)
            for j in range(artista.listaAlbumes.length-1,-1,-1):
                album = artista.listaAlbumes.getById(j)
                if j-1 == -1:
                    string += '"{}"->"NoneL{}{}"[style = dashed];\n'.format(album.nombre,j,i)
                else:
                    anterior = artista.listaAlbumes.getById(j-1)
                    string += '"{}"->"{};"\n'.format(album.nombre, anterior.nombre)
                for k in range(album.listaCanciones.length-1,-1,-1):
                    cancion = album.listaCanciones.getById(k)
                    if k-1 == -1:
                        string += '"{}"->"NoneL{}{}{}"[style = dashed];\n'.format(cancion.nombre,k,j,i)
                    else:
                        anterior = album.listaCanciones.getById(k-1)
                        string += '"{}"->"{}";\n'.format(cancion.nombre, anterior.nombre)
        string += "\n}"
        file = open("library.dot", "w")
        file.write(string)
        file.close()
        os.system('dot -Tpng library.dot -o library.png')
    def getArtistas(self):
        lista = []
        for i in range(self.listaArtistas.length):
            artista = self.listaArtistas.getById(i)
            lista.append(artista.nombre)
        return lista    
    def __str__(self):
        string = "Biblioteca\n\tArtistas:\n"
        for i in range(self.listaArtistas.length):
            string += "\n\t{}".format(self.listaArtistas.getById(i))
        return string
class EntryPlaceholder(Entry):
    def __init__(self, placeholder, master = None, color = 'grey'):    
        super().__init__(master)
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color
    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color
    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()
class ListaCircular:
    def __init__(self):
        self.length = 0
        self.head = None
        self.cola = None
        self.nombre = ""
    def append(self, value):
        nuevo = Nodo(value, self.length)
        if self.head == None:
            self.head = self.cola = nuevo
            self.head.anterior = self.cola
            self.cola.siguiente = self.head
        else:
            aux = self.cola
            self.cola = aux.siguiente = nuevo
            self.cola.anterior = aux
            self.head.anterior = self.cola
            self.cola.siguiente = self.head
        self.length += 1
    def getById(self, id):
        if id < 0 or id >= self.length or self.head == None:
            return None
        else:
            actual = self.head
            while True:
                if actual.id == id:
                    break
                actual = actual.siguiente
            return actual.value
    def contains(self, object):
        if self.head == None:
            return None
        else:
            actual = self.head
            while actual.siguiente != self.head:
                if actual == object:
                    break
                else:
                    actual = actual.siguiente
            if actual != None:
                return actual.siguiente
            else:
                return None
    def __str__(self):
        string = "["
        if self.head != None:
            actual = self.head
            while True:
                if actual.siguiente == self.head:
                    string += "{}]".format(actual)
                else:
                    string += "{},".format(actual)
                actual = actual.siguiente
                if actual == self.head:
                    break

        else:
            string += "]"
        return string