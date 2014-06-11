#!/usr/bin/python

from bs4 import BeautifulSoup
from urllib3 import connection_from_url
import html2text

tumblr = 'moderniscima.tumblr.com'

motor = connection_from_url(tumblr,maxsize=10)
conversor = html2text.HTML2Text()
conversor.ignore_links=True

# Primero busco todos los posts que tiene, iterando pagina por pagina
pagina=100
posts=[]
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
                posts_pagina.append( (post_id,post_url) )

    if len(posts_pagina)==0:
        print "%d no tiene posts" % pagina
        break
    else:
        posts.extend(posts_pagina)

print "Encontre {0} posts".format(len(posts))

# Extraigo cada post
for pid,purl in posts:
    print pid,purl
    http = motor.request('GET',purl)
    soup = BeautifulSoup(http.data)
    http.release_conn()

    div = soup.find('div',{ 'id':pid })
    post = div.find('div',{ 'class':'content' })
    print post
#    print conversor.handle(div.prettify())
