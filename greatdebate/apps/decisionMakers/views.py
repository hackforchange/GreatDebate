from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.http import require_POST
from greatdebate.apps.campaigns.models import Campaign
from greatdebate.apps.decisionMakers.models import DecisionMaker, DecisionMakerResponse
from json import dumps

def decision_maker_lookup(request, limit=5):
  """
  For finding a decision maker for organizers search
  """
  term = request.GET['term']
  decision_makers = DecisionMaker.objects.filter(Q(name__icontains=term) | Q(title__icontains=term))[:limit]
  results = []
  for dm in decision_makers:
    results.append({"label":dm.name + ' ' + dm.title,"id":dm.id})
  return HttpResponse(dumps(results), mimetype='application/javascript')

def get_responses(request):
  #Get's all the 
  campaign = Campaign.objects.get(pk=request.GET['campaign_id'])
  dm_responses = DecisionMakerResponse.objects.filter(campaign=campaign)
  context_dict = {
    'dm_responses': dm_responses,
  }
  return render_to_response('responses.html', context_dict)

def post_response(request):
  # Saves DM's response to a set of campaigns
  campaigns = request.POST['campaign_ids'].splt(',')
  camapaign_list = []
  for campaign_id in campaigns:
    campaign = Campaign.objects.get(pk=campaign_id)
    campaigns_list.append(campaign)

  response_add_params = {
    'response_url': request.POST['response_url'],
    'decision_maker': campaigns_list[0].decision_maker.all()[0]
  }
  new_response = DecisionMakerResponse(**response_add_params)
  new_response.save();

  for campaign in campaigns_list:
    new_response.campaign.add(campaign)

  return HttpResponse('POST SUCCESSFUL PLACEHOLDER')

def response_template(request):
  # Renders DM response page
  return render_to_response('respond.html')
