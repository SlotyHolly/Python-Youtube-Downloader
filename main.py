import os
from Funciones import *

parent_dir = ''
tarea = 0
key = ''
job = 0
nombre_playlist = ''
enlaces = []


import subprocess
import sys

def verificar_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except Exception:
        return False

def instalar_ffmpeg():
    import platform
    sistema = platform.system()
    print("FFmpeg no está instalado. Instalando automáticamente...")
    if sistema == "Windows":
        print("Instalando FFmpeg en Windows usando winget...")
        try:
            subprocess.run(["winget", "install", "--id", "BtbN.FFmpeg.GPL", "-e", "--accept-package-agreements", "--accept-source-agreements"], check=True)
            print("FFmpeg instalado. Reinicia la terminal si es necesario.")
        except Exception as e:
            print(f"Error instalando FFmpeg con winget: {e}")
            print("Por favor, instala FFmpeg manualmente y asegúrate de que esté en el PATH.")
            sys.exit(1)
    elif sistema == "Linux":
        print("Instalando FFmpeg en Linux usando apt...")
        try:
            subprocess.run(["sudo", "apt", "update"], check=True)
            subprocess.run(["sudo", "apt", "install", "-y", "ffmpeg"], check=True)
            print("FFmpeg instalado.")
        except Exception as e:
            print(f"Error instalando FFmpeg con apt: {e}")
            print("Por favor, instala FFmpeg manualmente usando el gestor de paquetes de tu distribución.")
            sys.exit(1)
    else:
        print("Sistema operativo no soportado para instalación automática de FFmpeg.")
        print("Por favor, instala FFmpeg manualmente y asegúrate de que esté en el PATH.")
        sys.exit(1)

if __name__ == "__main__":
    if not verificar_ffmpeg():
        instalar_ffmpeg()

    # Obtener ruta donde se guardan las descargas
    parent_dir = consultar_directorio('Carpeta')
    print('Carpeta seleccionada: {0}'.format(parent_dir), end='\n\n')
    print("Presione una tecla para continuar...")
    msvcrt.getwch()
          
    while tarea != '5':
        enlaces.clear()
        tarea = menu_inicio(parent_dir)  # Mostrar menú inicial
        loop = False
        clear()

        # Llenar una lista con los enlaces a descargar
        if tarea == '1':  # Un solo vídeo
            key = regresar_menu()
            if key == chr(27):
                continue
            enlaces.append(pide_url())

        elif tarea == '2':  # Fichero de texto
            loop = True
            ruta_fichero = consultar_directorio('Archivo')
            print('EL archivo seleccionado es : {0}'.format(ruta_fichero.name), end='\n')
            key = regresar_menu()
            if key == chr(27):
                continue
            enlaces = procesa_fichero(ruta_fichero.name)

        elif tarea == '3':  # Playlist
            loop = True
            key = regresar_menu()
            if key == chr(27):
                continue
            enlace_playlist = pide_url()
            ruta_fichero, nombre_playlist = obtener_fichero_playlist(enlace_playlist, parent_dir, nombre_playlist)
            enlaces = procesa_fichero(ruta_fichero)

        elif tarea == '4':  # Menu de configuración
            print('Menu de Configuración')
            print('---------------------')
            print('1. Cambiar carpeta de descarga')
            print('2. Regresar al menú principal')
            print('')
            print('Seleccione una opción: ', end='')
            opcion = input()
            if opcion == '1':
                parent_dir = consultar_directorio('Carpeta')
                msvcrt.getwch()
                continue

            elif opcion == '2':
                continue
        
        elif tarea == '5':  # Salir
            break

    
        # Seleccionar qué tipo de descarga hacer
        while job not in ['1', '2', '3', '4']:
            clear()
            job = seleccionar_accion()

        if key != chr(27): # Si no se presionó ESC
            # Iniciar descarga
            for x in enlaces:
                inicia_proceso_descarga(x, job, loop, nombre_playlist, parent_dir)
                clear()

    # Fin del programa
    # Ejecutamos una ventana emergente para indicar que el programa ha finalizado
    ventana = Tk()
    ventana.withdraw()
    messagebox.showinfo('Python Youtube Downloader', 'El programa ha finalizado.\nGracias por usarlo.\n\nCreado por: @SlotyHolly en GitHub')
    ventana.destroy()
