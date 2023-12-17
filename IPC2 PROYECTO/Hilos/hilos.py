import threading
import ctypes
from pygame import mixer

# La clase TPlay es una clase roscada que maneja la reproducción de archivos de audio usando el pygame.mixer
class TPlay(threading.Thread):
    def __init__(self, ruta, play_event, stop_event):
        threading.Thread.__init__(self)
        self.ruta = ruta
        self.play_event = play_event  # Evento para iniciar la reproducción
        self.stop_event = stop_event  # Evento para detener la reproducción
        self.estado = ""

    def run(self):
        mixer.init()
        mixer.music.load(self.ruta)
        mixer.music.set_volume(0.7)

        while True:
            self.play_event.wait()  # Esperar la señal para reproducir
            self.play_event.clear()  # Limpiar la señal para futuros usos
            mixer.music.play()

            while mixer.music.get_busy():
                if self.estado == 'p':
                    mixer.music.pause()
                    self.stop_event.wait()  # Esperar señal para detener la pausa
                    self.stop_event.clear()  # Limpiar la señal para futuros usos
                    mixer.music.unpause()
                elif self.estado == 'e':
                    mixer.music.stop()
                    break
            
            
    def get_id(self):
        if hasattr(self, "_thread_id"):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id
    def raise_exception(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')
            
    def stop_playback(self):
        self.stop_event.set()  # Enviar señal para detener la pausa o reproducción
        self.estado 