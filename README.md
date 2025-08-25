# Python Youtube Downloader 📺

Created: Jun 10, 2023 02:15 AM

Descarga de vídeos de Youtube seleccionando la calidad usando yt-dlp. También se puede descargar solo el audio de un vídeo en la mejor calidad posible bajo el formato mp3.

## Pre-requisitos 📋

- Tener instaladas las dependencias del fichero [requirements.txt](requirements.txt)
- Tener instalado Python 3.10.11 o superior. Puede funcionar en versiones anteriores pero no se ha probado.
- El script verifica automáticamente si FFmpeg está instalado y lo instala si es necesario (soporta Windows y Linux).

## Herramientas/Librerías usadas 🛠️

Estas son las herramientas usadas durante el desarrollo del proyecto:

- [moviepy](https://pypi.org/project/moviepy/): Para montar el audio y el vídeo en un mismo fichero.
- [tkinter](https://docs.python.org/es/3/library/tkinter.html): Para generar las ventanas donde se seleccionan las carpetas, etc.
- [pyinstaller](https://www.pyinstaller.org/): Para generar el ejecutable.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp): Para descargar vídeos y audios de Youtube de forma robusta y actualizada.
- [eyed3](https://pypi.org/project/eyed3/): Para editar los metadatos de los ficheros mp3.
- [mutagen](https://pypi.org/project/mutagen/): Para editar los metadatos de los ficheros mp3. (No se usa finalmente pero esta creado el código para usarlo)



## Funcionamiento 🔧

Al iniciar la aplicación, el script verifica automáticamente la presencia de FFmpeg y lo instala si es necesario (usando winget en Windows o apt en Linux).
Luego, podemos descargar los vídeos uno a uno usando su link a Youtube, poniendo las urls en un fichero de texto y que la aplicación los descargue en bucle o ingresando una playlist de youtube mediante su URL.
El menú nos pedirá que seleccionemos una de las tres opciones:

### Descarga un solo link

Nos pedirá la url del vídeo:

Ahora tendremos que seleccionar una de estas tres opciones:

- Descarga rápida de vídeo y audio: descarga el vídeo junto con el audio en la mejor calidad disponible (usa yt-dlp).
- Descargar vídeo seleccionando la calidad: Descarga el vídeo y audio en la calidad seleccionada (usa yt-dlp).
- Descargar audio: Descarga únicamente el audio de la canción en la mejor calidad posible y lo convierte a mp3 (usa yt-dlp y FFmpeg).

### Descarga en bucle

Se nos abrira una vnetana donde nos pedirá la ruta del fichero de texto que contiene los enlaces:

El fichero tendrá este formato:

Cuando el proceso acabe, veremos los vídeos o audios en la ruta configurada.

## Expresiones de gratitud 🎁

- Comenta a otros sobre este proyecto 📢
- Da las gracias públicamente 🤓
- Sígueme en [GitHub](https://github.com/SlotyHolly) 🐦
