#!/usr/bin/python

from requests import get
from cStringIO import StringIO


def descargaDesdeURLaArchivo(url, archivo):
    descarga = get(url)

    if descarga.status_code != 200:
        return

    print "Descargados %d kB de %s" % (len(descarga.content)/1024, url)

    with open(archivo, 'w') as salida:
        salida.write(descarga.content)


def descargaDesdeURLaStrinIO(url):
    """Descarga datos a un StringIO mediante la libreria Requests"""
    descarga = get(url)

    if descarga.status_code != 200:
        return

    # print "Descargando %s [%s]" % (url, descarga.status_code)

    try:
        print "Descargados %d kB de %s" % (len(descarga.content)/1024, url)
        fh = StringIO(descarga.content)
        return fh
    except Exception, e:
        print "Error descargando %s:\n%s\n" % (url, e)
