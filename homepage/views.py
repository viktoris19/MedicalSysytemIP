from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = 'homepage/index.html'
    