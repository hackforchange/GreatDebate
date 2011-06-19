from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.http import requires_POST
from greatdebate.apps.organizers.models import Organizer

def new_organizer(request):
  required_fields_list = [
    'email',
  ]

  organizer_insert_dict = {'email':request.POST['email']}
  organizer = Organizer(**organizer_insert_dict)
  organizer.save()
  return HttpResponseRedirect('/create_campaign')
