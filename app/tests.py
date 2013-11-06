
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Enlace, Categoria
from django.contrib.auth.models import User

class SimpleTest(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(titulo='Cat titulo')
        self.usuario = User.objects.create_user(username='julian', password='barba')

    def test_es_popular(self):
        test_enlace = Enlace.objects.create(
            titulo='Prueba', enlace='http://mejorando.la',
            categoria=self.categoria, usuario=self.usuario
            )

        # probar que cuando tengo un enlace con menos de 10
        # votos no es popular
        self.assertEqual(test_enlace.votos, 0)
        self.assertEqual(test_enlace.es_popular(), False)
        self.assertFalse(test_enlace.es_popular())

        #probar que un enlace con mas de 10 es popular
        test_enlace.votos = 50
        test_enlace.save()

        self.assertEqual(test_enlace.votos, 50, 'Yo espero que ya hayan votos')
        self.assertEqual(test_enlace.es_popular(), True)
        self.assertTrue(test_enlace.es_popular())

    def test_vistas(self):
        res = self.client.get(reverse('home'))
        self.assertEqual(res.status_code, 200)

        self.client.login(username='julian', password='barba')
        res = self.client.get(reverse('add'))
        self.assertEqual(res.status_code, 200)

    def test_add(self):
        self.assertEqual(Enlace.objects.count(), 0)
        data = {}
        data['titulo'] = 'Titulo prueba'
        data['enlace'] = 'http://google.com/'
        data['categoria'] = self.categoria.id
        self.client.login(username='julian', password='barba')
        res = self.client.post(reverse('add'), data)
        self.assertEqual(res.status_code, 302)
        self.assertEqual(Enlace.objects.count(), 1)
        enlace = Enlace.objects.all()[0]
        self.assertEqual(enlace.titulo, data['titulo'])
        self.assertEqual(enlace.enlace, data['enlace'])
        self.assertEqual(enlace.categoria, self.categoria)
