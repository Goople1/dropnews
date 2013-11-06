from django.contrib import admin
from models import *
from actions import export_as_csv

class EnlaceAdmin(admin.ModelAdmin):
	list_display = ('titulo','enlace','imagen_voto','categoria','usuario','es_popular')
	list_filter = ('usuario','categoria')
	search_fields = ('categoria__titulo','usuario__email')
	#tiene que estar en list_display
	list_editable = ('enlace','categoria')
	#Asi se le asigna el link al es_popular en list_display
	list_display_links = ('es_popular',)
	actions = [export_as_csv]
	#Para las categorias se han ma rapidas
	raw_id_fields=('categoria','usuario')

	def imagen_voto(self,obj):
		url = obj.mis_votos_en_imagen_rosada()
		tag = '<img src="%s">' %url
		return tag
	

	imagen_voto.allow_tags=True
	imagen_voto.admin_order_field='votos'

class EnlaceInline(admin.StackedInline):
	model = Enlace
	extra = 1 #Para agregar!

class CategoriaAdmin(admin.ModelAdmin):
	actions = [export_as_csv]
	inlines = [EnlaceInline]

class AgregadorAdmin(admin.ModelAdmin):
	filter_horizontal = ('enlaces',)#Se cambia a horizontal o vertical se cambia la palabra	
#admin.site.register(Enlace)	
admin.site.register(Enlace,EnlaceAdmin)
admin.site.register(Categoria,CategoriaAdmin)
admin.site.register(Agregador,AgregadorAdmin)

