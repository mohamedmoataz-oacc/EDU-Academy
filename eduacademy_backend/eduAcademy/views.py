from django.shortcuts import render 

def index(request, path=None):
    if not path: return render(request, 'index.html')
    