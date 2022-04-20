
from contextlib import nullcontext
from genericpath import exists
from django.shortcuts import redirect, render
from django.template import context
from django.urls import is_valid_path
from django.views.generic.detail import DetailView
from markupsafe import re
from dashboard.models import *
from django.db.models import Q
from django.contrib import messages
from dashboard.forms import  PostoForm, UtentForm
from django.core.mail import BadHeaderError, send_mail
from rest_framework import viewsets
from .serializers import *

#Api rest
class PrenotazioneApi(viewsets.ModelViewSet):
    queryset = Prenotazione.objects.all()
    serializer_class = PrenotazioneSerializers

class PostoApi(viewsets.ModelViewSet):
    queryset = Posto.objects.all()
    serializer_class = PostoSerializers

class AirportApi(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializers

class FlyApi(viewsets.ModelViewSet):
    queryset = Fly.objects.all()
    serializer_class = FlySerializers

class AircraftApi(viewsets.ModelViewSet):
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializers

class UtentApi(viewsets.ModelViewSet):
    queryset = Utent.objects.all()
    serializer_class = UtentSerializers







# Create your views here.

def index(request):
    ls_airports = set(Airport.objects.all())
    partenza = 
    ls_airports_arrive = set(Airport.objects.all().exclude(city=partenza))
    context = {
        'aeroporti_partenza': ls_airports,
        'aeroporti_arrivi': ls_airports_arrive,
        }
    print(ls_airports_arrive)
    return render(request, 'sito/index.html',context)

def visualizza_voli(request):
    context = {}
    if request.method == 'POST':
        aeroporto_partenza = request.POST['partenze']
        aeroporto_arrivo = request.POST['arrivi']
        data_andata = request.POST.get('dataandata','')
        classe = request.POST['classe']
        adulti = request.POST.get('adulti', '')
        scelta = request.POST['scelta']
        data_ritorno = request.POST.get('dataritorno','')
        partenza = Airport.objects.get(city=aeroporto_partenza)
        arrivo = Airport.objects.get(city=aeroporto_arrivo)
        if data_ritorno == '':

            voli = Fly.objects.filter(Q(aeroporto_partenza=partenza.id) & Q(aeroporto_arrivo=arrivo.id) & Q(data_partenza=data_andata))
            if (len(voli) == 0):
                context = {
                    'voli': voli,
                    'partenza': aeroporto_partenza,
                    'arrivo' : aeroporto_arrivo,
                    'data_andata' : data_andata,
                    'classe': classe,
                    'adulti': adulti,
                    'scelta': scelta,
                    'message': 'Non ci sono voli disponibili!',
                }
            else:
                context = {
                    'voli': voli,
                    'partenza': aeroporto_partenza,
                    'arrivo' : aeroporto_arrivo,
                    'data_andata' : data_andata,
                    'classe': classe,
                    'adulti': adulti,
                    'scelta': scelta,
                    'message': 'Ecco tutti i voli disponibili!',
                }
        else:
            voli_andata = Fly.objects.filter(Q(aeroporto_partenza=partenza.id) & Q(aeroporto_arrivo=arrivo.id) & Q(data_partenza=data_andata))
            if (len(voli_andata) == 0):
                context = {
                    'voli': voli_andata,
                    'partenza': aeroporto_partenza,
                    'arrivo' : aeroporto_arrivo,
                    'data_andata' : data_andata,
                    'classe': classe,
                    'adulti': adulti,
                    'scelta': scelta,
                    'message': 'Non ci sono voli disponibili!',
                }
            else:
                context = {
                    'voli': voli_andata,
                    'partenza': aeroporto_partenza,
                    'arrivo' : aeroporto_arrivo,
                    'data_andata' : data_andata,
                    'classe': classe,
                    'adulti': adulti,
                    'scelta': scelta,
                    'message': 'Ecco tutti i voli disponibili!',
                }
                
            voli_ritorno = Fly.objects.filter(Q(aeroporto_partenza=arrivo.id) & Q(aeroporto_arrivo=partenza.id) & Q(data_partenza=data_ritorno))
            if (len(voli_ritorno) == 0):
                context['voli_ritorno'] = voli_ritorno
                context['messager'] = 'Non ci sono voli disponibili!'
    
            else:
                context['voli_ritorno'] = voli_ritorno
                context['messager'] = 'Ecco tutti i voli disponibili!'
           

    else:
        context['message'] = 'Errore'
    
    return render(request,'sito/voli.html',context)


def seleziona_posto(request,pk,adulti,classe,scelta):
    volo = Fly.objects.get(id=pk)
    form_posto = PostoForm()
    form_utente = UtentForm()
    passegeri = []
    for i in range(1,adulti+1):
        passegeri.append(i)
    context = {
        'volo': volo,
        'classe': classe,
        'adulti': adulti,
        'form_posto': form_posto,
        'form_utente': form_utente,
        'passegeri': passegeri,
        'scelta':scelta,
      
    }
    return render(request, 'sito/postieutente.html', context)

def cerca_prenotazione(request):
    context = {}
    
    if request.method == 'POST':
        code = request.POST['codice']
        try:
            prenotazione = Prenotazione.objects.get(code_prenotazione=code)
            context = {
                'prenotazione': prenotazione,
                'message': 'Ecco tutti i dettagli della tua prenotazione!',
            }
        except:
            context['message']= 'Non ci sono prenotazioni per questo codice!'
        
    else:
        context['messageform'] = 'Errore! Si prega di riprovare! '
    
    return render(request,'sito/imieivoli.html',context)



def riepilogo(request):
    context = {}
    if request.method == 'POST':
        name = request.POST['name']
        lastname = request.POST['lastname']
        email = request.POST['email']
        telefono = request.POST['telefono']
        lettera = request.POST.get('lettera', '')
        numero = request.POST.get('numero', '')
        classet = request.POST.get('classe', '')
        id_volo = request.POST.get('id_volo', '')
        adulti = request.POST.get('adulti', '')
        scelta = request.POST.get('scelta', '')
     

        volo = Fly.objects.get(id=id_volo)
        context = {
            'volo': volo,
            'name': name,
            'lastname': lastname,
            'email':email, 
            'telefono': telefono,
            'lettera': lettera,
            'numero': numero,
            'classe': classet,
            'adulti':adulti,
            'scelta': scelta,
        }

    else:
        context['message'] = 'Errore!'

    return render(request, 'sito/prenotazione.html',context)

def prenota(request):
    context = {}
    if request.method == 'POST':
        name = request.POST['name']
        lastname = request.POST['lastname']
        email = request.POST['email']
        telefono = request.POST['telefono']
        lettera = request.POST.get('lettera', '')
        numero = request.POST.get('numero', '')
        classet = request.POST.get('classe', '')
        id_volo = request.POST.get('id_volo', '')
        scelta = request.POST.get('scelta','')
        adulti = request.POST.get('adulti', '')

        volo = Fly.objects.get(id=id_volo)
        utente = Utent(name=name, lastname=lastname, email=email, telefono=telefono)
        posto = Posto(lettera=lettera, numero=numero, classe = classet)
        posto.save()
        utente.save()
        prenotazione = Prenotazione(utente=utente, volo=volo, posto=posto)
        prenotazione.save()
        send_mail(
            'Conferma Prenotazione Starvato Airlines',
            'Gentile cliente la informiamo che la sua prenotazione è andata a buon fine. Le auguriamo buon viaggio! Cordiali saluti'+
            'Di seguito il codice della sua prenotazione : ' + prenotazione.code_prenotazione,
            'mucciacitomaria@gmail.com',
            [email],
            fail_silently=False,
        ) 
         
        context = {
            'code_prenotazione' : prenotazione.code_prenotazione,
            'email': email,
            'scelta': scelta,
            'volo': volo,
            'classe': classet,
            'scelta':scelta,
            'adulti':adulti,
        }
    else:
        context['message'] = 'Errore!'
    return render(request, 'sito/pagina_conferma.html', context)
        
def cancella_prenotazione(request,id):
    context = {}
    prenotazione = Prenotazione.objects.get(id=id)
    if request.method == 'POST':
        prenotazione.delete()
        return redirect('/')
    else:
        context['message'] = 'Errore'
    context['item'] = prenotazione
    return render(request,'partials/_delete_prenotazione.html',context)


            