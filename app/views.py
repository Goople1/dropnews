from django.shortcuts import render_to_response,get_object_or_404,render
from django.template.context import RequestContext
from models import *
from forms import * 
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from .tasks import calculo
#Usuario
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm 
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import auth
#fin
#@cache_page(6000)
def home(request):
    categorias = Categoria.objects.all()
    enlaces = Enlace.objects.order_by("-votos").all().filter(estado='1')
    template = "index.html"
    if request.user.is_authenticated():

        favorito = reportarFavoritos(request.user)
        sancion = reportarEnlacesSancionados(request.user)       
        if len(sancion) != 0:
            aux = []
            for en in enlaces:
                #Flag:flase->Si, no encuentra el id sancionado
                flag = False
                for t in sancion:
                    print "Enlace id y pk"
                    print t.get("enlace_id") 
                    print en.pk
                    if t.get("enlace_id") == en.pk:
                        flag = True
                        break

                if not flag:
                    aux.append(en)
            enlaces = aux
        return render(request,template,{"categorias" : categorias, "enlaces":enlaces,"favorito":favorito ,
            "request":request},context_instance=RequestContext(request))
    else:
        return render_to_response(template,{"categorias" : categorias, "enlaces":enlaces},context_instance=RequestContext(request))
    #favorito = EnlaceFavorito.objects.filter(usuario=request.user).values()
    #print 
    #calculo()
    #calculo.delay()
    
    #Cambiar el render_to_response para coger el contexto global o contexto local
def reportarFavoritos(user):
    return EnlaceFavorito.objects.filter(usuario=user).values()

def reportarEnlacesSancionados(user):
    return ReportarEnlace.objects.filter(usuario=user).values()


