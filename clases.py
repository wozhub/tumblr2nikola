#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib3 import connection_from_url

from Queue import Queue
from threading import Thread

class Tumblr:
    def __init__(self, tumblr_url):
        self.url = tumblr_url
        self.pool = connection_from_url(tumblr_url,maxsize=10)
        self.posts=[]
        self.filaDescarga = Queue(maxsize=256)

        for i in range(4):
            trabajador = Thread(target=self._descargador, args=(i,))
            trabajador.setDaemon(True)

    def buscarPosts(self,):
        pagina=110

        while True:
            pagina+=1

            http = motor.request('GET','/page/%d' % pagina)
            soup = BeautifulSoup(http.data)
            http.release_conn()

    posts_pagina=[]
    for div in soup.findAll('div'):
        if div.has_key('class'):
            if 'post' in div['class']:
                post_id=div['id']
                post_url=div.find('a',{'class':'permalink'})['href']
                posts_pagina.append( Post(post_id,post_url) )

    if len(posts_pagina)==0:
        print "%d no tiene posts" % pagina
        break
    else:
        posts.extend(posts_pagina)

    def _descargador(self,i):
        while True:
            post = self.filaDescarga.get()

            if post:
                    self.posts.append(post)
                    self.filaDescarga.task_done()



    def _buscador(self,i):
        while True:

            busqueda = self.filaBusqueda.get()



class Post:
    def __init__(self,post_id,post_url):
        self.id = post_id
        self.url = post_url

    def expandir(self):
        http = motor.request('GET',purl)
        soup = BeautifulSoup(http.data)
        http.release_conn()

        div = soup.find('div',{ 'id': self.post_id })
        post = div.find('div',{ 'class':'content' })
