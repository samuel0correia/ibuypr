from django.shortcuts import render


def index(request):
    return render(request, 'ibuy/index.html')

# Create your views here.
