from django.test import TestCase
from django.test.client import Client
from greatdebate.apps.campaigns.models import Campaign
from greatdebate.apps.decisionMakers.models import DecisionMaker
from json import loads

class DecisionMakersTestCase(TestCase):
  
  def setUp(self):
    self.client = Client()

  def test_response_template(self):
    """TEsts we can render a respond.html template"""
    response = self.client.get('/respond/')
    self.assertEqual(response.templates[0].name, 'response.html')

  def test_dm_lookup_success(self):
    """Tests we can lookup a dm"""
    new_dm = DecisionMaker(name='barak obama', title='president of the us')
    new_dm.save()
    response = self.client.get('/decision_maker_lookup/?term=us')
    resp_list = loads(response.content)
    self.assertEqual(resp_list[0]['id'], new_dm.id)
    self.assertTrue(new_dm.title in resp_list[0]['label'])
    
  def test_post_response_success(self):
    """Tests we can successfull post a rsponse as a dm"""
    new_campaign = Campaign(campaign_url='test.com')
    new_campaign.save()
    new_dm = DecisionMaker(name='barak', title='pres')
    new_dm.save()
    new_campaign.decision_maker.add(new_dm)
    post_params = {
      'campaign_ids': new_campaign.id,
      'response_url': 'test.com',
    }
    response = self.client.post('/post_response/', post_params)
    #import ipdb; ipdb.set_trace()
    self.assertTrue('POST SUCCESSFUL' in response.content)
