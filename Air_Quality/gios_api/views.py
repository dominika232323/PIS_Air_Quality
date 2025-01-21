from django.shortcuts import render, HttpResponse
from . import services

def streamlit_app(request):
    return render(request, 'streamlit_app.html')
