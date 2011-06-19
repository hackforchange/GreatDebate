from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.decorators.http import require_POST
from greatdebate.apps.organizers.models import Organizer

def new_organizer(request):
  required_fields_list = [
    'email',
  ]
  organizer_insert_dict = {'email':request.POST['email']}
  organizer = Organizer(**organizer_insert_dict)
  organizer.save()
  return HttpResponseRedirect('/create_campaign/')

def render_home(request):
  return render_to_response('home.html')
