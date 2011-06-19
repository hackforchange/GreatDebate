from django.shortcuts import render_to_response

def create_campaign_template(request):
  return render_to_response('create_campaign.html')
