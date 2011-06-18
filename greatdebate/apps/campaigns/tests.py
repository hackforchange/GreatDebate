from django.test import TestCase
from django.test.client import Client
from greatdebate.apps.campaigns.models import Campaign

class CampaignsTestCase(TestCase):

  def setUp(self):
    self.client = Client()


  def test_save_campaign_success_no_dm(self):
    """
    Tests we can sucessfully save a campaign with no user.
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
