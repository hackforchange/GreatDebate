from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.http import require_POST
from greatdebate.apps.campaigns.models import Campaign
from greatdebate.apps.decisionMakers.models import DecisionMaker
from greatdebate.apps.activists.models import Activist, ActivistResponse

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
  try:
    campaign = Campaign.objects.get(campaign_url=request.POST['campaign_url'])
    return HttpResponse('Campaign Already Exists with that url')
  except Campaign.DoesNotExist:
    new_campaign_params = {
      'campaign_url': request.POST['campaign_url'],
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
    response_iframe = '<iframe src="%sresponses/?campaign_id=%s" scrolling="no" frameboarder="0"' % (settings.URL_ROOT, campaign.id)
    takeaction_iframe = '<iframe src="%sbutton/?campaign_id=%s" scrolling="no" frameborder="0"></iframe>' % (settings.URL_ROOT, campaign.id)
    return render_to_response('create_campaign.html', {'takeaction_iframe': takeaction_iframe, 'response_iframe': response_iframe}, context_instance=RequestContext(request))

def button_html(request):
  # Returns markup for take action button
  base_url = settings.URL_ROOT
  campaign_id = request.GET.get('campaign_id', None)
  if campaign_id is None:
    return HttpResponse('NO campaign id in request')
  resp_count = ActivistResponse.objects.filter(campaign=campaign_id).count()
  context = {
    'campaign_id': campaign_id,
    'base_url': base_url,
    'resp_count': resp_count,
  }
  return render_to_response('button.html',context)

