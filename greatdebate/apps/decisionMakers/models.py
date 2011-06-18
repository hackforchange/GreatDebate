from django.db import models

class DecisionMaker(models.Model):
  name = models.CharField(max_length=255)
  title = models.CharField(max_length=255)
  def __unicode__(self):
    return self.name[:10]
