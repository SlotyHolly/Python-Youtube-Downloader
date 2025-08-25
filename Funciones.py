from ast import Str
from pytube import YouTube
from pytube import Playlist
import msvcrt
import os
from moviepy.editor import *
import requests
import eyed3
from eyed3.id3.frames import ImageFrame
from PIL import Image
from io import BytesIO
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from tkinter import messagebox
from tkinter import filedialog
from tkinter import Tk


def regresar_menu():
    clear()
    print('Para regresar al menú principal presione ESC.')
    print("Presione una tecla para continuar...")
    key = msvcrt.getwch()
    return key


def menu_inicio(parent_dir) -> str:
    clear()
    print('Menu principal')
    print('--------------')
    print('La carpeta de descarga es: {0}'.format(parent_dir))
    print('')
    return input('Selecciona una opción:\n1. Descargar enlace YouTube\n2. Descargar fichero\n3. Descargar desde una playlist\n4. Menu de Configuracion\n5. Salir\n\nOpción (1|2|3|4|5): ')


def menu_configuracion() -> str:
    clear()
    return input('Selecciona una opción:\n1. Cambiar directorio de descarga\n2. Cambiar nombre de la playlist\n3. Volver al menu principal\n\nOpción (1|2|3): ')


def seleccionar_accion() -> Str:
    return input('¿Qué deseas hacer?\n\n1. Descarga rápida vídeo y audio\n2. Descarga vídeo seleccionando calidad\n3. Descarga audio.\n4. Volver al menu principal.\n\nOpción (1|2|3|4): ')


def print_proceso_terminado():
    print('Descarga completada')

    print('-------------------------------------------------------')


def add_metadata(file_path, title, artist, portada_path):
    audiofile = eyed3.load(file_path)
    
    if audiofile.tag is None:
        audiofile.initTag()

    audiofile.tag.title = title
    audiofile.tag.artist = artist

    audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(portada_path,'rb').read(), 'image/png')

    audiofile.tag.save(version=eyed3.id3.ID3_V2_3)


def agregar_caratula_con_mutagen(file_path, portada_path):
    audio = MP3(file_path, ID3=ID3)
    audio.tags.add(
        APIC(
            encoding=3,  # 3 is for utf-8
            mime='image/png',  # image/jpeg or image/png
            type=3,  # 3 es para la portada delantera
            desc='Cover',
            data=open('portada.png', mode='rb').read()
        )
    )


def pide_url() -> Str:
    return input('Ingrese la Url del video/playlist: ')


def procesa_fichero(ruta) -> list:
    list_enlaces = []

    with open(ruta, 'r') as file_object:
        for linea in file_object:
            list_enlaces.append(linea) 

    file_object.close()

    return list_enlaces


def descargar_portada(url, path):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save(path)


def consultar_directorio(std):
    ventana = Tk()
    if std == 'Carpeta':
        parent_dir = filedialog.askdirectory(initialdir="C:/", title='Seleccionar carpeta donde guardar las descargas')
        ventana.destroy()
        return parent_dir
    elif std == 'Archivo':
        parent_dir = filedialog.askopenfile(initialdir="C:/", title='Seleccione el archivo de texto con los enlaces.')
        ventana.destroy()
        return parent_dir
    else:
        print('Error en la selección de directorio')


def obtener_fichero_playlist(playlist_url, path, nombre_playlist):
    playlist = Playlist(playlist_url)
    nombre_playlist = input('Ingrese el nombre de la Playlist: ')
    while nombre_playlist == '':
        print('El nombre no puede estar vacío...')
        nombre_playlist = input('Ingrese el nombre de la Playlist: ')

    ruta_fichero = os.path.join(path, nombre_playlist + '.txt')

    with open(ruta_fichero, 'w') as f:
        for url in playlist.video_urls:
            f.write(url + '\n')

    return ruta_fichero, nombre_playlist


def clear():
    if os.name == 'nt':  # Para Windows
        os.system('cls')
    else:  # Para MacOS y Linux
        os.system('clear')


def inicia_proceso_descarga(link, job, loop, nombre_playlist, parent_dir):
    import yt_dlp
    from yt_dlp.utils import DownloadError
    
    ydl_opts = {}
    output_dir = parent_dir
    if nombre_playlist:
        output_dir = os.path.join(parent_dir, nombre_playlist)
        os.makedirs(output_dir, exist_ok=True)

    if job == '1':  # Vídeo y audio rápido
        ydl_opts = {
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
        }
    elif job == '2':  # Descargar vídeo y audio seleccionando calidad
        ydl_opts = {
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'merge_output_format': 'mp4',
        }
        # Nota: Para selección de calidad personalizada, se puede extender aquí
    elif job == '3':  # Solo audio
        ydl_opts = {
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'format': 'bestaudio/best',
            'extractaudio': True,
            'audioformat': 'mp3',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        print('Opción no válida')
        return

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print_proceso_terminado()
    except DownloadError as e:
        print(f'Error al descargar: {e}')
