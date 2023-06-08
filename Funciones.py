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

def clear():
    if os.name == 'nt':  # Para Windows
        os.system('cls')
    else:  # Para MacOS y Linux
        os.system('clear')


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


def obtener_fichero_playlist(playlist_url, path, nombre_playlist):
    playlist = Playlist(playlist_url)
    nombre_playlist = input('Ingrese el nombre de la Palylist: ')
    while nombre_playlist == '':
        print('El nombre no puede estar vacío')
        nombre_playlist = input('Ingrese el nombre de la Palylist: ')

    ruta_fichero = os.path.join(path, nombre_playlist + '.txt')

    with open(ruta_fichero, 'w') as f:
        for url in playlist.video_urls:
            f.write(url + '\n')

    return ruta_fichero, nombre_playlist


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

    file_object = open(ruta, 'r')

    for linea in file_object:
        list_enlaces.append(linea) 

    file_object.close()

    return list_enlaces


def descargar_portada(url, path):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.save(path)


def inicia_proceso_descarga(link, job, loop, nombre_playlist, parent_dir):
    contador = 1

    try:
        yt = YouTube(link)
    except:
        print('Error en el link: {0}'.format(link))
        return

    nombre_video = ''

    print('')
    print('-------------------------------------------------------')
    print('Título: {0}'.format(yt.title))
    print('Autor: {0}'.format(yt.author))
    print('')

    video_y_audio = yt.streams.filter(progressive=True).order_by('resolution').desc().first()
    vids = yt.streams.filter(mime_type='video/mp4').order_by('resolution').desc()

    if job == '1':  # Vídeo y audio rápido
        video_y_audio.download(parent_dir + '\Video')
        print_proceso_terminado()

    elif job == '2':  # Descargar vídeo y audio seleccionando calidad
        num_video_descargar = 1

        if not loop:
            print('')
            print('Seleccionar vídeo (1..{0})'.format(len(vids)))

            for video in vids:
                print('    ({1}) - {0}'.format(video, contador))
                contador += 1

            print('')

            num_video_descargar = int(input('Nº vídeo: '))

        num_video_descargar -= 1

        nombre_video = vids[num_video_descargar].default_filename
        nombre_video_final = 'f_' + nombre_video
        vids[num_video_descargar].download(parent_dir + '/Video')

        yt.streams.get_audio_only().download(parent_dir + '/Audio')

        audioclip = AudioFileClip(parent_dir + '/Audio/' + nombre_video)

        videoclip2 = VideoFileClip(parent_dir + '/Video/' + nombre_video)
        videoclip2 = videoclip2.set_audio(audioclip)

        videoclip2.write_videofile(parent_dir + '/Video/' + nombre_video_final)

        os.remove(videoclip2.filename)
        os.remove(audioclip.filename)

    elif job == '3':  # Solo audio
        if nombre_playlist == '':
            ruta_fin = yt.streams.filter(only_audio=True, mime_type='audio/mp4').order_by('abr').desc().first().download(parent_dir)
        else:
            ruta_fin = yt.streams.filter(only_audio=True, mime_type='audio/mp4').order_by('abr').desc().first().download(parent_dir + '/' + nombre_playlist)
        audioclip = AudioFileClip(ruta_fin, fps=44100)
        file_mp3 = audioclip.filename.replace('.mp4', '.mp3')
        audioclip.write_audiofile(file_mp3)

        descargar_portada(yt.thumbnail_url, parent_dir + '/portada.png')
        add_metadata(file_mp3, yt.title, yt.author, parent_dir + '/portada.png')

        audioclip.close()
        os.remove(audioclip.filename)
        os.remove(parent_dir + '/portada.png')
        
        print_proceso_terminado()


def regresar_menu():
    clear()
    print('Para regresar al menú principal presione ESC.')
    print("Presione una tecla para continuar...")
    key = msvcrt.getwch()
    return key