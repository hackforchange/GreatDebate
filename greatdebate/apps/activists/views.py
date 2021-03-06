from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.http import require_POST, require_GET
from greatdebate.apps.activists.models import Activist, ActivistResponse
from greatdebate.apps.campaigns.models import Campaign
from greatdebate.apps.decisionMakers.models import DecisionMakerResponse

@require_POST
def process_takeaction(request):
  """
  Allows activist to fillout form and take action
  """
  if 'email' not in request.POST or 'campaign_id' not in request.POST:
    return HttpResponse('Invalid Data. Email and Campaign Required.');
  try:
    campaign = Campaign.objects.get(pk=request.POST['campaign_id'])
  except (Campaign.DoesNotExist, ValueError):
    return HttpResponse('Invalid Campaign ID')

  expected_params = [
    'email',
    'first_name',
    'last_name',
    'address',
    'city',
    'zip',
    'message',
  ]
  activist_add_params = {}
  for param in expected_params:
    if request.POST.get(param, False):
      activist_add_params[param] = request.POST[param]
    else:
      activist_add_params[param] = None

  message = activist_add_params['message']
  del activist_add_params['message']

  new_activist = Activist(**activist_add_params)
  new_activist.save();

  response_add_params = {
    'campaign': campaign,
    'activist': new_activist,
    'message': message,
  }
  new_activist_response = ActivistResponse(**response_add_params)
  new_activist_response.save()

  dm_responses = DecisionMakerResponse.objects.filter(campaign=campaign)
  context_dict = {
    'dm_responses': dm_responses,
  }
  return render_to_response('takeaction_complete.html',context_dict)


def take_action_template(request):
  """
  Requires campaign id in GET params, shows form that users can use to take action
  """
  if 'campaign_id' not in request.GET:
    return HttpResponse('campaign id not in request')
  try:
    campaign = Campaign.objects.get(pk=request.GET['campaign_id'])
  except (Campaign.DoesNotExist, ValueError):
    return HttpResponse('Campaign does not exist for %s' % (request.GET['campaign_id']))
  #import ipdb; ipdb.set_trace()
  dms = campaign.decision_maker.all()
  context_dict = {
    'dms': dms,
    'campaign': campaign,
  }
  return render_to_response('takeaction.html',context_dict)
