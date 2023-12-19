from objetos.Objetos import Library, Cancion
from tkinter import filedialog
import xml.etree.ElementTree as ET
class XMLReader:
    def __init__(self):
        self.ruta = self.loadXML()
        self.contenido = ""
    def loadXML(self):
        try:
            ruta  = filedialog.askopenfilename(title = "Seleccione su XML", filetypes=[("XML File", "*.xml *.XML")])
            return ruta
        except: FileNotFoundError
    def analyze(self):
        if self.ruta == "":
            print("Sin ruta XML")
            return None
        else:
            self.contenido = open(self.ruta, "r").read()
            self.biblioteca = Library()
            library = ET.fromstring(self.contenido)
            for biblioteca in library.iter("biblioteca"):
                for cancion in biblioteca.iter("cancion"):
                    nombre = cancion.attrib["nombre"]
                    album = ""
                    artista = ""
                    imagen = ""
                    ruta = ""
                    for artist, album_, image, path in zip(
                        cancion.iter("artista"), cancion.iter("album"), cancion.iter("imagen"), cancion.iter("ruta")):
                        album += album_.text
                        artista += artist.text
                        imagen += image.text
                        ruta += path.text
                    if nombre == "":
                        nombre += "single"
                    if album == "":
                        album += "single"
                    if artista == "":
                        artista += "single"
                    self.biblioteca.addSong(Cancion(nombre, album, artista, ruta, imagen))
            return self.biblioteca 
    
    
    def analyze(self):
        if self.ruta == "":
            print("Sin ruta XML")
            return None
        else:
            self.contenido = open(self.ruta, "r").read()
            self.biblioteca = Library()
            library = ET.fromstring(self.contenido)

            # Cargar canciones desde el XML a la biblioteca
            for cancion in library.iter("cancion"):
                nombre = cancion.attrib["nombre"]
                album = cancion.find("album").text
                artista = cancion.find("artista").text
                imagen = cancion.find("imagen").text
                ruta = cancion.find("ruta").text
                
                # Agregar la canción a la biblioteca
                self.biblioteca.addSong(Cancion(nombre, album, artista, ruta, imagen))

            # Generar informe HTML con cantidad de reproducciones
            self.generate_HTML_report()

            return self.biblioteca

    def generate_HTML_report(self):
        reporte_html = open("reporte_canciones.html", "w")
        reporte_html.write("<html><head><title>Informe de Canciones</title></head><body><h1>Informe de Canciones</h1>")
        reporte_html.write("<table border='1'><tr><th>Nombre Canción</th><th>Artista</th><th>Álbum</th><th>Reproducciones</th></tr>")

        # Recorrer la biblioteca y generar filas de la tabla para cada canción
        for i in range(self.biblioteca.listaArtistas.length):
            artista = self.biblioteca.listaArtistas.getById(i)
            for j in range(artista.listaAlbumes.length):
                album = artista.listaAlbumes.getById(j)
                for k in range(album.listaCanciones.length):
                    cancion = album.listaCanciones.getById(k)
                    nombre_cancion = cancion.nombre
                    nombre_artista = cancion.artista
                    nombre_album = cancion.album
                    reproducciones = 0  # Aquí deberías obtener la cantidad de reproducciones de cada canción

                    # Agregar una fila a la tabla del informe HTML
                    reporte_html.write("<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>".format(nombre_cancion, nombre_artista, nombre_album, reproducciones))

        reporte_html.write("</table></body></html>")
        reporte_html.close()