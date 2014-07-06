#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib3 import connection_from_url
from html2text import HTML2Text

from Queue import Queue
from threading import Thread

from funciones import *


class Tumblr:
    def __init__(self, tumblr_url):
        self.url = tumblr_url
        self.pool = connection_from_url(tumblr_url, maxsize=10)
        self.posts = []
        self.filaDescarga = Queue(maxsize=256)

        for i in range(1):
            trabajador = Thread(target=self._descargador, args=(i,))
            trabajador.setDaemon(True)
            trabajador.start()

    def buscarPosts(self,):
#        pagina = 110
        pagina = 0

        while True:
            http = self.pool.request('GET', '/page/%d' % pagina)
            soup = BeautifulSoup(http.data)
            http.release_conn()

            posts = 0
            for div in soup.findAll('div'):
                if div.has_attr('class'):
                    if 'post' in div['class']:
                        posts = 1
                        post = Post(
                            div['id'],
                            div.find('a', {'class': 'permalink'})['href'],
                            div['class'][1],
                            self.pool
                        )
                        self.filaDescarga.put(post)

            if posts == 0:
                print "%d no tiene posts" % pagina
                break

            pagina += 1

    def _descargador(self, i):
        while True:
            post = self.filaDescarga.get()

            if post:
                    post.expandir()
                    self.filaDescarga.task_done()


class Post:
    def __init__(self, post_id, post_url, post_type, http_pool):
        print post_id, post_url, post_type
        self.id = post_id
        self.url = post_url
        self.post_type = post_type
        self.pool = http_pool
        self.contenido = ""
        self.adjunto = ""

    def expandir(self):
        http = self.pool.request('GET', self.url)
        soup = BeautifulSoup(http.data)
        http.release_conn()

        h = HTML2Text()
        h.ignore_links = True

        div = soup.find('div', {'id': self.id})
        contenido = div.find('div', {'class': 'content'})

        self.contenido = h.handle(contenido.prettify())

        if self.post_type == "photo":
            url = div.find('a', {'class': 'zoom'})['href']
            archivo = url.split('/')[-1]
            descargaDesdeURLaArchivo(url, archivo)
            self.adjunto = archivo

        elif self.post_type == "audio":
            link = div.find('iframe', {'class': 'tumblr_audio_player'})['src']
            link = link.split('?', 1)[0].split('/')[-1]
            archivo = "%s.mp3" % self.id
            url = "https://a.tumblr.com/%so1.mp3" % link
            self.adjunto = archivo
            descargaDesdeURLaArchivo(url, archivo)
