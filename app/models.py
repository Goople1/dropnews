from django.db import models
from django.contrib.auth.models import User




class Categoria(models.Model):
    titulo = models.CharField(max_length = 140)
    
    def __unicode__(self):
        return self.titulo


class Enlace(models.Model):
    titulo = models.CharField(max_length = 140)
    enlace = models.URLField()
    votos = models.IntegerField(default = 0)
    categoria = models.ForeignKey(Categoria)
    usuario = models.ForeignKey(User)
    timestamp = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='enlaces/',blank=True,null=True)
    estado = models.BooleanField(default="1")
    

    def __unicode__(self):
        return "%s -  %s" % (self.titulo,self.enlace)

    def mis_votos_en_imagen_rosada(self):
        return 'http://placehold.it/200x100/E8117F/ffffff/&text=%d+votos' % self.votos

    def es_popular(self):
        return self.votos>=5

    es_popular.boolean=True

class EnlaceFavorito(models.Model):
    tiempo = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User)
    enlace = models.ForeignKey(Enlace)

class ReportarEnlace(models.Model):
    tiempo = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User)
    enlace = models.ForeignKey(Enlace)

class Agregador(models.Model):
    titulo = models.CharField(max_length=140)
    enlaces = models.ManyToManyField(Enlace)

User.add_to_class('foto', models.ImageField(upload_to='fotos/',blank=True,null=True))

from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.sessions.models import Session
@receiver(post_save)
def clear_cache(sender, **kwargs):
    if sender != Session:
        cache.clear()
    