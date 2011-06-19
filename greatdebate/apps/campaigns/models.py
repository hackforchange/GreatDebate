from django.db import models
from greatdebate.apps.decisionMakers.models import DecisionMaker
from greatdebate.apps.organizers.models import Organizer

class Campaign(models.Model):
  """Stores Description of campaigns"""
  name = models.CharField(max_length=255, null=True, blank=True) 
  organizer = models.ForeignKey(Organizer, null=True, blank=True)
  decision_maker = models.ManyToManyField(DecisionMaker)
  campaign_url = models.TextField()
  def __unicode__(self):
    return u'%s' % (self.campaign_url[:10])
