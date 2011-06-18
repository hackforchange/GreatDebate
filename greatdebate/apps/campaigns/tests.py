from django.test import TestCase
from django.test.client import Client
from greatdebate.apps.campaigns.models import Campaign
from greatdebate.apps.decisionMakers.models import DecisionMaker

class CampaignsTestCase(TestCase):

  def setUp(self):
    self.client = Client()


  def test_save_campaign_success_no_dm(self):
    """
    Tests we can sucessfully save a campaign with no dm.
    """
    post_params = {
      'campaign_url': 'uniquetestcampaign.com',
      'decision_makers': '1',
      'email': 'test@test.com',
    }
    response = self.client.post('/save_campaign/', post_params)
    new_campaign_count = Campaign.objects.filter(campaign_url=post_params['campaign_url']).count()
    self.assertEqual(new_campaign_count, 1)
    #import ipdb; ipdb.set_trace()


  def test_save_campaign_success_with_dm(self):
    """
    Tests we can sucessfully save a campaign with a dm.
    """
    post_params = {
      'campaign_url': 'uniquetestcampaign.com',
      'decision_makers': '1',
      'email': 'test@test.com',
    }
    new_dm = DecisionMaker(name='Barak Obama', title='Commander and Chef')
    new_dm.save()
    response = self.client.post('/save_campaign/', post_params)
    new_campaign = Campaign.objects.filter(campaign_url=post_params['campaign_url'])
    self.assertEqual(new_campaign.count(), 1)
    self.assertEqual(new_campaign[0].decision_maker.all()[0], new_dm)
