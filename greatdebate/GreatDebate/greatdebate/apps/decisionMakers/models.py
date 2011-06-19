from django.db import models

class DecisionMaker(models.Model):
  name = models.CharField(max_length=255)
  title = models.CharField(max_length=255)
  def __unicode__(self):
    return self.name[:10]

class DecisionMakerResponse(models.Model):
  decision_maker = models.ForeignKey(DecisionMaker)
  campaign = models.ManyToManyField('campaigns.Campaign')
  response_url = models.TextField()
  def __unicode__(self):
    return self.response_url[:10]
