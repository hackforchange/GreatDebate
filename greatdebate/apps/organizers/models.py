from django.db import models

class Organizer(models.Model):
  email = models.TextField()
  def __unicode__(self):
    return u'%s' % (self.email[:10])
