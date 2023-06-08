# Python Youtube Downloader 📺

Created: Jun 07, 2023 02:15 AM

Descarga de vídeos de Youtube seleccionando la calidad. También se puede descargar solo el audio de un vídeo con la mas alta posible bajo el formato mp4.

## Pre-requisitos 📋

- Tener instaladas las dependencias del fichero [requirements.txt](requirements.txt)
- Tener instalado Python 3.10.11. Puede funcionar en versiones anteriores pero no se ha probado.

## Herramientas/Librerías usadas 🛠️

Estas son las herramientas usadas durante el desarrollo del proyecto:

- [moviepy](https://pypi.org/project/moviepy/): Para montar el audio y el vídeo en un mismo fichero.
- [tkinter](https://docs.python.org/es/3/library/tkinter.html): Para generar las ventanas donde se seleccionan las carpetas, etc.
- [pyinstaller](https://www.pyinstaller.org/): Para generar el ejecutable.
- [pytube](https://pypi.org/project/pytube/): Para descargar vídeos de Youtube.
- [eyed3](https://pypi.org/project/eyed3/): Para editar los metadatos de los ficheros mp3.
- [mutagen](https://pypi.org/project/mutagen/): Para editar los metadatos de los ficheros mp3. (No se usa finalmente pero esta creado el código para usarlo)


## Funcionamiento 🔧

Podemos descargar los vídeos uno a uno usando su link a Youtube, poniendo las urls en un fichero de texto y que la aplicación los descargue en bucle o ingresando una playlist de youtube mediante su URL.

Al iniciar la aplicación nos pide que seleccionemos una de las tres opciones:

### Descarga un solo link

Nos pedirá la url del vídeo:

Ahora tendremos que seleccionar una de estas tres opciones:

- Descarga rápida de vídeo y audio: descarga el vídeo junto con el audio en baja calidad
- Descargar vídeo seleccionando la calidad: Nos mostrará las calidades disponibles en el vídeo para que seleccionemos una. Esta opción es la que más tarda porque tiene que descargar el vídeo por un lado y el audio por otro para mergearlo después. Este proceso es transparente para el usuario y se hace de forma automática.
- Descargar audio: Descarga únicamente el audio de la canción en la mas alta calidad.

### Descarga en bucle

Se nos abrira una vnetana donde nos pedirá la ruta del fichero de texto que contiene los enlaces:

El fichero tendrá este formato:

Cuando el proceso acabe, veremos los vídeos o audios en la ruta configurada.

## Expresiones de gratitud 🎁

- Comenta a otros sobre este proyecto 📢
- Da las gracias públicamente 🤓
- Sígueme en [GitHub](https://github.com/SlotyHolly) 🐦