def ingresar(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            form = AuthenticationForm(request.POST)
            if form.is_valid:
                user = request.POST['username']
                clave = request.POST['password']
                acceso = authenticate(username=user,password=clave)
                if acceso is not None:
                    if acceso.is_active:
                        login(request,acceso)
                        return HttpResponseRedirect('/')
                    else:
                        form = AuthenticationForm()
                        return render_to_response('login.html',{'form':form,'error':'Su cuenta ha sido desactivada,por violar los derechos de uso'},context_instance = RequestContext(request))
                else:
                    form = AuthenticationForm()
                    return render_to_response('login.html',{'form':form,'error':'Por favor Ingrese Correctamente su usuario o password'},context_instance=RequestContext(request))
        else:
            form = AuthenticationForm()
        return render_to_response('login.html',{'form':form},context_instance=RequestContext(request))          
    else:
        return HttpResponseRedirect("/")
def salir(request):
    auth.logout(request)
    
    return HttpResponseRedirect("/")
def categoria(request,id_categoria):
    categorias = Categoria.objects.all()
    cat = get_object_or_404(Categoria,pk = id_categoria)
    #cat = Categoria.objects.get(pk = id_categoria)
    enlaces = Enlace.objects.filter(categoria = cat)
    template = "index.html"
    return render(request,template,locals())

def usuario(request):
    if not request.user.is_authenticated():
        if request.method == 'POST':
            form = register_user(request.POST,request.FILES)
            if form.is_valid():
                name_user = form.cleaned_data['usuario']
                email_user = form.cleaned_data['email']
                pass_user = form.cleaned_data['password1']

                foto = form.cleaned_data['imagen']
                if foto == None:
                    foto = "fotos/18501_thumb.jpg"
                create_user = User.objects.create_user(username= name_user, email= email_user,password=pass_user,foto = foto)          
                create_user.is_staff = True
                create_user.save()
                user = auth.authenticate(username=name_user, password=pass_user)
                if user is not None and user.is_active:
                    # Correct password, and the user is marked "active"
                    auth.login(request, user)
                
                return HttpResponseRedirect("/")
        else:
            form = register_user()
        return render_to_response('newUser.html',{'form':form},context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect("/")

@login_required(login_url='/ingresar')
def minus(request,enlace_id):
    enlace = get_object_or_404(Enlace,pk=enlace_id)
    enlace.votos = enlace.votos - 1
    enlace.save()
    return HttpResponseRedirect("/")

@login_required(login_url='/ingresar')
def plus(request,enlace_id):
    enlace = get_object_or_404(Enlace,pk=enlace_id)
    enlace.votos = enlace.votos + 1
    enlace.save()
    return HttpResponseRedirect("/")

@login_required(login_url='/ingresar')
def add(request):
    if request.POST:
        form = EnlaceForm(request.POST,request.FILES)
        if form.is_valid():
            enlace = form.save(commit = False)
            #enlace = form.save()
            imagen = form.cleaned_data['imagen']
            if imagen == None:
                imagen = "enlaces/akatsuki-500a3.png"
            enlace.imagen = imagen
            enlace.usuario = request.user
            enlace.save()
            return HttpResponseRedirect("/")
    else:
        form = EnlaceForm()
    template = "form.html"

    return render_to_response(template,context_instance=RequestContext(request,locals()))

from django.views.generic import ListView, DetailView

class EnlaceListView(ListView):
    model = Enlace
    context_object_name = 'enlaces'
    def get_template_names(self):
        return 'index.html'

class EnlaceDetailView(ListView):
    model = Enlace
    def get_template_names(self):
        return 'index.html'
 
from .serializers import EnlaceSerializer,UserSerializer
from rest_framework import viewsets
from django.contrib.auth.models import User
class EnlaceViewSet(viewsets.ModelViewSet):
    queryset = Enlace.objects.all()
    serializer_class = EnlaceSerializer   

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer   

def Error404(request):  
    return render(request,"Error404.html",context_instance=RequestContext(request))

def Error500(request):
    return render(request,"Error500.html",context_instance=RequestContext(request))


def encontrarEnlace(palabra):
    return Enlace.objects.filter(titulo__icontains=palabra)
    

def buscarEnlace(request):
    if request.is_ajax():

        try:
            en = encontrarEnlace(request.GET['busca'])
            print len(en)
            if len(en) != 0:
                return HttpResponse("busqueda?ask="+request.GET['busca'])
            else:
                return HttpResponse("0")
        except Exception, e:
            raise
  
    else:
         return HttpResponseRedirect("/")

def ask(request):
    try:
        pre = request.GET['ask']
        enl = encontrarEnlace(pre)
    except Exception, e:
        raise

    categorias = Categoria.objects.all()
    template = "busqueda.html"
    return render(request,template,{"categorias" : categorias, "enl":enl, "request":request},context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def favorito(request,enlace_id):
    enlace = get_object_or_404(Enlace,pk=enlace_id)
    encontrar = EnlaceFavorito.objects.filter(usuario=request.user, enlace=enlace,estado="1")
    if len(encontrar) == 0:
        e = EnlaceFavorito(usuario = request.user , enlace = enlace)
        e.save()
    return HttpResponseRedirect("/")

@login_required(login_url='/ingresar')
def misfavoritos(request):
    total = reportarFavoritos(request.user)
    categorias = Categoria.objects.all()
    if len(total)!= 0:
        aux = []
        for t in total:
            aux.append(Enlace.objects.get(pk=t.get("enlace_id")))
        total = aux
    template ="misfavoritos.html"
    #return render_to_response(template,{"total":total},context_instance=RequestContext(request))
    return render(request,template,{"total":total, "request":request,"categorias" : categorias},context_instance=RequestContext(request))

@login_required(login_url='/ingresar')
def reportar(request,enlace_id):
    enlace = get_object_or_404(Enlace,pk=enlace_id)
    reportar = ReportarEnlace.objects.filter(usuario=request.user, enlace=enlace)
    if len(reportar) == 0 :
        r = ReportarEnlace(usuario = request.user, enlace = enlace)
        r.save()
    return HttpResponseRedirect("/")