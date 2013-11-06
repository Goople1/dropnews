from rest_framework import serializers
from .models import Enlace
from django.contrib.auth.models import User
class EnlaceSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Enlace
		fields = ('url','titulo','enlace','votos','usuario','timestamp',)

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url','username','email',)

