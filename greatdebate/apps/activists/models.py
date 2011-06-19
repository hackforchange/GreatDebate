from django.db import models

class Activist(models.Model):
  """
  Activists are people that take action on certain campaigns
  """
  first_name = models.CharField(max_length=20, null=True, blank=True)
  last_name = models.CharField(max_length=20, null=True, blank=True)
  email = models.CharField(max_length=255, null=True, blank=True)
  address = models.CharField(max_length=255, null=True, blank=True)
  city = models.CharField(max_length=255, null=True, blank=True)
  zip = models.IntegerField(null=True, blank=True)

  def __unicode__(self):
    return u'%s-%s' % (self.first_name,self.last_name)

class ActivistResponse(models.Model):
  """
  This is the object for an activist's response for a specific campaign
  """
  campaign = models.ForeignKey('campaigns.Campaign')
  activist = models.ForeignKey(Activist) 
  message = models.TextField(null=True, blank=True)

  def __unicode__(self):
    return u'%s-%s' % (self.campaign.campaign_url[:8], self.activist.first_name)
