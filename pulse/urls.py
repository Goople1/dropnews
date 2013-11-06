from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic import TemplateView
from app.views import EnlaceListView,EnlaceDetailView
from django.conf import settings
from rest_framework import routers
from app.views import EnlaceViewSet,UserViewSet
router = routers.DefaultRouter()
from app.feeds import LatestEntriesFeed
router.register(r'links',EnlaceViewSet)
router.register(r'user',UserViewSet)
handler404 = 'app.views.Error404'
handler500 = 'app.views.Error500'
urlpatterns = patterns('',
    # Examples:

    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', 'app.views.home', name='home'),
    url(r'^ingresar/$', 'app.views.ingresar', name='ingresar'),
    url(r'^salir/$', 'app.views.salir', name='salir'),
    url(r'^categoria/(\d+)$', 'app.views.categoria', name='categoria'),
    url(r'^plus/(\d+)$', 'app.views.plus', name='plus'),
    url(r'^minus/(\d+)$', 'app.views.minus', name='minus'),
    url(r'^favorito/(\d+)$', 'app.views.favorito', name='favorito'),
    url(r'^misfavoritos/$', 'app.views.misfavoritos', name='misfavoritos'),
    url(r'^reportar/(\d+)$', 'app.views.reportar', name='reportar'),
    url(r'^add/$', 'app.views.add', name='add'),
    url(r'^usuario/$', 'app.views.usuario', name='usuario'),
    url(r'^buscarEnlace/$', 'app.views.buscarEnlace', name='buscarEnlace'),
    url(r'^busqueda', 'app.views.ask', name='ask'),
    url(r'^about/$', TemplateView.as_view(template_name='index.html'), name='about'),
    url(r'^enlaces/$', EnlaceListView.as_view(), name='enlaces'),
    url(r'^enlaces/(?P<pk>[\d]+)$', EnlaceDetailView.as_view(), name='enlace'),
    url(r'^rss/', LatestEntriesFeed()), #  presta atencion a LatestEntriesFeed()
    # url(r'^pulse/', include('pulse.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',
    {'document_root':settings.MEDIA_ROOT,}
    ),
)
