from django.shortcuts import render
from .models import Art
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import ArtForm
from django.shortcuts import redirect

def art_list(request):
    arts = Art.objects.all()
    return render(request, 'station/art_list.html', {'arts':arts})

def art_detail(request, pk):
    art = get_object_or_404(Art, pk=pk)
    return render(request, 'station/art_detail.html', {'art': art})

def art_new(request):
    arts = Art.objects.all()
    return render(request, 'station/art_list.html', {'arts':arts})
