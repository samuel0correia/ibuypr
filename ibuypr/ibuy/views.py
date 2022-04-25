from django.shortcuts import render


def index(request):
    return render(request, 'ibuy/index.html')

def minhaconta(request):
    return render(request, 'ibuy/minhaconta.html')

# Create your views here.
