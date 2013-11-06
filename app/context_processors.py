from random import choice
from django.core.cache import cache
frases = ['Dotnata es flaco','Diego y Dotnata equals','Gian Carlos Cabeza de otro Cuerpo']

def ejemplo(request):
	frase = cache.get('frase_cool')
	if frase is None:
		frase = choice(frases)
		#1.Low level_>usar directamente meto:set-get
		cache.set('frase_cool',frase)
	return {'frase':frase}

from django.core.urlresolvers import reverse

def menu(request):
	menu = {'menu':[
		 {'name':'Home','url':reverse('home')},
		 {'name':'Add','url':reverse('add')},
		 {'name':'About','url':reverse('about')},	
	]}

	for item in menu['menu']:
		if request.path == item['url']:
			item['active'] = True
			print "RequestPaths:"
			print request.path

		


	return menu