from django.shortcuts import render
from django.views.generic.detail import DetailView
from dashboard.models import *
from django.db.models import Q
from django.contrib import messages

# Create your views here.

def index(request):
    ls_airports = Airport.objects.all()
    print(ls_airports)
    context = {'aeroporti': ls_airports}
    return render(request, 'sito/index.html',context)

def visualizza_voli(request):
    context = {}
    if request.method == 'POST':
        aeroporto_partenza = request.POST['partenze']
        aeroporto_arrivo = request.POST['arrivi']
        data = request.POST['data']
        classe = request.POST['classe']
        adulti = request.POST['adulti']
        bambini = request.POST['bambini']
        partenza = Airport.objects.get(city=aeroporto_partenza)
        arrivo = Airport.objects.get(city=aeroporto_arrivo)

        voli = Fly.objects.filter(Q(aeroporto_partenza=partenza.id) & Q(aeroporto_arrivo=arrivo.id) & Q(data_partenza=data))
    
        messages.success(request, 'Ecco tutti i voli disponibili')
        
        context = {
            'voli': voli,
            'partenza': aeroporto_partenza,
            'arrivo' : aeroporto_arrivo,
            'data' : data,
            'classe': classe,
            'adulti': adulti,
            'bambini': bambini,
        }

    else:
        messages.error(request, 'Non ci sono voli disponibili!')
    
    return render(request,'sito/voli.html',context)

def seleziona(request,pk,adulti,classe):
    volo = Fly.objects.get(id=pk)
    context = {
        'volo': volo,
        'classe': classe,
        'adulti': adulti,
    }
    return render(request, 'sito/prenotazione.html', context)



