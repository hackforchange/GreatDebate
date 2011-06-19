from django.test import TestCase
from django.test.client import Client
from greatdebate.apps.activists.models import Activist, ActivistResponse
from greatdebate.apps.campaigns.models import Campaign

class ActivistsTestCase(TestCase):
  
  def setUp(self):
    self.client = Client()


  def test_proccess_takeaction_success(self):
    """
    Tests that we can successfull process a take action.
    """
    new_campaign = Campaign(campaign_url='test.com')
    new_campaign.save()  
    post_params = {
      'email': 'test@test.com',
      'campaign_id': new_campaign.id,
    }
    response = self.client.post('/process_takeaction/', post_params)
    activists = Activist.objects.all()
    self.assertEqual(activists.count(), 1)
    responses = ActivistResponse.objects.filter(activist=activists[0])
    self.assertEqual(responses.count(), 1)


  def test_take_action_template(self):
    """
    tests we can server take_action_template
    """
    new_campaign = Campaign(campaign_url='test.com')
    new_campaign.save()  
    response = self.client.get('/takeaction/?campaign_id=%s' % (new_campaign.id))
    self.assertEqual('takeaction.html', response.templates[0].name) 

  def test_button_html_success(self):
    """Test we can render button.html"""
    new_campaign = Campaign(campaign_url='test.com')
    new_campaign.save()  
    response = self.client.get('/button/?campaign_id=%s' % (new_campaign.id))
    #import ipdb; ipdb.set_trace()
    self.assertEqual('button.html', response.templates[0].name)
