from django import forms
from django.forms import ModelForm
from models import Enlace
from django.contrib.auth.models import User

class EnlaceForm(ModelForm):
    
    class Meta:
        model = Enlace
        exclude = ("votos","usuario","estado",)

class register_user(forms.Form):
    usuario = forms.CharField(max_length=30)
    email = forms.EmailField()
    password1 = forms.CharField(max_length=40, widget= forms.PasswordInput)
    password2 = forms.CharField(max_length=40, widget= forms.PasswordInput)
    imagen = forms.ImageField(required=False)

    #Validar de la cantidad de letras del password
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1','')
        
        num_words = len(password1)
        if num_words < 4:
            raise forms.ValidationError('Ingrese mas de 4 letras')
        if num_words > 40:
        	raise forms.ValidationError('Ingrese menos de 40 letras')
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        #Comparar las dos contrasenas  
        if password1 != password2:
            raise forms.ValidationError('Repita la contrasena correctamente')
        return password2
	

    def clean_usuario(self):
        usuario = self.cleaned_data.get('usuario','')
        us = User.objects.filter(username = usuario)
        if us:
           raise forms.ValidationError('Ese usuario ya existe!') 
        return usuario 


    def clean_email(self):
        email = self.cleaned_data.get('email','')
        em = User.objects.filter(email=email)
        if em:
            raise forms.ValidationError('Ese email ya existe!') 
        return email
        





