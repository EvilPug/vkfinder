from django.shortcuts import HttpResponse, get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.utils.encoding import uri_to_iri

import requests as rq


class MainPage(TemplateView):
    template_name = "intro.html"
