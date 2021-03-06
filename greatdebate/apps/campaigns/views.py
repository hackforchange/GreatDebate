from csv import writer
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST, require_GET
from greatdebate.apps.campaigns.models import Campaign
from greatdebate.apps.organizers.models import Organizer
from greatdebate.apps.decisionMakers.models import DecisionMaker, DecisionMakerResponse
from greatdebate.apps.activists.models import Activist, ActivistResponse
from StringIO import StringIO
from django.db.models import Q
from json import dumps

def create_campaign_template(request):
  return render_to_response('create_campaign.html')

@require_POST
def save_campaign(request):
  """Creates a new campaign"""
  required_fields_list = [
    'campaign_url',
    'decision_makers',
    'email',
  ]
  for field in required_fields_list:
    if field not in request.POST:
      return HttpResponse('Missing %s param in request' % (field))
  email = request.POST.get('email', None)
  name = request.POST.get('name', None)
  new_organizer = None
  if email is not None:
    try:
      new_organizer = Organizer.objects.get(email=email)
    except Organizer.DoesNotExist:
      new_organizer = Organizer(email=email)
      new_organizer.save()
  try:
    campaign = Campaign.objects.get(campaign_url=request.POST['campaign_url'])
    return HttpResponse('Campaign Already Exists with that url')
  except Campaign.DoesNotExist:
    new_campaign_params = {
      'campaign_url': request.POST['campaign_url'],
      'organizer': new_organizer,
      'name': name,
    } 
    campaign = Campaign(**new_campaign_params)
    campaign.save()
    decision_makers = request.POST['decision_makers'].split(',') # this will be a list of ids from the form
    for dm_id in decision_makers:
      try:
        dm = DecisionMaker.objects.get(pk=dm_id)
      except DecisionMaker.DoesNotExist:
        continue
      campaign.decision_maker.add(dm)
    response_iframe = '<iframe src="%sresponses/?campaign_id=%s" height="200" height="200" scrolling="no" frameborder="0"></iframe>' % (settings.URL_ROOT, campaign.id)
    takeaction_iframe = '<iframe src="%sbutton/?campaign_id=%s" height="90" width="150" scrolling="no" frameborder="0"></iframe>' % (settings.URL_ROOT, campaign.id)
    return render_to_response('create_campaign.html', {'takeaction_iframe': takeaction_iframe, 'response_iframe': response_iframe}, context_instance=RequestContext(request))

def button_html(request):
  # Returns markup for take action button
  base_url = settings.URL_ROOT
  campaign_id = request.GET.get('campaign_id', None)
  if campaign_id is None:
    return HttpResponse('No campaign id in request')
  resp_count = ActivistResponse.objects.filter(campaign=campaign_id).count()
  context = {
    'campaign_id': campaign_id,
    'base_url': base_url,
    'resp_count': resp_count,
  }
  return render_to_response('button.html',context)

def current_campaigns(request):
  campaigns = Campaign.objects.all()
  return render_to_response('campaigns.html', {'campaigns': campaigns})

def campaign_responses(request):
  #Returns all the responses by decision makers for a given campaign
  base_url = settings.URL_ROOT
  campaign = Campaign.objects.get(pk=request.GET['campaign_id'])
  responses = DecisionMakerResponse.objects.filter(campaign=campaign)
  #import ipdb; ipdb.set_trace();
  context = {
    'base_url': base_url,
    'responses': responses,
  }
  return render_to_response('responses_widget.html',context)

def export_data(request, campaign_id):
  """exports data s csv for a certain campaign"""
  try:
    campaign = Campaign.objects.get(pk=campaign_id)
  except Campaign.DoesNotExist:
    return HttpResponse('No campaign exists with id %s' % (campaign_id))
  activist_responses = ActivistResponse.objects.filter(campaign__id=campaign_id)
  tmp_file = StringIO()
  response_csv = writer(tmp_file)
  response_csv.writerow(['First Name', 'Last Name', 'Email', 'Address', 'City', 'Zip', 'Message'])
  for activist_response in activist_responses:
    response_csv.writerow([
      activist_response.activist.first_name or 'None',
      activist_response.activist.last_name or 'None', 
      activist_response.activist.email or 'None', 
      activist_response.activist.address or 'None', 
      activist_response.activist.city or 'None', 
      activist_response.activist.zip or 'None', 
      activist_response.message or 'None',
    ])
  tmp_file.seek(0)    
  response = HttpResponse(tmp_file)
  response['Content-type'] = 'application/force-download'
  response['Content-Disposition'] = 'attachement; filename=%s.csv' % (campaign.campaign_url[:10])
  return response
  
def campaign_lookup(request, limit=5):
  #Looks up campaigns for dm's to respond to
  term = request.GET['term']
  campaigns = Campaign.objects.filter(Q(name__icontains=term))[:limit]
  results = []
  for c in campaigns:
    results.append({"label":c.name, "id":c.id})
  return HttpResponse(dumps(results), mimetype='application/javascript')

@require_GET
def campaign_responses_get(request, campaign_id):
  """exports data as json for a certain campaign"""
  try:
    campaign = Campaign.objects.get(pk=campaign_id)
  except Campaign.DoesNotExist:
    return HttpResponse('No campaign exists with id %s' % (campaign_id))
  activist_responses = ActivistResponse.objects.filter(campaign__id=campaign_id)
  output_list = []
  for activist_response in activist_responses:
    activist_tmp_dict = {
      'first_name': activist_response.activist.first_name or 'None',
      'last_name': activist_response.activist.last_name or 'None', 
      'email': activist_response.activist.email or 'None', 
      'address': activist_response.activist.address or 'None', 
      'city': activist_response.activist.city or 'None', 
      'zip': activist_response.activist.zip or 'None', 
      'message': activist_response.message or 'None',
    }
    output_list.append(activist_tmp_dict)
  return HttpResponse(dumps(output_list), mimetype='application/javascript')  





