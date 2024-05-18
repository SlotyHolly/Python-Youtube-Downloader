import os
from Funciones import *

parent_dir = ''
tarea = 0
key = ''
job = 0
nombre_playlist = ''
enlaces = []

if __name__ == "__main__":

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
