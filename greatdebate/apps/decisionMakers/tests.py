from django.test import TestCase
from django.test.client import Client
from greatdebate.apps.campaigns.models import Campaign
from greatdebate.apps.decisionMakers.models import DecisionMaker

class DecisionMakersTestCase(TestCase):
  
  def setUp(self):
    self.client = Client()

  def test_response_template(self):
    """TEsts we can render a respond.html template"""
    response = self.client.get('/respond/')
    self.assertEqual(response.templates[0].name, 'response.html')
